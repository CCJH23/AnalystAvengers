<!-- Register page for users to register for an account before entering the site -->
<template>
    <div class="background-container">
        <LoginNavbar />
        <div class="register-container">
        <h1>Register</h1>
        <!-- Registration form preventing default submission behavior -->
        <form @submit.prevent="handleRegister" class="needs-validation">
            <div class="form-group">
                <label for="email">Email</label>
                <input type="email" id="email" v-model="email" class="form-control" required>
            </div>
            <div class="form-group">
                <label for="password">Password</label>
                <input type="password" id="password" v-model="password" class="form-control" required>
            </div>
            <button type="submit" class="btn btn-primary">Register</button>
        </form>
    </div>
    </div>

</template>

<script>
import LoginNavbar from '../components/LoginNavbar.vue';
import Auth from '../utils/auth' // Importing the Auth utility for authentication functions

export default {
    components: {
        LoginNavbar,
    },
    data() {
        return {
            email: '',
            password: ''
        };
    },
    created() {
        // On component creation, check user's authentication state
        (async () => {
            const result = await Auth.checkState();
            if(result){
                this.$router.push('/') // If authenticated, redirect to the homepages
            }
        })();
    },
    methods: {
        async handleRegister(){
            // Handle registration with provided email and password
            try {
                await Auth.register(this.email, this.password)
                this.email = ''
                this.password = ''
                this.$router.push('/')
            } catch (error) {
                console.error("Registration error:", error.message)
            }
        },
        getCookie(name) {
            // Utility method to get a cookie by name
            const value = `; ${document.cookie}`;
            const parts = value.split(`; ${name}=`);
            
            if (parts.length === 2) {
                return parts.pop().split(';').shift();
            }
        },
    },
};
</script>

<style scoped>
.background-container {
  background: url('@/assets/bg.jpg') center center fixed;
  background-size: cover;
  position: absolute;
  width: 100%;
  height: 100%;
  overflow: hidden;
  margin: 0;
  padding: 0;
}

.register-container h1 {
  text-align: center;
  margin-bottom: 20px;
}
.register-container {
  max-width: 400px;
  margin: 10% auto; 
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 4px;
  background-color: rgba(255, 255, 255, 0.8); 
  color:black;
}

.form-group {
    margin-bottom: 20px;
}

label {
    display: block;
    font-weight: bold;
}

input[type="text"],
input[type="email"],
input[type="password"] {
    width: 100%;
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
