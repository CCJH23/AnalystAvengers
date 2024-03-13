<template>
    <Sidebar/>
    <div class="display">
        <v-container style="background-color:white; padding-bottom: 10vh;" class="mb-6 mt-8" data-aos="fade-down" >
            <h2 style="color: #758d84; margin: 8px; margin-bottom: 40px; margin-top:60px">
                Name: {{ $route.params.infrastructureName }}
            </h2>
            <div style="margin: 8px;">
                <div style="background-color: #dddddd; padding: 10px; border: 1px solid black; border-bottom: none;">
                    <h3>Overview</h3>
                </div>
                <div style="background-color: #ececec; padding: 20px; border: 1px solid black; border-top: none;">
                    <v-row>
                        <v-col class="col-title">
                            <strong>Status</strong>
                        </v-col>
                        <v-col class="col-title">
                            <strong>Infrastructure Type</strong>
                        </v-col>
                        <v-col class="col-title">
                            <strong>Monitoring Tool</strong>
                        </v-col>
                        <v-col class="col-title">
                            <strong>Infrastructure Priority</strong>
                        </v-col>
                        <v-col class="col-title">
                            <strong>Infrastructure Country</strong>
                        </v-col>
                    </v-row>

                    <v-row>
                        <v-col class="col-content">
                            <img v-if="OverallHealthStatus == 'Healthy'" src="../assets/healthy.png" alt="Logo" class="row-logo" style="width: 15px; height: 15px; margin-top: 5px;">
                            <img v-else-if="OverallHealthStatus == 'Warning'" src="../assets/degraded.png" alt="Logo" class="row-logo" style="width: 15px; height: 15px; margin-top: 5px;">
                            <img v-else src="../assets/unhealthy.png" alt="Logo" class="row-logo" style="width: 15px; height: 15px; margin-top: 5px;">
                        </v-col>
                        <v-col class="col-content">
                            <p>{{ infrastructureType }}</p>
                        </v-col>
                        <v-col class="col-content">
                            <p>{{ monitoringTool }}</p>
                        </v-col>
                        <v-col class="col-content">
                            <p>{{ infrastructurePriority }}</p>
                        </v-col>
                        <v-col class="col-content">
                            <p>{{  infrastructureCountry }}</p>
                        </v-col>
                    </v-row>  
                </div>
            </div>
            <div style="margin: 8px;margin-top: 60px; ">
                <div style="background-color: #dddddd; padding: 10px; border: 1px solid black; border-bottom: none;">
                    <h3>Problems</h3>
                </div>

                <div style="background-color: #ececec; padding: 10px; border: 1px solid black; border-top: none;"> 
                    <!-- if  OverallHealthStatus == 'Healthy' , display string "Server is running as per expected" -->
                    <!-- else display 3 columns, Log Date Time, Problem Name, Problem Severity -->
                    <v-row v-if="OverallHealthStatus == 'Healthy'">
                        <v-col class="col-content">
                            <p>Infrastructure working as expected. No problem logs</p>
                        </v-col>
                    </v-row>
                    <v-row v-if="OverallHealthStatus != 'Healthy'">
                        <v-col cols="3" class="col-title">
                            <strong>Log Date Time</strong>
                        </v-col>
                        <v-col cols="6" class="col-title">
                            <strong>Problem Name</strong>
                        </v-col>
                        <v-col cols="3" class="col-title">
                            <strong>Problem Severity</strong>
                        </v-col>
                    </v-row>
                    <v-row v-if="OverallHealthStatus != 'Healthy'" class="row-with-border" v-for="(log, index) in problemLogs" :key="index">
                        <v-col cols="3" class="col-content">{{ log.LogDateTime }}</v-col>
                        <v-col cols="6" class="col-content">{{ log.ProblemName }}</v-col>
                        <v-col cols="3" class="col-content">{{ log.ProblemSeverity }}</v-col>
                    </v-row>
                </div>
            </div>

            <div style="margin: 8px;margin-top: 60px; ">
                <div style="background-color: #dddddd; padding: 10px; border: 1px solid black; border-bottom: none;">
                    <h3>Logs</h3>
                </div>
            
                <!-- Log Title Row -->
                <div style="background-color: #ececec; padding: 10px; border: 1px solid black; border-top: none; border-bottom: none;">
                    <v-row>
                        <v-col class="col-title">
                            <strong>Log Id</strong>
                        </v-col>
                        <v-col class="col-title">
                            <strong>Log Date</strong>
                        </v-col>
                        <v-col class="col-title">
                            <strong>ServerAvailability</strong>
                        </v-col>
                        <v-col class="col-title">
                            <strong>ServerCpuUtilisation</strong>
                        </v-col>
                        <v-col class="col-title">
                            <strong>ServerDiskUtilisation</strong>
                        </v-col>
                        <v-col class="col-title">
                            <strong>ServerMemoryUtilisation</strong>
                        </v-col>
                        <v-col class="col-title">
                            <strong>ServerNetworkAvailability</strong>
                        </v-col>
                    </v-row>
                </div>

                <!-- Log Data Rows with Scrollable Content -->
                <div style="background-color: #ececec; padding: 10px; border: 1px solid black; border-top: none; overflow-y: auto; height: 30vh; scrollbar-width: none;">
                    <v-row v-if="!historicalServerLogs.length" class="justify-center" style="margin-top: 5px;">
                        <v-progress-circular
                            indeterminate
                            color="teal-lighten-3"
                            class="text-center"
                        ></v-progress-circular>
                    </v-row>
                    <v-row v-for="(log, index) in historicalServerLogs.slice(-20).reverse()" :key="index">
                        <v-col class="col-content">
                            <p>{{ log.Id }}</p>
                        </v-col>
                        <v-col class="col-content">
                            <p>{{ log.LogDateTime }}</p>
                        </v-col>
                        <v-col class="col-content">
                            <p>{{ log.ServerAvailability }}</p>
                        </v-col>
                        <v-col class="col-content">
                            <p>{{ (parseFloat(log.ServerCpuUtilisation)).toFixed(3) }}%</p>
                        </v-col>
                        <v-col class="col-content">
                            <p>{{ (parseFloat(log.ServerDiskUtilisation)).toFixed(3) }}%</p>
                        </v-col>
                        <v-col class="col-content">
                            <p>{{ (parseFloat(log.ServerMemoryUtilisation)).toFixed(3) }}%</p>
                        </v-col>
                        <v-col class="col-content">
                            <p>{{ log.ServerNetworkAvailability }}</p>
                        </v-col>
                    </v-row>  
                </div>
            </div>
            <v-row>
                <v-btn
                color="#c5dad2"
                class="buttonstyle"
                dark
                absolute
                bottom
                @click="$router.push('/')"
                >
                Return to Health Status Page    
            </v-btn>
            </v-row>
            
        </v-container>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import AOS from 'aos';
