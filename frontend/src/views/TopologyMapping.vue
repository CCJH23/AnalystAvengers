<template>
  <div>
    <div class="message" v-if="this.message.length > 0">{{ message }}</div>
    <div v-show="!Object.keys(summarisedServerStatus).length > 0">Loading Topology Map...</div>
    <svg v-show="Object.keys(summarisedServerStatus).length > 0" ref="chart"></svg>
    <div v-if="this.report.length > 0">{{ report }}</div>
  </div>
</template>

<script>
import * as d3 from 'd3';
import axios from 'axios';
import io from 'socket.io-client';

// Establish Mapping Graph connection

export default {
  props: {
    currentServer: String,
  },
  watch: {
    summarisedServerStatus: {
      handler: function (newValue) {
        if (Object.keys(newValue).length > 0) {
          // Update the chart when summarisedServerStatus changes and is not empty
          this.createTopologyChart(this.mapping, this.summarisedServerStatus);
          this.message = "Change Detected in Topology Mapping"
          this.report = ""
          setTimeout(() => {
            this.message = ""
          }, 3000);
          var incidentServerArr = [];
          for (var server in this.summarisedServerStatus){
            // if server is critical, store in incidentServerArr
            if (this.summarisedServerStatus[server] == "Critical"){
              incidentServerArr.push(server)
            }
          }
          if (incidentServerArr.length > 0){
            var serversStr = ""
            for (var i = 0; i < incidentServerArr.length; i++){
              if (i < incidentServerArr.length - 1){
                serversStr += `${incidentServerArr[i]}, `
              } else {
                serversStr += `and ${incidentServerArr[i]}`
              }
            }
            this.report += `It seems that servers ${serversStr} are under critical condition, and have issues. Please look into it.`
          }
          window.addEventListener('resize', this.createTopologyChart);
        }
      },
      deep: true, // Watch nested properties
      immediate: true, // Trigger the handler immediately during the component's creation
    },
  },
  data(){
    return {
      mapping: {},
      currentNode: this.currentServer,
      servers: {},
      message: "",
      summarisedServerStatus: {},
      report: ""
    }
  },
  async mounted() {
    await this.getServersStatus()
    var mapping = await this.getMapping()
    const topologyMapping = this.getTopologyMapping(mapping, this.currentNode);
    this.mapping = topologyMapping
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.createTopologyChart);
  },
  methods: {
    handleSvgClick(data) {
      // Your logic for handling SVG click goes here
      console.log('SVG Clicked:', data);
    },
    getServersStatus(){
      // Establish SocketIO connection
      const socket = io('http://52.138.212.155:8000/latestlogs');
      // Listen for the 'historical_server_logs' event
      socket.on('new_health_status', (data) => {
          var servers = data.data
          for (var server of servers){
            var infrastructureName = server.InfrastructureName
            var serverType = server.InfrastructureType
            var overallHealthStatus = server.OverallHealthStatus
            var healthStatus = server.HealthStatus
            this.servers[infrastructureName] = {}
            this.servers[infrastructureName]['serverType'] = serverType
            this.servers[infrastructureName]['overallHealthStatus'] = overallHealthStatus
            this.servers[infrastructureName]['healthStatus'] = healthStatus
            this.summarisedServerStatus[infrastructureName] = overallHealthStatus
          }
      });
      // setTimeout(() => {
      //   this.summarisedServerStatus = {
      //       "4.231.173.187:9100": "Healthy",
      //       "20.123.40.22": "Healthy",
      //       "4.231.170.13": "Critical",
      //       "4.231.171.90": "Healthy",
      //       "74.234.41.9": "Critical"
      //   }
      // }, 3000);
      // setTimeout(() => {
      //   this.summarisedServerStatus = {
      //       "4.231.173.187:9100": "Critical",
      //       "20.123.40.22": "Healthy",
      //       "4.231.170.13": "Critical",
      //       "4.231.171.90": "Healthy",
      //       "74.234.41.9": "Critical"
      //   }
      // }, 20000);
    },
    async getMapping(){
      try {
        const response = await axios.get('http://52.138.212.155:8000/mappingGraph');
        return response.data
      } catch (error) {
        console.error("Error fetching data from the API", error)
      }
    },
    getTopologyMapping(graph, node){
      const result = {
        currentEdge: node,
        parentEdges: [],
        childEdges: [],
        siblingEdges: []
      };
      // Helper function to check for uniqueness and not equal to the node's IP address
      const isUniqueAndNotEqual = (ip, array, nodeIP) => !array.includes(ip) && ip !== nodeIP;
      // var index = -1;
      // for (var obj of graph) {
      //   if (obj['ParentEdge'] === result.currentEdge || obj['ChildEdge'] === result.currentEdge) {
      //     index = obj.index;
      //     break; // Assuming you want to exit the loop once you find a matching object
      //   }
      // }
      var index = -1
      for (var i = 0; i<graph.length; i++){
        if (graph[i]['ParentEdge'] == result.currentEdge || graph[i]['ChildEdge'] == result.currentEdge){
          index = i
        }
      }
      if (index !== -1) {
        // Move the variable at 'index' to index 0
        const movedElement = graph.splice(index, 1)[0];
        graph.splice(0, 0, movedElement);
      }
      for (var obj of graph) {
        // if node is in parent
        if (obj['ParentEdge'] === node && isUniqueAndNotEqual(obj['ChildEdge'], result.childEdges, node)) {
          // Append the corresponding ChildEdge to childEdges in result
          result.childEdges.push(obj['ChildEdge']);
        }
        // if node is in child
        if (obj['ChildEdge'] === node && isUniqueAndNotEqual(obj['ParentEdge'], result.parentEdges, node)) {
          // Append the corresponding ParentEdge to parentEdges in result
          result.parentEdges.push(obj['ParentEdge']);
        }
        // check if obj has the same child as the given node (i.e., obj is a sibling)
        if (
          (result.childEdges.includes(obj['ChildEdge'])) &&
          isUniqueAndNotEqual(obj['ParentEdge'], result.siblingEdges, node)
        ) {
          // Append the sibling to siblingEdges in result if not already present and not equal to the node's IP address
          var siblingObj = {}
          siblingObj['ParentEdge'] = obj['ParentEdge']
          siblingObj['ChildEdge'] = obj['ChildEdge']
          result.siblingEdges.push(siblingObj)
        }
        // check if obj has the same parent as the given node (i.e., obj is a sibling)
        if (
          (result.parentEdges.includes(obj['ParentEdge'])) &&
          isUniqueAndNotEqual(obj['ChildEdge'], result.siblingEdges, node)
        ) {
          // Append the sibling to siblingEdges in result if not already present and not equal to the node's IP address
          var siblingObj = {}
          siblingObj['ParentEdge'] = obj['ParentEdge']
          siblingObj['ChildEdge'] = obj['ChildEdge']
          result.siblingEdges.push(siblingObj)
        }
      }
      return result;
    },
    async createTopologyChart(mappings, summarisedServerStatus) {
      const {currentEdge, parentEdges, childEdges, siblingEdges} = mappings

      // Set a common x-coordinate for parentEdges
      var parentX = 100
      // Generate servers array for parentEdges
      const parentServers = parentEdges.map((ip, index) => ({
        id: index + 1,
        name: ip,
        x: parentX,
        y: index * 100 + 50
      }))
      parentX += 200
      // Add the server for currentEdge
      const currentServer = {
          id: parentEdges.length + 1,
          name: currentEdge,
          x: parentX, // Set x-coordinate for currentEdge
          y: 50, // Set y-coordinate for currentEdge
      };
      // Generate servers array for siblingEdges
      const siblingServers = [];
      for (const siblingEdge of siblingEdges) {
        const { ParentEdge, ChildEdge } = siblingEdge;
        // Check if ParentEdge is in parentServers
        const parentServer = parentServers.find(server => server.name === ParentEdge);
        if (parentServer) {
          siblingServers.push({
            id: parentServers.length + 1 + siblingServers.length + 1,
            name: ChildEdge,
            x: parentX, // Assuming a horizontal layout, adjust as needed
            y: 100 + 50 * (siblingServers.length + 1)
          });
        } else {
          siblingServers.push({
            id: parentServers.length + 1 + siblingServers.length + 1,
            name: ParentEdge,
            x: parentX,
            y: 100 + 50 * (siblingServers.length + 1)
          });
        }
      }
      parentX += 200
      // Generate servers array for childEdges
      const childServers = childEdges.map((ip, index) => ({
        id: parentServers.length + 1 + siblingServers.length + 1 + index,
        name: ip,
        x: parentX,
        y: index * 100 + 50
      }))
      // Combine parentServers and currentServer
      const servers = [...parentServers, currentServer, ...siblingServers, ...childServers];
      // Generate connections array for parentEdges to currentEdge
      const parentConnections = parentEdges.map((parentEdge, index) => ({
          source: parentServers[index].id,
          target: currentServer.id,
      }));
      // Generate connections array for currentEdge to childServers
      const childConnections = childEdges.map((childEdge, index) => ({
          source: currentServer.id,
          target: childServers[index].id,
      }));
      // Generate connections array for siblingEdges to parentEdges of childEdges
      const siblingConnections = siblingEdges.map((siblingEdge, index) => {
        var parentEdge = siblingEdge['ParentEdge']
        var childEdge = siblingEdge['ChildEdge']
        if (parentEdges.includes(parentEdge)){
          const parentServerObject = parentServers.find(server => server.name === parentEdge);
          var id = parentServerObject.id
          return {
            source: parentServerObject.id,
            target: siblingServers[index].id
          }
        } else {
          const childServerObject = childServers.find(server => server.name === childEdge);
          var id = childServerObject.id
          return {
            source: childServerObject.id,
            target: siblingServers[index].id
          }
        }
      })
      // Combine parentConnections and childConnections
      const connections = [...parentConnections, ...childConnections, ...siblingConnections];
      const parentWidth = this.$el.clientWidth;
      const svg = d3.select(this.$refs.chart);
      const height = 300;
      svg.selectAll('*').remove();
      svg.attr('width', parentWidth).attr('height', height);
      // Add a border to the SVG
      svg.style('border', '1px solid black');
      // Load image dynamically
      const serverImageURL = await import('@/assets/server.png');
      // Append server images with the correct path
      const serverImages = svg
      .selectAll('image')
      .data(servers)
      .enter()
      .append('image')
      .attr('x', (d) => d.x - 20)
      .attr('y', (d) => d.y - 20)
      .attr('xlink:href', serverImageURL.default)
      .attr('width', 40)
      .attr('height', 40)
      .style('filter', (d) => {
        // Apply different colors or styles based on health status
        const status = summarisedServerStatus[d.name];
        return status === 'Healthy' ? 'none' : 'url(#grayscale)';
      })
    // Append server names
    svg
      .selectAll('text')
      .data(servers)
      .enter()
      .append('text')
      .attr('x', (d) => d.x)
      .attr('y', (d) => d.y + 30)
      .text((d) => d.name)
      .style('text-anchor', 'middle')
      .style('font-size', '12px')

    // Append server status text
    svg
      .selectAll('statusText')
      .data(servers)
      .enter()
      .append('text')
      .attr('x', (d) => d.x)
      .attr('y', (d) => d.y + 50) // Adjust the vertical position as needed
      .text((d) => summarisedServerStatus[d.name] || 'Status not available')
      .style('text-anchor', 'middle')
      .style('font-size', '10px')
      .style('fill', (d) => (summarisedServerStatus[d.name] === 'Healthy' ? 'green' : 'red'))
    svg.selectAll('line')
      .data(connections)
      .enter()
      .append('line')
      .attr('x1', (d) => servers.find((s) => s.id === d.source).x)
      .attr('y1', (d) => servers.find((s) => s.id === d.source).y)
      .attr('x2', (d) => servers.find((s) => s.id === d.target).x)
      .attr('y2', (d) => servers.find((s) => s.id === d.target).y)
      .style('stroke', 'black')
      .style('stroke-dasharray', '5,5')
      .style('stroke-width', 3)
    },
  },
};
</script>

<style scoped>
svg {
  border: 1px solid black;
}
div {
  margin: 10px;
}
.buttonstyle {
  float: right;
  margin-top: 50px;
  margin-bottom: 10px;
  font-size: 10px;
}
.message {
  background-color: lightblue;
  padding: 10px;
  margin-left: 0;
  margin-right: 0;
  margin-bottom: 10px;
  border-radius: 10px;
  text-align: center;
}
/* Add any additional styling for your SVG here */
</style>
