
<!-- App.vue --> 

<template>
    <div style="margin-top:100px">
      <v-app-bar app color="#c5dad2" dark>
        <v-app-bar-nav-icon @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
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
    methods: {
      signOut() {
        try {
          Auth.signout()
          this.$router.push('/login')
        } catch (error) {
          console.error(error.message)
        }
      },
    },
  };
</script>
  
   