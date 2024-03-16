<script setup>
    import Sidebar from "@/components/Navbar/Sidebar.vue";
    import Auth from '../utils/auth'
</script>
<template>
    <Sidebar/>
    <v-container fluid class="top-container">
      <img src="../assets/logo.png" alt="Logo" class="logo" data-aos="fade-down">
      <span class="text-center bold headline" data-aos="fade-down">Server Logs</span>
    </v-container>
    <v-container fluid class="bottom-container">
      <v-container class="fluid inner-container-1">
        <v-row style="margin-bottom:18px" class="service-label" data-aos="fade-down">
          <v-col class="col-title">Infrastructure Name</v-col>
          <v-col class="col-title">Infrastructure Type</v-col>
          <v-col class="col-title">Health Status</v-col>
          <v-col class="col-title">LogDateTime</v-col>
        </v-row>
        <v-row v-if="!latestServerLogs.length" style="margin-bottom:18px" class="service-label justify-center" data-aos="fade-down">
          <v-progress-circular
            indeterminate
            color="teal-lighten-3"
            class="text-center"
          ></v-progress-circular>
        </v-row>
        <v-row class="row-with-border" v-for="(log, index) in latestServerLogs" :key="index" data-aos="fade-down">
          <v-col class="col-content">
            <v-btn @click="redirect(log.InfrastructureName)">{{ log.InfrastructureName }}</v-btn>
          </v-col>
          <v-col class="col-content">{{ log.InfrastructureType }}</v-col>
          
          <v-col class="col-content">
            <!-- Health Status Icon from healthStatus -->
            <img v-if="healthStatus[log.InfrastructureName] === 'Healthy'" src="../assets/healthy.png" alt="Healthy" class="row-logo" style="width: 15px; height: 15px; margin-top: 5px;">
            <img v-else-if="healthStatus[log.InfrastructureName] === 'Degraded'" src="../assets/degraded.png" alt="Degraded" class="row-logo" style="width: 15px; height: 15px; margin-top: 5px;">
            <img v-else src="../assets/unhealthy.png" alt="Unhealthy" class="row-logo" style="width: 15px; height: 15px; margin-top: 5px;">
          </v-col>
          
          <v-col class="col-content">{{ log.LogDateTime }}</v-col>
        </v-row>

        <v-row style="margin-top:38px; margin-left:70px">
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
      </v-container>
    </v-container>
</template>
  
<script>
import AOS from 'aos'
import 'aos/dist/aos.css'
import io from 'socket.io-client';

// Establish SocketIO connection
// const socket = io('http://52.138.212.155:8000/latestlogs');
const socket = io('http://52.138.212.155:8000/latestlogs');


socket.on('error', (error) => {
  console.error('SocketIO error:', error);
});

socket.on('disconnect', () => {
  console.log('SocketIO connection closed');
});

export default {
  data() {
    return {
      healthStatus: [],
      latestServerLogs: []
    }
  },
  async created() {
    try {
        const result = await Auth.checkState();
        if (result == null){
            this.$router.push('/login')
        }
    } catch (error) {
        console.error(error);
    }
  
    // configure socket to listen on created
    socket.on('connect', () => {
      console.log('SocketIO connection established');
    });

    console.log('Component mounted');
    socket.emit('serverlog')

    // Listen for the 'health_status' event
    socket.on('new_health_status', (data) => {
      try {
        // console.log('Received health_status event:', data);
        this.healthStatus = data.data;
        console.log('Received health_status logs:', this.healthStatus);
      } catch (error) {
        console.error('Error in health_status event listener:', error);
      }
    });

    socket.on('latest_server_logs', (data) => {
      try {
        // console.log('Received health_status event:', data);
        this.latestServerLogs = data.data.latest_server_logs;
        console.log('Received latest server logs:', this.latestServerLogs);
      } catch (error) {
        console.error('Error in latest_server_logs event listener:', error);
      }
    });

  },
  methods: {
    redirect(infrastructureName) {
      this.$router.push({ name: 'ViewEachServer', params: { infrastructureName: infrastructureName } });
    }
  },
  mounted() {
    AOS.init({
      duration: 1600,
    });
    AOS.refresh();
  }
};
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
    height: 750px;
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
    color: #9db9ae
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
    margin-bottom: 35px; /* Offset the margin for better alignment */
  }

  .row-logo {
    width: 15px; /* Adjust the width of the row logo */
    height: auto;
    margin: 5px; /* Add margin between row logos */
  }
</style>
../../utils/auth