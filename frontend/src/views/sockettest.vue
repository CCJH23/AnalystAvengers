<!-- Pulling data for the servers logs table in vieweachserver pages-->
<template>
  <Sidebar />
  <v-container fluid class="top-container">
    <!-- Logo and page headline -->
    <img src="../assets/logo.png" alt="Logo" class="logo">
    <span class="text-center bold headline">Latest Server Logs</span>
  </v-container>
  <v-container fluid class="bottom-container">
    <!-- Container for the server logs table -->
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
      <!-- Table rows for server logs -->
      <v-row class="row-with-border" v-for="(log, index) in latestServerLogs" :key="index">
        <v-col cols="2" class="col-content">{{ log.InfrastructureName }}</v-col>
        <v-col cols="1" class="col-content">{{ log.InfrastructureType }}</v-col>
        <v-col cols="2" class="col-content">{{ log.LogDateTime }}</v-col>
        <v-col cols="1" class="col-content">
          <img v-if="log.ServerAvailability === 0" src="../assets/unhealthy.png" alt="Unhealthy" class="row-logo">
          <img v-else src="../assets/healthy.png" alt="Healthy" class="row-logo">
        </v-col>
        <!-- Server utilization metrics -->
        <v-col cols="1" class="col-content">{{ (parseFloat(log.ServerCpuUtilisation)).toFixed(5) }}%</v-col>
        <v-col cols="1" class="col-content">{{ (parseFloat(log.ServerDiskUtilisation)).toFixed(5) }}%</v-col>
        <v-col cols="1" class="col-content">{{ (parseFloat(log.ServerMemoryUtilisation)).toFixed(5) }}%</v-col>
        <v-col cols="1" class="col-content">
          <img v-if="log.ServerNetworkAvailability === 0" src="../assets/unhealthy.png" alt="Unhealthy" class="row-logo">
          <img v-else src="../assets/healthy.png" alt="Healthy" class="row-logo">
        </v-col>
      </v-row>
    </v-container>
  </v-container>
</template>

<script setup>
  // Importing required components and Vue functionalities
  import Sidebar from "@/components/Sidebar.vue";
  import { ref, onMounted } from 'vue';
  import io from 'socket.io-client'; // Import socket.io-client for real-time web socket communication
  
  const latestServerLogs = ref([]);
  
  // Establish SocketIO connection
  const socket = io('http://52.138.212.155:8000/latestlogs');
  
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
  font-size: 14px; 
  text-align: center;
}

.col-title{
  font-size: 15px; 
  text-align: center;
}

.top-container {
  height: auto; 
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.bottom-container {
  display: flex;
  flex-direction: column; 
  align-items: center;
  background-color: rgb(239, 244, 246);
  padding-top: 20px; 
  padding-bottom: 20px; 
}

.inner-container-1 {
  background-color: white;
  position: relative; 
  max-width: 100%; 
  overflow-x: auto; 
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
  margin: 0; 
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
  