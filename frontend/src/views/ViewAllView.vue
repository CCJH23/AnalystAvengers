<script setup>
    import Sidebar from "@/components/Navbar/Sidebar.vue";
</script>
<template>
    <Sidebar/>
    <v-container fluid class="top-container">
      <img src="../assets/logo.png" alt="Logo" class="logo">
      <span class="text-center bold headline">Everything looks good</span>
    </v-container>
    <v-container fluid class="bottom-container">
      <v-container class="fluid inner-container-1">
        <v-row style="margin-bottom:18px" class="service-label">Service Health</v-row>
        <v-row class="row-with-border">
          <v-col cols="2"></v-col>
          <v-col cols="2">
            China
          </v-col>
          <v-col cols="2">
            APAC
          </v-col>
          <v-col cols="2">
            Europe
          </v-col>
          <v-col cols="2">
            Australia
          </v-col>
          <v-col cols="2">
            India
          </v-col>
        </v-row>
        <v-row class="row-with-border" v-for="(rowLabel, rowIndex) in rowLabels" :key="rowIndex">
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
          <v-col cols="2" v-for="colIndex in 5" :key="colIndex">
            <img src="../assets/logo.png" alt="Logo" class="row-logo">
          </v-col>
        </v-row>        
        <v-row style="margin-top:38px">
          <v-col cols="4">
          </v-col>
          <v-col>
            <img src="../assets/healthy.png" alt="Logo" class="row-logo" style="width: 15px; height: 15px; margin-top: 5px;">
            <span>Healthy</span>
          </v-col>          
          <v-col>
            <img src="../assets/degraded.jpeg" alt="Logo" class="row-logo" style="width: 15px; height: 15px;">Degraded
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
export default {
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
      ]
    };
  }
};
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
    background-color: rgb(239, 234, 234);
    display: flex;
    flex-direction: column; /* Stack items vertically */
    align-items: center;
    height: 100vh; /* Span entire viewport height */
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
