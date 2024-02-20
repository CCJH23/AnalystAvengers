<template>
    <Sidebar/>
    <v-container fluid class="top-container">
      <img src="../assets/logo.png" alt="Logo" class="logo">
      <span class="text-center bold headline">Latest Server Logs</span>
    </v-container>
    <v-container fluid class="bottom-container">
      <v-container class="fluid inner-container-1">
        <v-row style="margin-bottom:18px" class="service-label">Server Logs</v-row>
        <v-row class="row-with-border" v-for="(log, index) in latestServerLogs" :key="index">
          <v-col cols="2">
            {{ log.ServerName }}
          </v-col>
          <v-col cols="2">
            {{ log.CPUUtilization }}
          </v-col>
          <v-col cols="2">
            {{ log.DiskUtilization }}
          </v-col>
          <v-col cols="2">
            {{ log.MemoryUtilization }}
          </v-col>
          <v-col cols="2">
            {{ log.NetworkAvailability }}
          </v-col>
          <v-col cols="2">
            {{ log.Timestamp }}
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
    height: 100vh; /* Span entire viewport height */
    background-color: rgb(239, 244, 246)
  }

  .inner-container-1{
    background-color: white;
    position: relative; /* To position the label */
    height: 720px;
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
    margin: 0; /* Remove margin to prevent any unwanted spacing */
  }

  .logo {
    width: 80px; /* Adjust the width of the logo */
    height: auto;
    margin: 0; /* Remove margin to prevent any unwanted spacing */
  }

  .service-label {
    top: 5;
    left: 5;
    font-weight: bold;
    padding: 10px;
    font-size: 20px;
  }

  .row-with-border {
    border-bottom: 1px solid black; /* Add border to the bottom of each row */
    margin-bottom: -1px; /* Offset the margin for better alignment */
  }

  .row-logo {
    width: 10px; /* Adjust the width of the row logo */
    height: auto;
    margin: 5px; /* Add margin between row logos */
  }
  </style>
  