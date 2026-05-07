<template>
  <main class="auth-page">
    <form class="auth-card" @submit.prevent="handleLogin">
      <h1>Login</h1>
      <p>Welcome back to DriftDater.</p>

      <div class="form-group">
        <label for="email">Email</label>
        <input id="email" v-model="email" type="email" placeholder="Enter your email" />
      </div>

      <div class="form-group">
        <label for="password">Password</label>
        <input id="password" v-model="password" type="password" placeholder="Enter your password" />
      </div>

      <p v-if="errorMessage" class="error">{{ errorMessage }}</p>

      <button type="submit">Login</button>

      <p class="switch-link">
        Don't have an account?
        <RouterLink to="/register">Register here</RouterLink>
      </p>
    </form>
  </main>
</template>


<script setup>
import { ref } from "vue";
import { RouterLink, useRouter } from "vue-router";


const router = useRouter();
const email = ref("");
const password = ref("");
const errorMessage = ref("");
const message = ref("");

async function handleLogin() {
  errorMessage.value = "";

  if (!email.value || !password.value) {
    errorMessage.value = "Please enter both email and password.";
    return;
  }

  try{
    let response = await fetch('/api/login', {
      method: 'POST',
      header: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        email: email.value,
        password: password.value
      })
    })
    let data = await response.json()
    if(response.ok){
      message.value = data.message
      console.log(message)
      router.push("/dashboard");
    }
    if(!response.ok){
      errorMessage.value = "Response Error"
    }
  } catch(error){
    console.error
  }

  console.log("Login submitted:", {
    email: email.value,
    password: password.value
  });
}  
</script>
 


<style scoped>
.auth-page {
  min-height: 80vh;
  display: flex;
  align-items: center;
  justify-content: center;
}

.auth-card {
  width: 100%;
  max-width: 420px;
  padding: 2rem;
  border-radius: 12px;
  background: white;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.auth-card h1 {
  margin-bottom: 0.5rem;
}

.auth-card p {
  color: #555;
}

.form-group {
  margin-top: 1rem;
}

label {
  display: block;
  margin-bottom: 0.4rem;
  font-weight: 600;
}

input {
  width: 100%;
  padding: 0.7rem;
  border: 1px solid #ccc;
  border-radius: 8px;
}

button {
  width: 100%;
  margin-top: 1.5rem;
  padding: 0.8rem;
  border: none;
  border-radius: 8px;
  background-color: #e75480;
  color: white;
  font-weight: 600;
  cursor: pointer;
}

.error {
  color: #c0392b;
  margin-top: 1rem;
}

.switch-link {
  margin-top: 1rem;
  text-align: center;
}

</style>