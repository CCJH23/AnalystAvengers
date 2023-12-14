<template>
  <nav>
    <ul>
      <li><router-link to="/login">Login</router-link></li>
      <li><router-link to="/register">Register</router-link></li>
    </ul>
  </nav>
</template>

<script>
export default {
  name: 'LoginNavbar',
}
</script>

<style scoped>
nav {
  background-color: #f2f2f2;
  padding: 10px;
  position: relative;
  width: 100%;
}

ul {
  list-style-type: none;
  margin: 0;
  padding: 0;
}

li {
  display: inline;
  margin-right: 10px;
}

a {
  text-decoration: none;
  color: #333;
}
</style>
