<template>
  <div class="container">
    <form class="mt-3" @submit.prevent="handleRegister">
      <div class="mb-3">
        <label for="exampleInputEmail1" class="form-label">Email address</label>
        <input type="email" class="form-control" id="exampleInputEmail1" v-model="email" aria-describedby="emailHelp">
      </div>
      <div class="mb-3">
        <label for="exampleInputPassword1" class="form-label">Password</label>
        <input type="password" class="form-control" v-model="password" id="exampleInputPassword1">
      </div>
      <button type="submit" class="btn btn-primary">Submit</button>
  </form>
  </div>
</template>

<script>
  import Auth from '../../utils/auth'
  export default {
    data(){
      return {
        email: "",
        password: ""
      }
    },
    methods: {
      async handleRegister(){
        try {
            const user = await Auth.register(this.email, this.password)
            console.log("User registered:", user)
            this.email = ''
            this.password = ''
        } catch (error) {
            console.error("Registration error:", error.message)
        }
      }
    }
  }
</script>

<style scoped>

</style>