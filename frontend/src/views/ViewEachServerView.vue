<template>
    <Sidebar/>
    <div class="display">
        <v-container style="background-color:white, max-width: 800px; height:90vh" class="mb-6 mt-8" data-aos="fade-down">
            <h2 style="color: #758d84; margin: 8px; margin-bottom: 40px; margin-top:150px">
                Name: {{ $route.params.infrastructureName }}
            </h2>
            <div style="margin: 8px;">
                <div style="background-color: #dddddd; padding: 10px; border: 1px solid black; border-bottom: none;">
                    <h3>Overview</h3>
                </div>
                <div style="background-color: #ececec; padding: 20px; border: 1px solid black; border-top: none;">
                    <v-row>
                        <v-col>
                            <strong>Status</strong>
                        </v-col>
                        <v-col>
                            <strong>Infrastructure Type</strong>
                        </v-col>
                        <v-col>
                            <strong>Monitoring Tool</strong>
                        </v-col>
                        <v-col>
                            <strong>Infrastructure Priority</strong>
                        </v-col>
                        <v-col>
                            <strong>Infrastructure Country</strong>
                        </v-col>
                    </v-row>

                    <v-row>
                        <v-col>
                            <h4 style="color:rgb(193, 63, 63)">To edit</h4>
                        </v-col>
                        <v-col>
                            <p>{{ infrastructureType }}</p>
                        </v-col>
                        <v-col>
                            <p>{{ monitoringTool }}</p>
                        </v-col>
                        <v-col>
                            <p>{{ infrastructurePriority }}</p>
                        </v-col>
                        <v-col>
                            <p>{{  infrastructureCountry }}</p>
                        </v-col>
                    </v-row>  
                </div>
            </div>
            <div style="margin: 8px;margin-top: 60px">
                <div style="background-color: #dddddd; padding: 10px; border: 1px solid black; border-bottom: none;">
                    <h3>Logs</h3>
                </div>
            
                <div style="background-color: #ececec; padding: 20px; border: 1px solid black; border-top: none;">
                    <v-row>
                        <v-col cols="3">
                            <strong>Error Id</strong>
                        </v-col>
                        <v-col cols="3">
                            <strong>Error Type</strong>
                        </v-col>
                        <v-col cols="3">
                            <strong>Error Started</strong>
                        </v-col>
                        <v-col cols="3">
                            <strong>Error Resolved</strong>
                        </v-col>
                    </v-row>

                    <v-row>
                        <v-col>
                            <p>drs-error012910010</p>
                        </v-col>
                        <v-col>
                            <p>Network connectivity</p>
                        </v-col>
                        <v-col>
                            <p>21st Jan, 04:08:12</p>
                        </v-col>
                        <v-col>
                            <p>-</p>
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
import Sidebar from "@/components/Navbar/Sidebar.vue";
import { ref, onMounted } from 'vue';
import AOS from 'aos';
import 'aos/dist/aos.css';
import { useRoute } from 'vue-router';
import axios from 'axios';

const route = useRoute();
let infrastructureName = ref('');
let infrastructureCountry = ref('');
let infrastructurePriority = ref(0);
let infrastructureType = ref('');
let monitoringTool = ref('');

onMounted(() => {
    // get data from InfrastructureConfigTest table using infrastructureName
    infrastructureName = route.params.infrastructureName;

    axios.get(`http://localhost:8000/infrastructureconfig/infrastructure_config/${infrastructureName}/server`)
    .then(response => {
        const serverConfigData = response.data.data.server_configuration;
        infrastructureCountry.value = serverConfigData.InfrastructureCountry;
        infrastructurePriority.value = serverConfigData.InfrastructurePriority;
        infrastructureType.value = serverConfigData.InfrastructureType;
        monitoringTool.value = serverConfigData.MonitoringTool;
    })
    .catch(err => {
        console.log(err);
    }) 

//   infrastructureName.value = router.currentRoute.params.infrastructureName;
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
  height: 100vh; /* Span entire viewport height */
  background-color: rgb(239, 244, 246);
}

.buttonstyle {
  margin-left: auto;
  margin-right: auto;
  margin-top: 50px;
}
</style>