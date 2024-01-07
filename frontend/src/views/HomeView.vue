<template>
  <div class="app-container">
    <!-- Hamburger button -->
    <button @click="toggleSidebar" class="hamburger">&#9776;</button>

    <!-- Sidebar -->
    <div :class="{ 'sidebar-collapsed': isSidebarCollapsed }" class="sidebar">
      <!-- Sidebar content goes here -->
      <ul>
        <li>Item 1</li>
        <li>Item 2</li>
        <li>Item 3</li>
      </ul>
    </div>

    <!-- Main content -->
    <div class="main-content">
      <!-- Main content goes here -->
      <p>This is the main content of your application.</p>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      isSidebarCollapsed: false,
    };
  },
  methods: {
    toggleSidebar() {
      this.isSidebarCollapsed = !this.isSidebarCollapsed;
    },
  },
};
</script>

<style scoped>
.app-container {
  display: flex;
  height: 100vh;
}

.hamburger {
  font-size: 20px;
  cursor: pointer;
}

.sidebar {
  width: 200px;
  background-color: #333;
  color: white;
  overflow: hidden;
  transition: width 0.3s;
}

.sidebar ul {
  list-style: none;
  padding: 0;
}

.sidebar li {
  padding: 10px;
  border-bottom: 1px solid #555;
}

.sidebar-collapsed {
  width: 60px;
}

.main-content {
  flex-grow: 1;
  padding: 20px;
}

@media screen and (max-width: 600px) {
  .sidebar {
    width: 0;
  }

  .sidebar-collapsed {
    width: 0;
  }

  .main-content {
    width: 100%;
  }
}
</style>
