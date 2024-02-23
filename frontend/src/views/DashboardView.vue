<script setup>
    import Sidebar from "@/components/Navbar/Sidebar.vue";
    import PieChart from "@/components/PieChart.vue";
    import Map from "@/components/Map.vue"
</script>

<template>
    <Sidebar/>
    <div class="mx-6 mt-6" style="background-color: rgb(239, 244, 246)" data-aos="fade-down">
        <v-row>
            <v-col class="mini-container" cols="2.5" data-aos="fade-down">
                <!-- First Mini Column -->
                <span class="mini-container-header">Uptime</span>
                <span class="mini-container-content1">99.99%</span>
                <span class="mini-container-content2">Monitoring frequency: <span class="highlight-text">continuously</span></span>
            </v-col>
            <v-col class="mini-container" cols="2.5" data-aos="fade-down">
                <!-- Second Mini Column -->
                <span class="mini-container-header">Average CPU Usage</span>
                <span class="mini-container-content1">20%</span>
                <span class="mini-container-content2">Monitoring frequency: <span class="highlight-text">every 5 min</span></span>
            </v-col>
            <v-col class="mini-container" cols="2.5" data-aos="fade-down">
                <!-- Third Mini Column -->
                <span class="mini-container-header">Average Memory Usage</span>
                <span class="mini-container-content1">40%</span>
                <span class="mini-container-content2">Monitoring frequency: <span class="highlight-text">every 5 min</span></span>
            </v-col>
            <v-col class="mini-container" cols="2.5" data-aos="fade-down">
                <!-- Fourth Mini Column -->
                <span class="mini-container-header">Average Network Throughput</span>
                <span class="mini-container-content1">40%</span>
                <span class="mini-container-content2">Monitoring frequency: <span class="highlight-text">every hour</span></span>
            </v-col>
        </v-row>
        <v-row>
            <v-col class="mini-container-geo" cols="8" data-aos="fade-down">
              <!-- First Mini Column -->
              <span class="mini-container-header" style="position: absolute; top: 10px;">Geo Map</span>
              <Map/>
              <v-row>
              </v-row>
              <span class="mini-container-content3" style="position: absolute; top: 80px;">
                <!-- Adjusted position for the dropdown menu -->
                <v-menu>
                    <template v-slot:activator="{ props }">
                        <v-btn
                            color="#a7c6ba"
                            v-bind="props"
                            class="button-with-padding"
                            style="padding-right:21px"
                        >
                            Service
                            <v-icon large right size="24">mdi-menu-down</v-icon>
                        </v-btn>
                    </template>
                    <v-list>
                      <v-list-item
                        v-for="(item, index) in serviceItems"
                        :key="index"
                        :value="index"
                      >
                            <v-list-item-title>{{ item.title }}</v-list-item-title>
                        </v-list-item>
                    </v-list>
                </v-menu>
                </span>
                <span class="mini-container-content4" style="position: absolute; top: 30px;">
                  <!-- Adjusted position for the Countries dropdown menu -->
                  <v-menu style="margin-bottom:200px">
                      <template v-slot:activator="{ props }">
                          <v-btn
                              color="#a7c6ba"
                              v-bind="props"
                              class="button-with-padding"
                          >
                              Country
                              <v-icon large right size="24">mdi-menu-down</v-icon>
                          </v-btn>
                      </template>
                      <v-list>
                          <v-list-item
                            v-for="(item, index) in countryItems"
                            :key="index"
                            :value="index"
                          >
                              <v-list-item-title>{{ item.title }}</v-list-item-title>
                          </v-list-item>
                      </v-list>
                  </v-menu>
                  </span>
            </v-col>

            <v-col class="mini-container-usage" cols="3.5" data-aos="fade-down">
                <!-- First Mini Column -->
                <span class="mini-container-header">Device Usage</span>
                <!-- Start of Device Usage dropdown -->
                <v-row>
                  
                </v-row>
                <span class="mini-container-content3" style="position: absolute; top: 80px;">
                  <!-- Adjusted position for the dropdown menu -->
                  <v-menu>
                      <template v-slot:activator="{ props }">
                          <v-btn
                              color="#a7c6ba"
                              v-bind="props"
                              class="button-with-padding"
                              style="padding-right:21px"
                          >
                              Service
                              <v-icon large right size="24">mdi-menu-down</v-icon>
                          </v-btn>
                      </template>
                      <v-list>
                          <v-list-item
                          v-for="(item, index) in serviceItems"
                          :key="index"
                          :value="index"
                        >
                              <v-list-item-title>{{ item.title }}</v-list-item-title>
                          </v-list-item>
                      </v-list>
                  </v-menu>
                  </span>
        
                  <span class="mini-container-content4" style="position: absolute; top: 30px">
                      <v-menu>
                          <template v-slot:activator="{ props }">
                            <v-btn
                              color="#a7c6ba"
                              v-bind="props"
                              class="button-with-padding"
                            >
                              Country
                              <v-icon large right size="24">mdi-menu-down</v-icon>
                            </v-btn>
                          </template>
                          <v-list>
                            <v-list-item
                              v-for="(item, index) in countryItems"
                              :key="index"
                              :value="index"
                            >
                              <v-list-item-title>{{ item.title }}</v-list-item-title>
                            </v-list-item>
                          </v-list>
                        </v-menu>
                      </span>
                <!-- End of Device Usage dropdown -->
                <!-- <span style="margin-right:0px; padding-right:0px"> -->
                    <PieChart/>
                <!-- </span> -->
              </v-col>
          </v-row>
    </div>
