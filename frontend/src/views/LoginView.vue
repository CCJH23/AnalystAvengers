<template>
  <div class="background-container">
    <LoginNavbar />
    <div class="login-container">
      <h1>Login</h1>
      <form @submit.prevent="register" class="needs-validation">
          <div class="form-group">
              <label for="username">Username</label>
              <input type="text" id="username" v-model="username" class="form-control" required>
          </div>
          <div class="form-group">
              <label for="password">Password</label>
              <input type="password" id="password" v-model="password" class="form-control" required>
          </div>
          <button type="submit" class="btn btn-primary">Login</button>
      </form>
    </div>
  </div>

</template>

<script>
  import LoginNavbar from '../components/LoginNavbar.vue';
  export default {
    components: {
      LoginNavbar,
    },
    data() {
      return {
        username: '',
        email: '',
        password: '',
      };
    },
    methods: {
      login() {
        // Perform registration logic here
        // You can make an API call to register the user
        // using the provided username, email, and password
        // Once the registration is successful, you can redirect the user to another page
      },
    },
  };
  
    // import axios from 'axios'
    // import { server } from "../utils/helper.js"

    // export default {
    //     name: 'LoginView',
    //     data() {
    //         return {
    //             userid: '',
    //             password: '',
    //             email: '',
    //             submitted: false,
    //             emailBlurred: false,
    //             passwordBlurred: false,
    //             // flag to prevent 2x output of data in console to reduce load
    //             isAuthenticating: false,
    //         }
    //     },
    //     methods: {
    //         authenticate() {
    //             if (this.isAuthenticating) {
    //                 return
    //             }

    //             this.isAuthenticating = true

    //             axios.post(`${server.baseURL}/login`, {
    //                 Email: this.email,
    //                 Password: this.password,
    //             })
    //             .then((response) => {
    //                 if (response.status === 200) {
    //                     const data = response.data.data
    //                     if (data.Access_Role === 4) {
    //                         sessionStorage.setItem('user', JSON.stringify(data))
    //                         this.$router.push({ name: 'HRHome' })
    //                     } else if (data.Access_Role === 2) {
    //                         sessionStorage.setItem('user', JSON.stringify(data));
    //                         this.$router.push({ name: 'StaffHome' })
    //                     }
    //                 } else if (response.status === 404) {
    //                     alert('Please enter valid credentials')
    //                 } else if (response.status === 401) {
    //                     if (response.data.message === "Incorrect password") {
    //                         alert("Please enter a valid password")
    //                     } else if (response.data.message === "Restricted Access") {
    //                         alert("Please select the correct access")
    //                     }
    //                 }
    //             })
    //             .catch((error) => {
    //                 console.error(error);
    //             });
    //         },
    //         validEmail(email) {
    //             return axios.post(`${server.baseURL}/validate-email`, { email })
    //                 .then((response) => {
    //                     return response.data.valid;
    //             })
    //                 .catch((error) => {
    //                     console.log(error);
    //                     return false;
    //             });
    //         },
    //         validPassword(password) {
    //             return axios.post(`${server.baseURL}/validate-password`, { password })
    //                 .then((response) => {
    //                     return response.data.valid;
    //                 })
    //                 .catch((error) => {
    //                     console.log(error);
    //                     return false;
    //                 });
    //         },
    //     }
    // }
</script>

<style scoped>
.background-container {
  /* Add your background image URL and additional styles */
  background: url('@/img/bg.jpg') center center fixed;
  background-size: cover;
  /* Add other background styles or overlay if needed */
  /* For example, you can add an overlay with opacity */
  position: absolute;
  width: 100%;
  height: 100%;
  overflow: hidden;
  margin: 0;
  padding: 0;
}

.login-container {
  max-width: 400px;
  margin: 10% auto; /* Adjust the margin to center the form vertically */
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 4px;
  background-color: rgba(255, 255, 255, 0.8); /* Adjust the opacity as needed */
  color:black;
}

.login-container h1 {
  text-align: center;
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  font-weight: bold;
  color:black;
}

input[type="text"],
input[type="email"],
input[type="password"] {
  width: calc(100% - 20px);
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

button[type="submit"] {
  padding: 10px 20px;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

</style>