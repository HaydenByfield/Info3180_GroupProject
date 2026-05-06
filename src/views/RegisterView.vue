<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router"; //imporing router for after registration

const router = useRouter();

const name = ref("");
const email = ref("");
const password = ref("");
const confirmPassword = ref("");
const errorMessage = ref("");

function handleRegister() {
  errorMessage.value = "";

  if (!name.value || !email.value || !password.value || !confirmPassword.value) {
    errorMessage.value = "Please fill out all fields.";
    return;
  }

  if (password.value !== confirmPassword.value) {
    errorMessage.value = "Passwords do not match.";
    return;
  }

  console.log("Registration submitted:", {
    name: name.value,
    email: email.value,
    password: password.value
  });

  //after a successful registration i want to send the user to a profile setup
  router.push("/profile/create");

}
</script>

<template>
  <main class="auth-page">
    <form class="auth-card" @submit.prevent="handleRegister">
      <h1>Create Account</h1>
      <p>Join DriftDater and start finding compatible matches.</p>

      <div class="form-group">
        <label for="name">Full Name</label>
        <input id="name" v-model="name" type="text" placeholder="Enter your full name" />
      </div>

      <div class="form-group">
        <label for="email">Email</label>
        <input id="email" v-model="email" type="email" placeholder="Enter your email" />
      </div>

      <div class="form-group">
        <label for="password">Password</label>
        <input id="password" v-model="password" type="password" placeholder="Create a password" />
      </div>

      <div class="form-group">
        <label for="confirmPassword">Confirm Password</label>
        <input
          id="confirmPassword"
          v-model="confirmPassword"
          type="password"
          placeholder="Confirm your password"
        />
      </div>

      <p v-if="errorMessage" class="error">{{ errorMessage }}</p>

      <button type="submit">Register</button>

      <p class="switch-link">
        Already have an account?
        <RouterLink to="/login">Login here</RouterLink>
      </p>
    </form>
  </main>
</template>

<style scoped>
.auth-page {
  min-height: 80vh;
  display: flex;
  align-items: center;
  justify-content: center;
}

.auth-card {
  width: 100%;
  max-width: 460px;
  padding: 2rem;
  border-radius: 12px;
  background: white;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
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