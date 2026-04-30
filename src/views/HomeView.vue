<script setup>
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