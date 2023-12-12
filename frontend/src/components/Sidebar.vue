<template>
  <div class="row" style="height: 100vh;">
    <!-- Hamburger Icon and Sidebar -->
    <div class="hamburger-sidebar">
      <div class="hamburger-icon" @click="toggleSidebar">&#9776;</div>
      <nav :style="{ width: sidebarWidth }" class="pt-2 sidebar" v-show="isSidebarOpen">
        <ul class="list-group list-group-flush">
          <li class="list-group-item list-group-item-action py-2 ripple" style="background-color:#f0f0f0;">
            <router-link to="/" class="list-item-link" style="background-color:#f0f0f0;">All Status</router-link>
          </li>
          <li class="list-group-item list-group-item-action py-2 ripple" style="background-color:#f0f0f0;">
            <router-link to="/" class="list-item-link" >item 2</router-link>
          </li>
          <li class="list-group-item list-group-item-action py-2 ripple" style="background-color:#f0f0f0;">
            <router-link to="/" class="list-item-link">item 3</router-link>
          </li>
        </ul>
      </nav>
    </div>
    <!-- <h4 class="text-center">Analyst Avengers</h4> -->
  </div>
</template>

<script>
export default {
  data() {
    return {
      isSidebarOpen: false,
    };
  },
  computed: {
    sidebarWidth() {
      return this.isSidebarOpen ? "300px" : "0"; // Adjust the width as needed
    },
  },
  methods: {
    toggleSidebar() {
      this.isSidebarOpen = !this.isSidebarOpen;
    },
  },
};
</script>

<style scoped>
.hamburger-sidebar {
  display: flex;
}

.hamburger-icon {
  font-size: 24px;
  cursor: pointer;
  padding: 10px;
}

.sidebar {
  background-color: #f0f0f0; 
  overflow-x: hidden;
  transition: 0.5s;
}

.list-item-link {
  display: block;
  width: 100%;
  padding: 10px;
  background-color: #f0f0f0; 
  text-decoration: none;
  color: #333; 
}

.content {
  flex: 1;
  padding: 20px;
}
</style>
