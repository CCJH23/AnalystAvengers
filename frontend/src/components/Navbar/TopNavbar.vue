<template>
    <nav class="navbar navbar-light d-flex topnav" style="position: sticky; z-index: 4; height: 80px;">
      <div class="d-flex justify-content-center">
        <img src="../../assets/logo.png" style="height: 100px; opacity: 100%;" class="p-0">
        <h3 class="pt-5 mr-2 font-italic fw-light fs-4">Analyst Avengers</h3> <!-- Adjusted the top padding, left padding, font weight, and font size -->
      </div>
      <div class="ml-auto">
        <button class="btn btn-none btn-sign-out pt-4 pr-4" @click="signOut">Sign out</button>
      </div>
    </nav>
  </template>
  
  <style>
  .topnav {
    background-color: #c5dad2;
  }
  
  /* Additional styles for font */
  .font-italic {
    font-style: italic;
  }
  
  .fw-light {
    font-weight: lighter;
  }
  
  .fs-4 {
    font-size: 1.5rem; /* Adjust the font size as needed */
  }
  
  .btn-sign-out {
    font-size: 1rem; /* Adjust the button font size */
    margin-top: 10px; /* Add top margin */
    margin-right: 10px; /* Add right margin */
  }
  </style>
  
  <script>
  export default {
    // Your component logic goes here
  }
  </script>
  