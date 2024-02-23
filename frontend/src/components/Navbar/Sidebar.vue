<template>
    <div style="margin-top: 100px">
      <v-app-bar app color="#c5dad2" dark>
        <!-- Conditionally render the v-app-bar-nav-icon based on the screen size -->
        <v-app-bar-nav-icon v-if="isPhoneSize" @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
        &nbsp;
        <img src="../../assets/logo.png" style="height: 40px; opacity: 100%;" class="my-5">
        <v-toolbar-title class="font-weight-bold font-italic mx-0 text-h5">Analyst Avengers</v-toolbar-title>
        <v-spacer></v-spacer>
        <span class="mr-14">
            <v-btn text to="/dashboard">Dashboard</v-btn>
            |
            <v-btn text to="/viewall">View All</v-btn>
        </span>
        <button class="btn btn-none btn-sign-out mb-2 pr-4" @click="signOut">Sign out&nbsp;&nbsp;<v-icon>mdi-logout</v-icon></button>
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
  