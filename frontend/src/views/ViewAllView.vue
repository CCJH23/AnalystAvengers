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
            <v-col cols="4" style="text-align: center; color: #a7c6ba; font-weight: bold;">Healthy Servers</v-col>
            <v-col cols="4" style="text-align: center; color: #a7c6ba; font-weight: bold;">Critical Servers</v-col>
            <v-col cols="2"></v-col>
          </v-row>
          <v-row class="row-with-border" v-for="(serviceGroup, idx) in Object.keys(serviceGroups)" :key="idx" data-aos="fade-down">
            <v-col cols="2">{{ serviceGroup }}</v-col>
            <v-col cols="4" style="text-align: center; color: green;">{{ serviceGroups[serviceGroup]['Healthy'] }}</v-col>
            <v-col cols="4" style="text-align: center; color: red;">{{ serviceGroups[serviceGroup]['Critical'] }}</v-col>
            <v-col cols="2">
              <v-btn variant="text" :to="'view/' + serviceGroup">View</v-btn>
            </v-col>
          </v-row>
          <v-row class="row-with-border" v-for="(rowLabel, rowIndex) in rowLabels" :key="rowIndex" data-aos="fade-down">
            <v-col cols="2">
              <!-- Render different icons based on the label -->
              <v-icon v-if="rowLabel === 'UBS Website'">mdi-web</v-icon>
              <v-icon v-else-if="rowLabel === 'UBS Trading Platform'">mdi-swap-horizontal</v-icon>
              <v-icon v-else-if="rowLabel === 'UBS Intranet'">mdi-web-box</v-icon>
              <v-icon v-else-if="rowLabel === 'UBS Wealth Management Platform'">mdi-currency-usd</v-icon>
              <v-icon v-else-if="rowLabel === 'UBS Mobile Banking App'">mdi-cellphone</v-icon>
              <v-icon v-else-if="rowLabel === 'UBS Online Banking Platform'">mdi-bank-transfer</v-icon>
              <v-icon v-else-if="rowLabel === 'UBS Financial Advisor Platform'">mdi-account-tie</v-icon>
              <!-- Add more conditions for other labels and their corresponding icons -->
              {{ rowLabel }}
            </v-col>
            <v-col cols="2" v-for="(colIndex, index) in 5" :key="colIndex">
              <img v-if="index !== 3" src="../assets/healthy.png" alt="Healthy Logo" class="row-logo" />
              <img v-else src="../assets/unhealthy.png" alt="Unhealthy Logo" class="row-logo" @load="hasUnhealthyLogo = true" />
              <!-- <img src="../assets/degraded.png" alt="Degraded Logo" class="row-logo" @load="hasUnhealthyLogo = true"/> -->
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
        serviceGroups: {}
    }
  },
  async mounted(){
    await this.getServersStatus()
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
      socket.on('health_status', (data) => {
          var servers = data.data
          for (var server of servers){
              var infrastructureName = server.InfrastructureName
              var overallHealthStatus = server.OverallHealthStatus
              this.servers[infrastructureName] = overallHealthStatus
          }
      })
    },
    async getInfrastructureConfigData(servers){
      var infrastructureName = null
      for (var server in servers){
          var serverStatus = servers[server]
          infrastructureName = server
          const response = await axios.get(`http://52.138.212.155:8000/infrastructureconfig/infrastructure_config/${infrastructureName}`);
          const serverConfigData = response.data.data.server_configuration
          const groupId = serverConfigData['GroupId']
          console.log(server)
          // Check if groupId exists in serviceGroups, if not, add it
          if (!this.serviceGroups.hasOwnProperty(groupId)) {
            this.serviceGroups[groupId] = {}
          }
          if (!this.serviceGroups[groupId].hasOwnProperty(serverStatus)){
            this.serviceGroups[groupId][serverStatus] = 1
          } else {
            this.serviceGroups[groupId][serverStatus] += 1
          }
      }
    },
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
