<script setup>
//Homeview displays the landing page for our app, DriftDater
//It provides entry points for new users to register/login
//Version 1 - Basic landing page
</script>

<template>
  <main class="home-page">
    <section class="hero-section">
      <div class="hero-content">
        <h1>Welcome to DriftDater</h1>
        <p>
          Create your profile, discover compatible matches, and connect with people
          who share your interests.
        </p>
        
        <!-- Navigation buttons route users to authentication pages. -->
        <div class="hero-actions">
          <RouterLink to="/register" class="btn primary">Get Started</RouterLink>
          <RouterLink to="/login" class="btn secondary">Login</RouterLink>
        </div>
      </div>
    </section>
  </main>
</template>

<style scoped>
.home-page {
  min-height: 80vh;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Limits hero content width so the page remains readable on large screens. */
.hero-section {
  width: 100%;
  max-width: 900px;
  padding: 4rem 2rem;
  text-align: center;
}

.hero-content h1 {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.hero-content p {
  font-size: 1.1rem;
  color: #555;
  max-width: 600px;
  margin: 0 auto 2rem;
}

/* Keeps call-to-action buttons aligned with spacing between them. */
.hero-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
}

.btn {
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  text-decoration: none;
  font-weight: 600;
}

.primary {
  background-color: #e75480;
  color: white;
}

.secondary {
  border: 1px solid #e75480;
  color: #e75480;
}
</style>