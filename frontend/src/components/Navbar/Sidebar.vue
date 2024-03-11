<template>
    <div style="margin-bottom: 60px">
      <v-app-bar app color="#c5dad2" dark>
        <!-- Conditionally render the v-app-bar-nav-icon based on the screen size -->
        <v-app-bar-nav-icon v-if="isPhoneSize" @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
        &nbsp;
        <!-- Add click event handler to the logo -->
        <img src="../../assets/logo.png" style="height: 30px; opacity: 100%; margin-left: 15px; margin-right:3px;" class="my-5" @click="navigateToViewAll">
        <!-- Use inline styles for Analyst and Avengers -->
        <v-toolbar-title class="mx-0 text-h6" @click="navigateToViewAll">
          <span style="font-weight: normal">ANALYST</span> <span style="font-style: normal; font-weight: 300;">AVENGERS</span>
        </v-toolbar-title>
        <v-spacer></v-spacer>
        <span class="mr-14">
            <v-btn text to="/"><v-icon>mdi-home</v-icon>&nbsp;&nbsp;Home</v-btn>
            |
            <v-btn text to="/dashboard"><v-icon>mdi-view-dashboard</v-icon>&nbsp;&nbsp;Dashboard</v-btn>
        </span>
        <button class="btn btn-none btn-sign-out mb-2 pr-4" @click="signOut"><v-icon>mdi-logout</v-icon>&nbsp;Sign out</button>
      </v-app-bar>
    </div>
  </template>
  
  <script>
  import Auth from '../../utils/auth'
  
  export default {
    data() {
      return {
        drawer: false,
        mini: false,
        clipped: false,
      };
    },
    computed: {
      // Check if the screen size is phone-sized
      isPhoneSize() {
        return window.innerWidth <= 600;
      }
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
      handleResize() {
        // Toggle the drawer if the screen becomes phone-sized
        this.drawer = this.isPhoneSize;
      },
      navigateToViewAll() {
        // Navigate to the "/viewall" route
        this.$router.push('/viewall');
      }
    },
    mounted() {
      // Add event listener for window resize
      window.addEventListener('resize', this.handleResize);
      // Call handleResize initially to set the initial state
      this.handleResize();
    },
    beforeUnmount() {
      // Remove event listener when the component is destroyed
      window.removeEventListener('resize', this.handleResize);
    }
  };
  </script>
  