<script setup>
    import Sidebar from "@/components/Navbar/Sidebar.vue";
</script>

<template>
    <Sidebar/>
    <v-container style="background-color: #ececec; max-width: 800px;" class="m-6">
        <v-row>
            <h2 style="color: #758d84; margin: 20px; margin-bottom: 40px">Server 1</h2>
        </v-row>
        <div style="margin: 8px;">
            <!-- Header Section -->
            <div style="background-color: #dddddd; padding: 10px; border: 1px solid black; border-bottom: none;">
                <h3>Overview</h3>
            </div>
        
            <!-- Content Section -->
            <div style="background-color: #ececec; padding: 20px; border: 1px solid black; border-top: none;">
                <v-row>
                    <!-- Status Column -->
                    <v-col cols="3">
                        <!-- Replace with actual status data -->
                        <strong>Status</strong>
                    </v-col>
                    <!-- IP Address Column -->
                    <v-col cols="3">
                        <!-- Replace with actual IP address data -->
                        <strong>IP Address</strong>
                    </v-col>
                    <!-- Country Column -->
                    <v-col cols="3">
                        <!-- Replace with actual country data -->
                        <strong>Country</strong>
                    </v-col>
                    <!-- Date/Time Column -->
                    <v-col cols="3">
                        <!-- Replace with actual date/time data -->
                        <strong>Date/Time</strong>
                    </v-col>
                </v-row>

                <v-row>
                    <v-col>
                        <!-- Replace with actual status data -->
                        <h4 style="color:rgb(193, 63, 63)">Unvailable</h4>
                    </v-col>
                    <!-- IP Address Column -->
                    <v-col>
                        <!-- Replace with actual IP address data -->
                        <p>192.168.1.100</p>
                    </v-col>
                    <!-- Country Column -->
                    <v-col>
                        <!-- Replace with actual country data -->
                        <p>Singapore</p>
                    </v-col>
                    <!-- Date/Time Column -->
                    <v-col>
                        <!-- Replace with actual date/time data -->
                        <p>21st Jan, 09:08:12</p>
                    </v-col>
                </v-row>  
            </div>
        </div>
        <div style="margin: 8px;margin-top: 60px">
            <!-- Header Section -->
            <div style="background-color: #dddddd; padding: 10px; border: 1px solid black; border-bottom: none;">
                <h3>Error Log</h3>
            </div>
        
            <!-- Content Section -->
            <div style="background-color: #ececec; padding: 20px; border: 1px solid black; border-top: none;">
                <v-row>
                    <v-col cols="3">
                        <!-- Replace with actual country data -->
                        <strong>Error Id</strong>
                    </v-col>
                    <!-- Status Column -->
                    <v-col cols="3">
                        <!-- Replace with actual status data -->
                        <strong>Error Type</strong>
                    </v-col>
                    <!-- IP Address Column -->
                    <v-col cols="3">
                        <!-- Replace with actual IP address data -->
                        <strong>Error Started</strong>
                    </v-col>
                    <!-- Date/Time Column -->
                    <v-col cols="3">
                        <!-- Replace with actual date/time data -->
                        <strong>Error Resolved</strong>
                    </v-col>
                </v-row>

                <v-row>
                    <v-col>
                        <!-- Replace with actual status data -->
                        <p>drs-error012910010</p>
                    </v-col>
                    <!-- IP Address Column -->
                    <v-col>
                        <!-- Replace with actual IP address data -->
                        <p>Network connectivity</p>
                    </v-col>
                    <!-- Country Column -->
                    <v-col>
                        <!-- Replace with actual country data -->
                        <p>21st Jan, 04:08:12</p>
                    </v-col>
                    <!-- Date/Time Column -->
                    <v-col>
                        <!-- Replace with actual date/time data -->
                        <p>-</p>
                    </v-col>
                </v-row>  
            </div>
        </div>
        <v-btn
            color="#c5dad2"
            dark
            absolute
            bottom
            right
            style="margin: 16px; margin-left: 555px; margin-top:50px"
            @click="$router.push('/viewall')"
            >
            Return to View All
        </v-btn>
        
    </v-container>



</template>