</template> 

<style>
.mini-container {
    position: relative;
    margin-bottom: 40px;
    margin-left: 30px;
    margin-right: 30px;
    margin-top: 50px;
    height: 220px; /* Let the height adjust based on content */
    display: flex;
    flex-direction: column; /* Stack items vertically */
    justify-content: center; /* Align items vertically */
    align-items: center; /* Align items horizontally */
    border: 1px solid black; /* Add border for visualization */
    padding: 20px; /* Add padding for spacing */
}

.mini-container-usage {
  position: relative;
  margin-bottom: 40px;
  margin-left: 30px;
  margin-right: 30px;
  height: 220px; /* Let the height adjust based on content */
  display: flex;
  flex-direction: column; /* Stack items vertically */
  justify-content: center; /* Align items vertically */
  align-items: center; /* Align items horizontally */
  border: 1px solid black; /* Add border for visualization */
  padding: 20px; /* Add padding for spacing */
}

.mini-container-geo {
  position: relative;
  margin-bottom: 50px;
  margin-left: 30px;
  height: 650px; /* Set a fixed height */
  display: flex;
  flex-direction: column; /* Stack items vertically */
  justify-content: center; /* Align items vertically */
  align-items: center; /* Align items horizontally */
  border: 1px solid black; /* Add border for visualization */
  padding: 20px; /* Add padding for spacing */
  overflow: hidden; /* Hide overflow content if any */
}

.mini-container-header {
    color: #a7c6ba; /* Set color to specified value */
    text-align: left; /* Align text to the left */
    align-self: flex-start; /* Align the header to the start of its container */
    margin-bottom: auto; /* Push the header to the top */
    font-size: 20px; /* Increase font size */
    font-weight: bold; /* Set font weight to bold */
}

.mini-container-content1 {
    font-size: 70px;
}

.mini-container-content2 {
    margin-bottom: auto;
    padding-bottom:30px;
    font-size: 20px;
}

.mini-container-content3 {
    margin-bottom: 15px;
    font-size: 20px;
    align-self: flex-start;
    position: fixed;
}

.mini-container-content4 {
    margin-top: 120px;
    font-size: 20px;
    align-self: flex-start;
    position: fixed;
}

.highlight-text {
    color: #a7c6ba;
}

.dropdown-menu {
    position: relative;
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

<script>
  import AOS from 'aos'
  import 'aos/dist/aos.css'
  AOS.init({
    duration: 1600,
  })
  AOS.refresh()
  export default {
    data: () => ({
      serviceItems: [
        { title: 'UBS Website' },
        { title: 'UBS Trading Platform' },
        { title: 'UBS Intranet' },
        { title: 'UBS Wealth Management Platform' },
        { title: 'UBS Mobile Banking App' },
        { title: 'UBS Online Banking Platform' },
        { title: 'UBS Financial Advisor Platform' }
      ],
      countryItems: [
        { title: 'China' },
        { title: 'India' },
        { title: 'APAC' },
        { title: 'Europe' },
        { title: 'Australia' }
      ],
    }),
  }
</script>
