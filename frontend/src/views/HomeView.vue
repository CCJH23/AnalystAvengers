<script setup>
    import Sidebar from "../components/Navbar/Sidebar.vue";
    import Auth from '../utils/auth'
</script>

<style>
  /* Your existing styles */
</style>

<template>
  <div>
    <Sidebar />
    <div class="container-flex p-3" style="margin-left:4.5rem;">
      <div class="row px-3 pt-2 pb-4">
        <div class="col-md-7 col-sm-auto" data-aos="fade-down">
          <h3 class="pt-3 ps-3">Welcome back,</h3>
          <h5 class="pt-1 ps-3">track your tools today</h5>
        </div>
      </div>
      <hr />
      <div class="px-3 py-2" data-aos="fade-down">
        <h3 class="ps-3">Monitoring Dashboard</h3>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  async created() {
    try {
        const result = await Auth.checkState();
        if (result == null){
            this.$router.push('/login')
        }
    } catch (error) {
        console.error(error);
    }
  },
};
</script>