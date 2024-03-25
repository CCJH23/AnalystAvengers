<!-- Sidebar component to be included at the top of each page after the user has logged in -->
<template>
      <v-app-bar app color="#c5dad2" dark style="margin-bottom: 140px;">
        <!-- logo -->
        <img src="../assets/logo.png" style="height: 30px; opacity: 100%; margin-left: 15px; margin-right:3px;" class="my-5" @click="navigateToViewAll">

        <v-toolbar-title class="mx-0 text-h6 header" @click="navigateToViewAll">
          <span style="font-weight: normal">ANALYST</span> <span style="font-style: normal; font-weight: bold;">AVENGERS</span>
        </v-toolbar-title>
        
        <v-spacer></v-spacer>
        <button class="btn btn-none btn-sign-out pr-4" @click="signOut"><v-icon>mdi-logout</v-icon>&nbsp;Sign out</button>
      </v-app-bar>
  </template>
  
  <script>
  import Auth from '../utils/auth'
  
  export default {
    data() {
      return {
        drawer: false,
        mini: false,
        clipped: false,
      };
    },
    methods: {
      signOut() {
        try {
          Auth.signout()
          this.$router.push('/login')
        } catch (error) {
          console.error(error.message)
        }
      },
      navigateToViewAll() {
        this.$router.push('/');
      }
    },
  };
  </script>
  
  <style scoped>
  .header {
    cursor: pointer;
  }
  </style>