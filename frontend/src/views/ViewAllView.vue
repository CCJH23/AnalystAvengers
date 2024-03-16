<script setup>
    import Sidebar from "@/components/Navbar/Sidebar.vue";
</script>
<template>
    <div>
      <Sidebar/>
      <v-container fluid class="bottom-container">
        <v-container class="fluid inner-container-1">
          <v-row style="margin-bottom:18px" class="service-label" data-aos="fade-down">Service Health</v-row>
          <v-row class="row-with-border">
            <v-col cols="2" style="color: #a7c6ba; font-weight: bold;">Service Groups</v-col>
            <v-col cols="8" style="text-align: center; color: #a7c6ba; font-weight: bold;">Service Group Status</v-col>
            <v-col cols="2"></v-col>
          </v-row>
          <v-row class="row-with-border" v-for="(serviceGroup, idx) in Object.keys(serviceGroups)" :key="idx" data-aos="fade-down">
            <v-col cols="2">{{ serviceGroupNames[serviceGroup] }}</v-col>
            <v-col cols="8" :style="{ 'text-align': 'center', color: getServiceGroupColor(serviceGroup)}">{{ serviceGroupComments[serviceGroup] }}</v-col>
            <v-col cols="2">
              <v-btn variant="text" :to="'view/' + serviceGroup">View</v-btn>
            </v-col>
          </v-row>
          <v-row style="margin-top:38px">
            <v-col cols="4">
            </v-col>
            <v-col data-aos="fade-down">
              <img src="../assets/healthy.png" alt="Logo" class="row-logo" style="width: 15px; height: 15px; margin-top: 5px;">
              <span>Healthy</span>
            </v-col>          
            <v-col data-aos="fade-down">
              <img src="../assets/degraded.png" alt="Logo" class="row-logo" style="width: 15px; height: 15px;">Degraded
            </v-col>
            <v-col data-aos="fade-down">
              <img src="../assets/unhealthy.png" alt="Logo" class="row-logo" style="width: 15px; height: 15px;">Unhealthy
            </v-col>
            <v-col cols="4">
            </v-col>
          </v-row>
        </v-container>
      </v-container>
    </div>
</template>
  
<script>
import io from 'socket.io-client';
import axios from 'axios';

export default {
  data(){
    return {
        servers: {},
        serviceGroups: {},
        serviceGroupNames: {},
        serviceGroupComments: {},
    }
  },
  async mounted(){
    await this.getServersStatus()
    await this.getServiceGroups()
  },
  watch: {
    servers: {
      handler: function (newValue) {
          if (Object.keys(newValue).length > 0) {
          // Get Infrastructure Data when Server data changes
          this.getInfrastructureConfigData(this.servers)
          }
      },
      deep: true, // Watch nested properties
      immediate: true, // Trigger the handler immediately during the component's creation
    },
  },
  methods: {
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
    async getServiceGroups(){
      const response = await axios.get('http://52.138.212.155:8000/serviceGroup')
      for (var service of response.data){
        this.serviceGroupNames[service.ServiceId] = service.ServiceName
      }
    },
    async getInfrastructureConfigData(servers){
      var infrastructureName = null
      for (var server in servers){
        infrastructureName = server
        const response = await axios.get(`http://52.138.212.155:8000/infrastructureconfig/infrastructure_config/${infrastructureName}`);
        const serverConfigData = response.data.data.server_configuration
        const groupId = serverConfigData['GroupId']
        // Check if groupId exists in serviceGroups, if not, add it
        if (!this.serviceGroups.hasOwnProperty(groupId)) {
          this.serviceGroups[groupId] = []; // Initialize as an array
        }
        // Add serverConfigData to the corresponding group
        this.serviceGroups[groupId].push(serverConfigData);
      }
      for (const groupId in this.serviceGroups){
        this.serviceGroupComments[groupId] = this.getServiceGroupComments(this.serviceGroups[groupId], this.servers)
      }
    },
    getServiceGroupComments(group, servers){
      console.log(servers, group)
      var criticalArr = []
      for (const server of group){
        const serverName = server['InfrastructureName']
        const serverStatus = servers[serverName]
        if (serverStatus == 'Unhealthy'){
          criticalArr.push(serverName)
        }
      }
      if (criticalArr.length === 0) {
        return "Everything is healthy.";
      } else {
        return `Service Group is unhealthy`;
      }
    },
    getServiceGroupColor(serviceGroup) {
      const status = this.serviceGroupComments[serviceGroup];
      if (status === 'Everything is healthy.') {
        return 'green';
      } else {
        return 'red';
      }
    }
  }
}
</script>

<style>
  .top-container {
    height: 20vh; /* Set height of the container to full viewport height */
    display: flex;
    flex-direction: column; /* Stack items vertically */
    justify-content: center; /* Center items vertically */
    align-items: center; /* Center items horizontally */
  }

  .bottom-container {
    display: flex;
    flex-direction: column; /* Stack items vertically */
    align-items: center;
    height: 80vh; /* Span entire viewport height */
    background-color: rgb(239, 244, 246)
  }

  .inner-container-1{
    background-color: white;
    position: relative; /* To position the label */
    height: 710px;
    width: 1200px;
    padding: 50px;
    margin: 20px 0; /* Add margin between service label and rows */
  }

  .text-center {
    display: block;
    text-align: center;
  }

  .bold {
    font-weight: bold;
    margin: 0; /* Remove margin to prevent any unwanted spacing */
  }

  .headline {
    font-size: 24px; /* Adjust the font size as needed */
    font-weight: bold;
    text-align: center; /* Center align the text */
    margin: 0; /* Remove default margin */
  }

  .logo {
    width: 120px; /* Adjust the width of the logo */
    height: auto;
  }

  .service-label {
    top: 5;
    left: 5;
    font-weight: bold;
    padding: 10px;
    font-size: 20px;
    color: #a7c6ba;
  }

  .row-with-border {
    border-bottom: 1px solid black; /* Add border to the bottom of each row */
    margin-bottom: -1px; /* Offset the margin for better alignment */
  }

  .row-logo {
    width: 15px; /* Adjust the width of the row logo */
    height: auto;
    margin: 5px; /* Add margin between row logos */
  }
</style>
