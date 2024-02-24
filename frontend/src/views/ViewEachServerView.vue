<script setup>
    import Sidebar from "@/components/Navbar/Sidebar.vue";
</script>

<template>
    <Sidebar/>
    <div class="display">
        <v-container style="background-color:white, max-width: 800px; height:90vh" class="mb-6 mt-8" data-aos="fade-down">
            <v-row>
                <h2 style="color: #758d84; margin: 20px; margin-bottom: 40px; margin-top:150px">Server 1</h2>
            </v-row>
            <div style="margin: 8px;">
                <div style="background-color: #dddddd; padding: 10px; border: 1px solid black; border-bottom: none;">
                    <h3>Overview</h3>
                </div>
                <div style="background-color: #ececec; padding: 20px; border: 1px solid black; border-top: none;">
                    <v-row>
                        <v-col cols="3">
                            <strong>Status</strong>
                        </v-col>
                        <v-col cols="3">
                            <strong>IP Address</strong>
                        </v-col>
                        <v-col cols="3">
                            <strong>Country</strong>
                        </v-col>
                        <v-col cols="3">
                            <strong>Date/Time</strong>
                        </v-col>
                    </v-row>

                    <v-row>
                        <v-col>
                            <h4 style="color:rgb(193, 63, 63)">Unvailable</h4>
                        </v-col>
                        <v-col>
                            <p>192.168.1.100</p>
                        </v-col>
                        <v-col>
                            <p>Singapore</p>
                        </v-col>
                        <v-col>
                            <p>21st Jan, 09:08:12</p>
                        </v-col>
                    </v-row>  
                </div>
            </div>
            <div style="margin: 8px;margin-top: 60px">
                <div style="background-color: #dddddd; padding: 10px; border: 1px solid black; border-bottom: none;">
                    <h3>Error Log</h3>
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
                Return to Server Logs
            </v-btn>
            </v-row>
            
        </v-container>
    </div>
</template>

<script>
    import AOS from 'aos'
    import 'aos/dist/aos.css'
</script>

<style>
.display {
    display: flex;
    flex-direction: column; /* Stack items vertically */
    align-items: center;
    justify-content: center; /* Center items horizontally */
    height: 100vh; /* Span entire viewport height */
    background-color: rgb(239, 244, 246)
}

.buttonstyle {
    margin-left: auto;
    margin-right: auto;
    margin-top:50px;
}
</style>