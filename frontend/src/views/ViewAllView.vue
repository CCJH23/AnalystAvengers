<template>
    <v-container style="background-color: #ececec" class="my-4">
        <v-row>
            <!-- Search bar (30% width) -->
            <v-col cols="4">
              <v-text-field v-model="searchKeyword" label="Search" outlined dense></v-text-field>
            </v-col>
      
            <!-- Filters (70% width) -->
            <v-col cols="8" class="d-flex justify-end">
                <!-- Add your filters here -->
                <v-select v-model="selectedStatusFilter" :items="statusFilterItems" label="Status" class="mr-3"></v-select>
                <!-- Country Filter -->
                <v-select v-model="selectedCountryFilter" :items="countryFilterItems" label="Country" class="mr-3"></v-select>
                <!-- Server Filter -->
                <v-select v-model="selectedServerFilter" :items="serverFilterItems" label="Server"></v-select>
            </v-col>
        </v-row>     
      <!-- Column Titles -->
      <hr class="my-4 mr-1 ml-15" style="border: 1px solid black;">
      <v-row>
        <!-- Checkbox column -->
        <!-- Column Titles -->
        <v-col cols="1"></v-col>
        <v-col v-for="(title, index) in columnTitles" :key="title" cols="1" class="mx-8">
          <v-card class="column-card" v-if="index > 0">
            <v-card-title class="text-center font-weight-bold green--text">{{ title }}</v-card-title>
          </v-card>
          <v-card class="column-card" v-else>
            <v-card-title class="text-center font-weight-bold green--text">{{ title }}</v-card-title>
          </v-card>
        </v-col>
      </v-row>
      <hr class="my-4 mr-1 ml-15" style="border: 1px solid black;">

  
      <!-- Fake Data Rows -->
      <v-row v-for="row in filteredRows" :key="row">
        <!-- Checkbox for each row -->
        <v-col cols="1">
          <v-checkbox v-model="selectedRows[row]" @click="updateSelectAll"></v-checkbox>
        </v-col>
        <!-- Fake Data for each column -->
        <v-col v-for="(title, index) in columnTitles" :key="title" cols="1" class="mx-8">
          <div class="data-card">
            <!-- eslint-disable vue/no-v-text-v-html-on-component -->
            <div class="text-center mt-4 fake-data">{{ generateFakeData(row, title) }}</div>
          </div>
        </v-col>
      </v-row>
    
    </v-container>
  </template>
  
  <script>
  export default {
    data() {
      return {
        columnTitles: ["Server", "Status", "Connection", "IP Address", "Product", "Country"],
        selectedRows: Array(10).fill(false), // Initialize with 10 rows
        selectAll: false,
        searchKeyword: '', 
        statusFilters: ["Available", "Down"],
        countryFilters: ["USA", "Canada", "Germany", "France", "Japan", "Australia", "Brazil", "India", "China"],
        serverFilters: ["Server1", "Server2", "Server3"],
        selectedStatusFilter: [],
        selectedCountryFilter: [],
        selectedServerFilter: [],
      };
    },
    computed: {
        statusFilterItems() {
            return ["", ...this.statusFilters];
        },
        countryFilterItems() {
            return ["", ...this.countryFilters];
        },
        serverFilterItems() {
            return ["", ...this.serverFilters];
        },
        filteredRows() {
            // Filter rows based on the search keyword
            return Array.from({ length: 10 }, (_, i) => i + 1).filter(row => {
                const rowData = this.columnTitles.map(title => this.generateFakeData(row, title)).join(' ');
                const statusFilterMatch = !this.selectedStatusFilter.length || (this.selectedStatusFilter.includes("Unselect All") || rowData.toLowerCase().includes(this.selectedStatusFilter.toLowerCase()));
                const countryFilterMatch = !this.selectedCountryFilter.length || (this.selectedCountryFilter.includes("Unselect All") || rowData.toLowerCase().includes(this.selectedCountryFilter.toLowerCase()));
                const serverFilterMatch = !this.selectedServerFilter.length || (this.selectedServerFilter.includes("Unselect All") || rowData.toLowerCase().includes(this.selectedServerFilter.toLowerCase()));
                return statusFilterMatch && countryFilterMatch && serverFilterMatch;
            });
        },
    },
    methods: {
        generateFakeData(row, columnTitle) {
            // Generate random "available" or "down" status for the "Status" column
                if (columnTitle === "Status") {
                    return (row % 2 === 0) ? "Available" : "Down";
                }

                // Generate Power data with alternating green and red icons
                if (columnTitle === "Power") {
                const isGreen = Math.random() < 0.5; // 50% chance of being green
                const powerIcon = isGreen ? "mdi-power" : "mdi-power-off";
                const iconColor = isGreen ? "green" : "red";
                return `<v-icon color="${iconColor}">${powerIcon}</v-icon>`;
                }

                // Generate random IP addresses for "IP Address" column
                if (columnTitle === "IP Address") {
                return `${Math.floor(Math.random() * 256)}.${Math.floor(Math.random() * 256)}.${Math.floor(Math.random() * 256)}.${Math.floor(Math.random() * 256)}`;
                }

                // Generate random countries for "Country" column
                const countryListings = [
                    "USA", "Canada", "Germany", "France", "Japan", "Australia", "Brazil", "India", "China"
                ];

                if (columnTitle === "Country") {
                    // Use modulo to cycle through the array based on the row number
                    const index = (row - 1) % countryListings.length;
                    return countryListings[index];
                }

                // Replace this with your logic to generate fake data based on the column title
                // For simplicity, using a placeholder value
                return `${columnTitle} Data`;
            
        },
      toggleSelectAll() {
        // Toggle selectAll value and update selectedRows accordingly
        this.selectAll = !this.selectAll;
        this.selectedRows.fill(this.selectAll);
      },
      updateSelectAll() {
        // Update selectAll value based on selectedRows
        this.selectAll = this.selectedRows.every((row) => row);
      },
    },
  };
  </script>
  
  <style>
  .column-card {
    height: 50px;
    width: 150px;
    margin-right: 20px;
    background-color: #c5dad2;
  }
  
  .data-card {
    width: 150px;
    margin-bottom: 20px;
  }
  
  .fake-data {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  
  .green--text {
    color: #2f5244;
  }
  </style>
  