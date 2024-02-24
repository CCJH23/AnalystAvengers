<template>
  <Sidebar />
  <v-container fluid class="top-container">
    <img src="../assets/logo.png" alt="Logo" class="logo">
    <span class="text-center bold headline">Latest Server Logs</span>
  </v-container>
  <v-container fluid class="bottom-container">
    <v-container class="fluid inner-container-1">
      <v-row style="margin-bottom:18px" class="service-label">
        <v-col class="col-title">Infrastructure Name</v-col>
        <v-col class="col-title">Infrastructure Type</v-col>
        <v-col class="col-title">Log Date Time</v-col>
        <v-col class="col-title">Server Availability</v-col>
        <v-col class="col-title">Server CPU Utilization</v-col>
        <v-col class="col-title">Server Disk Utilization</v-col>
        <v-col class="col-title">Server Memory Utilization</v-col>
        <v-col class="col-title">Server Network Availability</v-col>
      </v-row>
      <v-row class="row-with-border" v-for="(log, index) in latestServerLogs" :key="index">
        <v-col cols="2" class="col-content">{{ log.InfrastructureName }}</v-col>
        <v-col cols="1" class="col-content">{{ log.InfrastructureType }}</v-col>
        <v-col cols="2" class="col-content">{{ log.LogDateTime }}</v-col>
        <v-col cols="1" class="col-content">
          <img v-if="log.ServerAvailability === 0" src="../assets/unhealthy_logo.png" alt="Unhealthy" class="row-logo">
          <img v-else src="../assets/healthy_logo.png" alt="Healthy" class="row-logo">
        </v-col>
        <v-col cols="1" class="col-content">{{ (parseFloat(log.ServerCpuUtilisation)).toFixed(5) }}%</v-col>
        <v-col cols="1" class="col-content">{{ (parseFloat(log.ServerDiskUtilisation)).toFixed(5) }}%</v-col>
        <v-col cols="1" class="col-content">{{ (parseFloat(log.ServerMemoryUtilisation)).toFixed(5) }}%</v-col>
        <v-col cols="1" class="col-content">
          <img v-if="log.ServerNetworkAvailability === 0" src="../assets/unhealthy_logo.png" alt="Unhealthy" class="row-logo">
          <img v-else src="../assets/healthy_logo.png" alt="Healthy" class="row-logo">
        </v-col>
      </v-row>
    </v-container>
  </v-container>
</template>

<script setup>
  import Sidebar from "@/components/Navbar/Sidebar.vue";
  import { ref, onMounted } from 'vue';
  import io from 'socket.io-client';
  
  const latestServerLogs = ref([]);
  
  // Establish SocketIO connection
  const socket = io('http://localhost:8000/latestlogs');
  
  socket.on('connect', () => {
    console.log('SocketIO connection established');
  });
  
  // Listen for the 'latest_server_logs' event
  socket.on('latest_server_logs', (data) => {
    try {
      console.log('Received latest_server_logs event:', data);  
      latestServerLogs.value = data.data.latest_server_logs;
      console.log('Received latest server logs:', latestServerLogs.value);
    } catch (error) {
      console.error('Error in latest_server_logs event listener:', error);
    }
  });
  
  socket.on('error', (error) => {
    console.error('SocketIO error:', error);
  });
  
  socket.on('disconnect', () => {
    console.log('SocketIO connection closed');
  });
  
  // Cleanup SocketIO connection on component unmount
  onMounted(() => {
    console.log('Component mounted');
    socket.emit('serverlog')
    return () => {
      console.log('Component unmounted');
      socket.disconnect();
    };
  });
</script>


<style>
.col-content{
  font-size: 14px; /* Adjust the font size as needed */
  text-align: center; /* Center-align the text */
}

.col-title{
  font-size: 15px; /* Adjust the font size as needed */
  text-align: center;
}

.top-container {
  height: auto; /* Let the height adjust based on content */
  display: flex;
  flex-direction: column; /* Stack items vertically */
  justify-content: center;
  align-items: center;
}

.bottom-container {
  display: flex;
  flex-direction: column; /* Stack items vertically */
  align-items: center;
  background-color: rgb(239, 244, 246);
  padding-top: 20px; /* Add padding to reduce gap */
  padding-bottom: 20px; /* Add padding to reduce gap */
}

.inner-container-1 {
  background-color: white;
  position: relative; /* To position the label */
  max-width: 100%; /* Ensure container does not exceed screen width */
  overflow-x: auto; /* Allow horizontal scrolling if content overflows */
}

.text-center {
  display: block;
  text-align: center;
}

.bold {
  font-weight: bold;
}

.headline {
  font-size: 24px;
  margin: 0; /* Remove margin to prevent any unwanted spacing */
}

.logo {
  width: 80px;
  height: auto;
}

.service-label {
  font-weight: bold;
  font-size: 20px;
}

.row-with-border {
  border-bottom: 1px solid black;
}

.row-logo {
  width: 10px;
  height: auto;
  margin: 5px;
}

</style>
  