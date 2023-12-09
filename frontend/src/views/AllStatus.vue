<template>
  <div>
      <div class="row">
        <div class="col-2">
          <Sidebar></Sidebar>
        </div>
        <div class="col px-0">
          <Header></Header>
          <h1 class="p-4">Home Page</h1>
        </div>
      </div>
  </div>
</template>

<script>
  import Sidebar from '../components/Sidebar.vue'
  import Header from '../components/Header.vue'
  export default {
    components: {
      Sidebar,
      Header
    }
  }
</script>

<style scoped>

</style>