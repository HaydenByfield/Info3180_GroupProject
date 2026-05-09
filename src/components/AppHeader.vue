<template>
  <header>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary fixed-top">
      <div class="container">
        <a class="navbar-brand" href="/">Dating App</a>
        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarSupportedContent"
          aria-controls="navbarSupportedContent"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
          <ul class="navbar-nav ms-auto">
            <li class="nav-item">
              <RouterLink class="nav-link" to="/dashboard">Dashboard</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink class="nav-link" to="/matches">Matches</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink class="nav-link" to="/messages">Messages</RouterLink>
            </li>
            <li class="nav-item">
              <button type="button" class="nav-link btn btn-link" @click="handleLogout">Logout</button>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  </header>
</template>

<script setup>
import { RouterLink, useRouter } from "vue-router";

const router = useRouter();

async function handleLogout() {
  try {
    const csrfResponse = await fetch("/api/csrf-token");
    const csrfData = await csrfResponse.json();
    const csrfToken = csrfData.csrf_token;
    console.log("CSRF Token:", csrfToken);

    const response = await fetch("/api/logout", {
      method: "POST",
      headers: {
        "X-CSRFToken": csrfToken
      }
    });

    if (response.ok) {
      router.push("/login");
    }
  } catch (error) {
    console.error(error);
  }
}
</script>

<style>
/* Add any component specific styles here */
</style>
