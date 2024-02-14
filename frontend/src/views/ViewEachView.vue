<template>
    <Sidebar/>
    <v-container class="big-container">
        <v-menu>
            <template v-slot:activator="{ props }">
              <v-btn
                color="#a7c6ba"
                v-bind="props"
                class="button-with-padding"
                style="margin-top:15px;"
              >
                Service
                <v-icon large right size="24">mdi-menu-down</v-icon>
              </v-btn>
            </template>
            <v-list>
              <v-list-item
                v-for="(item, index) in items"
                :key="index"
                :value="index"
                @click="selectService(item.title)"
              >
                <v-list-item-title>{{ item.title }}</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-menu>
          <div class="dashboard-header" style="font-size: 27px; margin-bottom:150px; margin-top:40px">
            Performance Dashboard for <span style="color: #6d9d8a">{{ selectedService }}</span>
          </div>
          <div v-if="selectedService">
            <div v-for="infrastructure in selectedInfrastructure" :key="infrastructure" style="text-align: center;">
              <img :src="getImage(infrastructure)" :alt="infrastructure" style="margin-right: 20px;">
            </div>
          </div>
          <div class="status-text">
            <div style="margin-right:20px">
                <img src="../assets/healthy.png" alt="Logo" class="row-logo" style="width: 25px; height: 25px; "> Healthy
            </div>
            <div>
                <img src="../assets/degraded.png" alt="Logo" class="row-logo" style="width: 30px; height: 30px; "> Degraded
            </div>
            <div>
                <img src="../assets/unhealthy.png" alt="Logo" class="row-logo" style="width: 25px; height: 25px; "> Unhealthy
            </div>
        </div>
    </v-container>
</template>

<script setup>
  import { ref } from 'vue';
  import Sidebar from "@/components/Navbar/Sidebar.vue";

  const selectedService = ref('');
  const items = [
    { title: 'UBS Website' },
    { title: 'UBS Trading Platform' },
    { title: 'UBS Intranet' },
    { title: 'UBS Wealth Management Platform' },
    { title: 'UBS Mobile Banking App' },
    { title: 'UBS Online Banking Platform' },
    { title: 'UBS Financial Advisor Platform' },
  ];

  const infrastructureMapping = {
    'UBS Mobile Banking App': ['UBS Banking Server', 'UBS Banking Database', 'Authentication Service', 'Transaction Service', 'UBS Mobile Banking App'],
    // Add mappings for other services here
  };

  const selectedInfrastructure = ref([]);

  const selectService = (service) => {
    selectedService.value = service;
    selectedInfrastructure.value = infrastructureMapping[service] || [];
  }

  const getImage = (infrastructure) => {
    // Logic to determine the image based on infrastructure name
    if (infrastructure.includes('Server')) {
      return '../assets/app.png';
    } else if (infrastructure.includes('Database')) {
      return '../assets/database.png';
    } else if (infrastructure.includes('Service')) {
      return '../assets/service.png';
    } else if (infrastructure.includes('User')) {
      return '../assets/user.png';
    }
    // Add more conditions for other infrastructure types as needed
  }
</script>

<style>
.big-container{
    background-color: rgb(239, 244, 246);
    width: 800px; /* Set the desired width */
    height: 1000px; /* Set the desired height */
    overflow: auto;
    position: relative;
}

.dashboard-header {
    text-align: center;
    margin-top: 20px;
    font-size: 20px;
}

.status-text {
    position: absolute;
    bottom: 20px;
    right: 20px;
    text-align: right; /* Align text to the right */
    font-size:20px
}

.status-text div {
    margin-top: 10px; /* Add margin between each row */
}

.dropdown-menu {
    position: absolute;
    background-color: white; /* Set background color for dropdown menu */
    border: 1px solid black; /* Add border for dropdown menu */
    padding: 10px; /* Add padding for dropdown menu */
    top: 100%; /* Position dropdown menu below its parent */
    right: 0; /* Position dropdown menu on the right */
    z-index: 1; /* Ensure dropdown is above other content */
}

.dropdown-menu ul {
    list-style-type: none;
    padding: 0;
}

.dropdown-menu ul li {
    padding: 5px 0;
}

.button-with-padding .v-btn__content {
    padding-right: 30px; /* Adjust the padding as needed */
    padding-left: 30px; /* Adjust the padding as needed */
    text-align: center;
}
</style>
