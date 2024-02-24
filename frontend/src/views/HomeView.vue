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
          <v-col class="col-title">Log Date Time</v-col>
          <v-col class="col-title">Server Availability</v-col>
          <v-col class="col-title">Server CPU Utilization</v-col>
          <v-col class="col-title">Server Disk Utilization</v-col>
          <v-col class="col-title">Server Memory Utilization</v-col>
          <v-col class="col-title">Server Network Availability</v-col>
        </v-row>
        <v-row class="row-with-border" v-for="(log, index) in latestServerLogs" :key="index" data-aos="fade-down">
          <v-col class="col-content"><v-btn @click="redirect(server.serverId)">{{ log.InfrastructureName }}</v-btn></v-col>
          <v-col class="col-content">{{ log.InfrastructureType }}</v-col>
          <v-col class="col-content">{{ log.LogDateTime }}</v-col>
          <v-col class="col-content">{{ log.ServerAvailability }}</v-col>
          <v-col class="col-content">{{ (parseFloat(log.ServerCpuUtilisation)).toFixed(5) }}%</v-col>
          <v-col class="col-content">{{ (parseFloat(log.ServerDiskUtilisation)).toFixed(5) }}%</v-col>
          <v-col class="col-content">{{ (parseFloat(log.ServerMemoryUtilisation)).toFixed(5) }}%</v-col>
          <v-col class="col-content">{{ log.ServerNetworkAvailability }}</v-col>
        </v-row>
        <v-row style="margin-top:38px; margin-left:70px">
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
</template>
  
<script>
import AOS from 'aos'
import 'aos/dist/aos.css'
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

export default {
  async created() {
    try {
        const result = await Auth.checkState();
        if (result == null){
            this.$router.push('/login')
        }
    } catch (error) {
        console.error(error);
    }
  },
  data() {
    return {
      rowLabels: [
        "UBS Website",
        "UBS Trading Platform",
        "UBS Intranet",
        "UBS Wealth Management Platform",
        "UBS Mobile Banking App",
        "UBS Online Banking Platform",
        "UBS Financial Advisor Platform"
      ],
      hasUnhealthyLogo: false,
    };
  },
  methods: {
        redirect(serverId){
            console.log(serverId)
            this.$store.dispatch('loadedServer', serverId)
            this.$router.push('/SearchAllPets/'+ serverId)
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
