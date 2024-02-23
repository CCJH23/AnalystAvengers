<script setup>
    import Sidebar from "@/components/Navbar/Sidebar.vue";
</script>
<template>
    <Sidebar/>
    <v-container fluid class="top-container">
      <img src="../assets/logo.png" alt="Logo" class="logo" data-aos="fade-down">
      <span class="text-center bold headline" :style="headlineStyle" data-aos="fade-down">{{ healthStatus }}</span>
    </v-container>
    <v-container fluid class="bottom-container">
      <v-container class="fluid inner-container-1">
        <v-row style="margin-bottom:18px" class="service-label" data-aos="fade-down">Service Health</v-row>
        <v-row class="row-with-border" data-aos="fade-down">
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
        <v-row class="row-with-border" v-for="(rowLabel, rowIndex) in rowLabels" :key="rowIndex" data-aos="fade-down">
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
          <v-col cols="2" v-for="(colIndex, index) in 5" :key="colIndex">
            <img v-if="index !== 3" src="../assets/healthy.png" alt="Healthy Logo" class="row-logo" />
            <img v-else src="../assets/unhealthy.png" alt="Unhealthy Logo" class="row-logo" @load="hasUnhealthyLogo = true" />
            <!-- <img src="../assets/degraded.png" alt="Degraded Logo" class="row-logo" @load="hasUnhealthyLogo = true"/> -->
          </v-col>
        </v-row>        
        <v-row style="margin-top:38px">
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
      ],
      hasUnhealthyLogo: false,
    };
  },
  computed: {
    healthStatus() {
      // Return appropriate status based on the condition
      return this.hasUnhealthyLogo ? "Hmm...something's not right" : "Everything looks good";
    },
    headlineStyle() {
      return this.healthStatus === "Everything looks good" ? { color: '#a7c6ba' } : { color: 'red' };
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
    height: 710px;
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
    font-weight: bold;
    text-align: center; /* Center align the text */
    margin: 0; /* Remove default margin */
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
    margin-bottom: -1px; /* Offset the margin for better alignment */
  }

  .row-logo {
    width: 15px; /* Adjust the width of the row logo */
    height: auto;
    margin: 5px; /* Add margin between row logos */
  }
</style>
