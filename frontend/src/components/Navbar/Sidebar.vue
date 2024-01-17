<!-- App.vue -->

<template>
    <v-app>
      <!-- Navigation Drawer -->
      <v-navigation-drawer app :mini-variant="mini" :clipped="clipped" v-model="drawer">
        <!-- Your sidebar content goes here -->
        <v-list>
          <v-list-item link>
            <v-list-item-icon>
              <v-icon>mdi-view-dashboard</v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title>Dashboard</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
  
          <v-list-item link>
            <v-list-item-icon>
              <v-icon>mdi-list-status</v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title>View All</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
  
          <v-list-item link>
            <v-list-item-icon>
              <v-icon>mdi-logout</v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title>Sign Out</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-list>
      </v-navigation-drawer>
  
      <!-- App Bar -->
      <v-app-bar app color="#c5dad2" dark>
        <v-app-bar-nav-icon @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
        <!-- <img src="../../assets/logo.png" style="height: 100px; opacity: 100%;" class="mt-5"> -->
        <v-toolbar-title class="font-italic mx-0">Analyst Avengers</v-toolbar-title>
        <v-spacer></v-spacer>
        <span class="mr-14">
            <v-btn text to="/dashboard">Dashboard</v-btn>
            |
            <v-btn text to="/dashboard">View All</v-btn>
        </span>
        <button class="btn btn-none btn-sign-out mb-2 pr-4" @click="signOut">Sign out</button>
      </v-app-bar>
      
    </v-app>
  </template>
  
  <script>
  export default {
    data() {
      return {
        drawer: false,
        mini: false, // For mini variant
        clipped: false, // For clipped drawer
      };
    },
    methods: {
      signOut() {
        // Implement your sign-out logic
      },
    },
  };
  </script>
  
  <style>
  /* Add your custom styles here */
  </style>
  