import 'aos/dist/aos.css';
import { useRoute } from 'vue-router';
import axios from 'axios';
import io from 'socket.io-client';
import Sidebar from "@/components/Navbar/Sidebar.vue";

const route = useRoute();
const infrastructureName = ref('');
const infrastructureCountry = ref('');
const infrastructurePriority = ref(0);
const infrastructureType = ref('');
const monitoringTool = ref('');
const historicalServerLogs = ref([]);
const healthStatus = ref([]);
const OverallHealthStatus = ref('');
const problemLogs = ref([]);

// Establish SocketIO connection
const socket = io('http://52.138.212.155:8000/latestlogs');
  
socket.on('connect', () => {
    console.log('SocketIO connection established');
});

// Listen for the 'historical_server_logs' event
socket.on('historical_server_logs', (data) => {
    try {
        // console.log('Received historical_server_logs event:', data);  
        const filteredLogs = data.data.historical_server_logs.filter(log => log.InfrastructureName === infrastructureName.value);
        // console.log('Filtered historical_server_logs:', filteredLogs);
        historicalServerLogs.value = filteredLogs;
        // console.log('Filtered historical_server_logs:', historicalServerLogs.value);
    } catch (error) {
        console.error('Error in historical_server_logs event listener:', error);
    }
});

// Listen for the 'health_status' event
socket.on('health_status', (data) => {
    try {
        console.log('Received health_status event:', data);
        // Filter health status based on infrastructureName
        const filteredHealthStatus = data.data.filter(item => item.InfrastructureName === infrastructureName.value);
        healthStatus.value = filteredHealthStatus;
        console.log('Filtered health status:', healthStatus.value);
        OverallHealthStatus.value = healthStatus.value[0].OverallHealthStatus;
        console.log('OverallHealthStatus:', OverallHealthStatus.value);
    } catch (error) {
        console.error('Error in health_status event listener:', error);
    }
});


socket.on('problem_logs', (data) => {
    try {
        if (data && data.data && Array.isArray(data.data.problem_logs)) {
        const filteredProblemLogs = data.data.problem_logs
            .filter(log => log.InfrastructureName === infrastructureName.value)
            .sort((a, b) => new Date(b.LogDateTime) - new Date(a.LogDateTime));

        if (filteredProblemLogs.length > 0) {
            const latestLog = filteredProblemLogs[0];
            problemLogs.value = [latestLog];
        } else {
            problemLogs.value = [];
        }
        } else {
        console.error('Error: problem_logs event data is not in the expected format.');
        }
    } catch (error) {
        console.error('Error in problem_logs event listener:', error);
    }
    });


socket.on('error', (error) => {
    console.error('SocketIO error:', error);
});

socket.on('disconnect', () => {
    console.log('SocketIO connection closed');
});

onMounted(async () => {
    // get data from InfrastructureConfigTest table using infrastructureName
    infrastructureName.value = route.params.infrastructureName;
    try {
        const response = await axios.get(`http://52.138.212.155:8000/infrastructureconfig/infrastructure_config/${infrastructureName.value}`);
        const serverConfigData = response.data.data.server_configuration;
        infrastructureCountry.value = serverConfigData.InfrastructureCountry;
        infrastructurePriority.value = serverConfigData.InfrastructurePriority;
        infrastructureType.value = serverConfigData.InfrastructureType;
        monitoringTool.value = serverConfigData.MonitoringTool;
    } catch (error) {
        console.error('Error fetching infrastructure config:', error);
    }

    socket.emit('serverlog');
    AOS.init({
        duration: 1600,
    });
    AOS.refresh();
});
</script>

<style>
.display {
  display: flex;
  flex-direction: column; /* Stack items vertically */
  align-items: center;
  justify-content: center; /* Center items horizontally */
  height: 150vh; /* Span entire viewport height */
  background-color: rgb(239, 244, 246);
}

.buttonstyle {
  margin-left: auto;
  margin-right: auto;
  margin-top: 50px;
}

.inner-container-1{
    background-color: white;
    position: relative; /* To position the label */
    height: 750px;
    padding: 50px;
    margin: 20px 0; /* Add margin between service label and rows */
  }
</style>