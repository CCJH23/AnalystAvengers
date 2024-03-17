<script setup>
    import Sidebar from "@/components/Navbar/Sidebar.vue";
    import MapComponent from "@/components/MapComponent.vue";
</script>

<template>
    <div>
        <Sidebar/>
        <div data-aos="fade-down">
            <div class="content">
                <div class="titles">Service Group {{ group }} Details</div>
                <div class="message" v-if="message.length > 0">{{ message }}</div>
                <div v-show="!Object.keys(servers).length > 0">Loading Topology Diagram...</div>
                <svg v-show="Object.keys(servers).length > 0" ref="chart" class="svg-container"></svg>
                <div v-show="!buildMap">Loading Map...</div>
            </div>
            <MapComponent v-if="buildMap" :mapData="mapComponentData" :servers="servers" :group="group"></MapComponent>
            <v-row style="margin-top:10px; margin-left:70px">
                <v-col cols="4">
                </v-col>
                <v-col>
                <img src="../assets/healthy.png" alt="Logo" class="row-logo" style="width: 15px; height: 15px; margin-top: 5px;">
                <span>Healthy</span>
                </v-col>          
                <v-col>
                <img src="../assets/degraded.png" alt="Logo" class="row-logo" style="width: 15px; height: 15px;">Degraded
                </v-col>
                <v-col>
                <img src="../assets/unhealthy.png" alt="Logo" class="row-logo" style="width: 15px; height: 15px;">Unhealthy
                </v-col>
                <v-col cols="4">
                </v-col>
            </v-row>
            <v-row>
                <v-btn
                color="#c5dad2"
                class="buttonstyle"
                dark
                right
                @click="$router.push('/')"
                >
                Return to Home 
            </v-btn>
            </v-row>
        </div>
    </div>
</template>

<script>
import * as d3 from 'd3';
import axios from 'axios';
import io from 'socket.io-client';

export default {
    components: {
        MapComponent,
    },
    watch: {
    servers: {
        handler: function (newValue) {
            if (Object.keys(newValue).length > 0) {
            // Update the chart when servers changes and is not empty
            this.getInfrastructureConfigData(this.servers)
            this.message = "Change Detected in Topology Mapping"
            setTimeout(() => {
                this.message = ""
            }, 3000);
            window.addEventListener('resize', this.createTopologyChart);
            }
        },
        deep: true, // Watch nested properties
        immediate: true, // Trigger the handler immediately during the component's creation
        },
    },
    async mounted(){
        await this.getServersStatus()
        this.mapping = await this.getMapping()
        this.allPaths = await this.getTopologyMapping(this.mapping, this.group)
    },
    data(){
        return {
            servers: {},
            mapping: {},
            allPaths: [],
            serversSvg: new Set(),
            uniqueConnections: new Set(),
            message: '',
            group: 1,
            mapComponentData: {},
            buildMap: false,
        }
    },
    created(){
        this.group = Number(this.$route.params.serviceGroup)
    },
    methods: {
        svgClickEvent(d){
            this.$router.push(`/vieweachserver/${d.name}`);
        },
        dragged(event, d){
            d3.select(this).attr("cx", d.x = event.x).attr("cy", d.y = event.y);
        },
        getServersStatus(){
            // Establish SocketIO connection
            const socket = io('http://52.138.212.155:8000/latestlogs');
            socket.on('new_health_status', (data) => {
                var servers = data.data
                for (var server in servers){
                    if (server != ''){
                        var infrastructureName = server
                        var overallHealthStatus = servers[server]
                        this.servers[infrastructureName] = overallHealthStatus
                    }
                }
            })
        },
        async getInfrastructureConfigData(servers){
            var infrastructureName = null
            for (var server in servers){
                infrastructureName = server
                const response = await axios.get(`http://52.138.212.155:8000/infrastructureconfig/infrastructure_config/${infrastructureName}`);
                const serverConfigData = response.data.data.server_configuration
                const groupId = serverConfigData['GroupId']
                const country = serverConfigData['InfrastructureCountry']
                const infrastructureType = serverConfigData['InfrastructureType']
                if (groupId == this.group){
                    this.mapComponentData[infrastructureName] = {}
                    this.mapComponentData[infrastructureName]['groupId'] = groupId
                    this.mapComponentData[infrastructureName]['country'] = country
                    this.mapComponentData[infrastructureName]['infrastructureType'] = infrastructureType
                }
            }
            await this.createTopologyChart(this.allPaths, this.servers, this.mapComponentData);
        },
        async getMapping(){
            try {
                const response = await axios.get("http://52.138.212.155:8000/mappingGraph")
                return response.data
            } catch (error) {
                console.error("Error fetching data from the API", error)
            }
        },
        getTopologyMapping(graph, serviceGroup){
            const filteredData = graph.filter(item => item.ServiceGroup === serviceGroup);
            const allPaths = this.findAllPaths(filteredData)
            return allPaths
        },
        findAllPaths(graph){
            const adjacencyList = {};
            // Build the adjacency list
            for (const edge of graph) {
                if (!adjacencyList[edge.ParentEdge]) {
                    adjacencyList[edge.ParentEdge] = [];
                }
                adjacencyList[edge.ParentEdge].push(edge.ChildEdge);
            }
            const paths = [];
            function dfs(node, currentPath) {
                currentPath.push(node);
                if (!adjacencyList[node] || adjacencyList[node].length === 0) {
                    // Reached a leaf node, add the current path to the list
                    paths.push([...currentPath]);
                } else {
                    // Continue DFS for each adjacent node
                    for (const neighbor of adjacencyList[node]) {
                        dfs(neighbor, currentPath);
                    }
                }
                // Backtrack: remove the last node when moving back up the path
                currentPath.pop();
            }
            // Start DFS from each node
            for (const startNode in adjacencyList) {
                dfs(startNode, []);
            }
            var strArr = [];
            for (var path of paths){
                strArr.push(path.join(','))
            }
            function isSubset(str1, str2) {
                return str2.includes(str1);
            }
            // Loop through strArr
            for (var i = 0; i < strArr.length; i++) {
                for (var j = 0; j < strArr.length; j++) {
                    if (i !== j && isSubset(strArr[i], strArr[j])) {
                        // Check which string is longer and remove the shorter one
                        if (strArr[i].length > strArr[j].length) {
                            strArr.splice(j, 1);
                        } else {
                            strArr.splice(i, 1);
                        }
                        // After removing a string, adjust the loop variables and break
                        i--;
                        break;
                    }
                }
            }
            // Convert each string into an array
            var arrayOfArrays = strArr.map(function(str) {
                return str.split(',');
            });

            // Resulting array of arrays
            return arrayOfArrays;
        },
        async createTopologyChart(allPaths, summarisedServerStatus, mapComponentData){
            d3.select(this.$refs.chart).selectAll("*").remove();
            this.buildMap = true
            const serverNameMap = new Map();
            const links = []
            var parentY = 100;
            var idx = 0;
            for (const path of allPaths) {
                var parentX = 100;
                const servers = path.map((server, index) => ({
                    id: idx += 1,
                    name: server,
                    x: parentX + (200 * index),
                    y: parentY
                }));
                // Create links between servers
                for (let i = 0; i < servers.length - 1; i++) {
                    links.push({
                        source: servers[i].name,
                        target: servers[i + 1].name
                    });
                }
                servers.forEach((server) => {
                    // Check if the server name is not already in the map
                    if (!serverNameMap.has(server.name)) {
                        // Add country to server object
                        server['country'] = mapComponentData[server.name]['country']
                        // Add the server name to the map
                        serverNameMap.set(server.name, true);
                        // Add the server object to the set
                        this.serversSvg.add(server);
                    }
                });
                // Create links between servers using their IDs
                parentY += 100;
            }
            var connections = new Set();
            for (var link of links){
                var source = link['source']
                var target = link['target']
                var connectionObj = {};
                for (var server of this.serversSvg){
                    var sourceId = null;
                    var targetId = null;
                    if (server['name'] == source){
                        sourceId = server['id']
                        connectionObj['source'] = sourceId
                    }
                    if (server['name'] == target){
                        targetId = server['id']
                        connectionObj['target'] = targetId
                    }
                }
                connections.add(connectionObj)
            }
            for (const obj of connections){
                const isUnique = [...this.uniqueConnections].every(
                    uniqueObj => uniqueObj.source !== obj.source || uniqueObj.target !== obj.target
                );

                if (isUnique) {
                    this.uniqueConnections.add(obj);
                }
            }

            const parentWidth = window.innerWidth;
            const svg = d3.select(this.$refs.chart);
            const g = svg.append('g');
            const handleZoom = (e) => g.attr('transform', e.transform);
            const zoom = d3.zoom().on('zoom', handleZoom);
            // Add zooming and panning
            d3.select('svg').call(zoom);
            const height = 400;
            g.selectAll('*').remove();
            g.attr('width', parentWidth).attr('height', height);
            // Add a border to the SVG
            g.style('border', '1px solid black');
            // Add instruction text
            svg.append('text')
                .attr('x', 10) // Adjust the horizontal position as needed
                .attr('y', 20) // Adjust the vertical position as needed
                .text("Click and drag to pan around, and use your mouse scroll or keypad to zoom in and out.")
                .style('font-size', '12px')
                .style('fill', 'black');
            // Load image dynamically
            const serverImageURL = await import('@/assets/server.png');
            const webAppImageURL = await import('@/assets/app.png');

            console.log(mapComponentData)

            // Add icons of virtual machines under service group to d3
            g
            .selectAll('image')
            .data(this.serversSvg)
            .enter()
            .append('image')
            .attr('x', (d) => d.x - 20)
            .attr('y', (d) => d.y - 20)
            .attr('xlink:href', (d) => (mapComponentData[d.name]['infrastructureType'] === 'server' ? serverImageURL.default : webAppImageURL.default))
            .attr('width', 40)
            .attr('height', 40)
            .style('cursor', 'pointer')
            .on('click', (event, d) => {
                this.svgClickEvent(d); // Add clickevent for each icon
            })
            // Append server names
            g
            .selectAll('text')
            .data(this.serversSvg)
            .enter()
            .append('text')
            .attr('x', (d) => d.x)
            .attr('y', (d) => d.y + 30)
            .text((d) => d.name)
            .style('text-anchor', 'middle')
            .style('font-size', '12px')
            .style('cursor', 'pointer')
            .on('click', (event, d) => {
                this.svgClickEvent(d); // Add clickevent for each virtual server name
            })
            // Convert set to array for easy manipulation
            const serversArray = Array.from(this.serversSvg);
            // Append connections
            const connectionsSvg = g
            .selectAll('line')
            .data([...this.uniqueConnections])
            .enter()
            .append('line')
            .style('stroke', 'black') // Set the color of the lines
            .style('stroke-width', 1); // Set the width of the lines
            // Update the position of the lines based on source and target servers
            connectionsSvg
            .attr('x1', (d) => serversArray.find(server => server.id === d.source).x)
            .attr('y1', (d) => serversArray.find(server => server.id === d.source).y)
            .attr('x2', (d) => serversArray.find(server => server.id === d.target).x)
            .attr('y2', (d) => serversArray.find(server => server.id === d.target).y)
            .style('stroke', 'black')
            .style('stroke-dasharray', '5,5')  // Adjust the values for dashed pattern
            .style('stroke-width', 3);  // Adjust the value for line thickness
            // Append status text
            g
            .selectAll('statusText')
            .data(this.serversSvg)
            .enter()
            .append('text')
            .attr('x', (d) => d.x)
            .attr('y', (d) => d.y - 25) // Adjust the vertical position as needed
            .text((d) => summarisedServerStatus[d.name] || "Status Not Found") // Corrected this line
            .style('text-anchor', 'middle')
            .style('font-size', '10px')
            .style('fill', (d) => (this.servers[d.name] === 'Healthy' ? 'green' : 'red'));
            // Append country text
            g
            .selectAll('countryText')
            .data(this.serversSvg)
            .enter()
            .append('text')
            .attr('x', (d) => d.x)
            .attr('y', (d) => d.y - 40) // Adjust the vertical position as needed
            .text((d) => d.country || "Status Not Found") // Corrected this line
            .style('text-anchor', 'middle')
            .style('font-size', '10px')
            .style('fill', 'blue');
        }
    }
}

</script>

<style scoped>
svg {
  border: 1px solid black;
  width: 30%;
  height: 400px;
}
div {
  margin: 10px;
}
.buttonstyle {
  margin-top: 0px;
  margin-bottom: 24px;
  font-size: 16px;
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
.titles{
    color: #a7c6ba;
    font-size: 20px;
    font-weight: bold;
    padding-top: 20px;
}
.center {
    display: flex;
    justify-content: center; /* Horizontally center the content */
    align-items: center; /* Vertically center the content */
}
.content {
text-align: center; /* Optionally, center the text within the content */
}
.svg-container {
    width: 100%;
}
</style>