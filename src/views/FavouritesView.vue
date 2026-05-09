<script setup>
import { onMounted, ref } from "vue";
import ProfileCard from "@/components/ProfileCard.vue";

const favourites = ref([]);
const isLoading = ref(false);
const errorMessage = ref("");
const csrfToken = ref("");

function normaliseFavourite(favourite) {
  return {
    id: favourite.id,
    username: favourite.username || favourite.name || `Favourite User #${favourite.id}`,
    age: favourite.age || "N/A",
    location: favourite.location || "Location not provided",
    bio: favourite.bio || "No bio added yet.",
    interests: favourite.interests || [],
    photo: favourite.photo || null
  };
}

async function getCsrfToken() {
  if (csrfToken.value) return csrfToken.value;

  const response = await fetch("/api/csrf-token", {
    credentials: "include"
  });

  if (!response.ok) {
    throw new Error("Unable to get CSRF token.");
  }

  const data = await response.json();
  csrfToken.value = data.csrf_token;

  return csrfToken.value;
}

async function loadFavourites() {
  isLoading.value = true;
  errorMessage.value = "";

  try {
    const token = await getCsrfToken();
    const response = await fetch("/api/favourite", {
      credentials: "include",
      headers: {
        "X-CSRFToken": token
      }
    });

    if (!response.ok) {
      throw new Error("Unable to load favourites.");
    }

    const data = await response.json();
    favourites.value = (data.favourite || []).map(normaliseFavourite);
  } catch (error) {
    console.error(error);
    errorMessage.value = error.message || "Unable to load favourites.";
  } finally {
    isLoading.value = false;
  }
}

onMounted(loadFavourites);
</script>

<template>
  <main class="favourites-page">
    <section class="favourites-header">
      <div>
        <h1>Your Favourites</h1>
        <p>Profiles you saved from your suggested matches.</p>
      </div>

      <button type="button" class="refresh-btn" @click="loadFavourites">
        Refresh
      </button>
    </section>

    <section v-if="isLoading" class="status-box">
      <p>Loading favourites...</p>
    </section>

    <section v-else-if="errorMessage" class="empty">
      <h2>{{ errorMessage }}</h2>
      <p>Please try refreshing the page.</p>
    </section>

    <section v-else-if="favourites.length" class="favourites-grid">
      <ProfileCard
        v-for="favourite in favourites"
        :key="favourite.id"
        :profile="favourite"
        :show-actions="false"
      />
    </section>

    <section v-else class="empty">
      <h2>No favourites yet</h2>
      <p>Save profiles from the dashboard and they will appear here.</p>
    </section>
  </main>
</template>

<style scoped>
.favourites-page {
  width: min(1100px, 92%);
  margin: 0 auto;
  padding: 2rem 0;
}

.favourites-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.favourites-header h1 {
  font-size: 2.2rem;
  margin: 0 0 0.4rem;
  color: #222;
}

.favourites-header p {
  color: #555;
  margin: 0;
  max-width: 650px;
}

.refresh-btn {
  border: none;
  border-radius: 10px;
  background: #e75480;
  color: #fff;
  font-weight: 700;
  padding: 0.75rem 1.1rem;
  cursor: pointer;
}

.refresh-btn:hover {
  background: #d94270;
}

.favourites-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.25rem;
}

.status-box {
  padding: 0.9rem 1rem;
  border-radius: 10px;
  margin-bottom: 1rem;
  background: #f5f5f5;
  color: #444;
}

.status-box p {
  margin: 0;
}

.empty {
  text-align: center;
  padding: 3rem 1rem;
  background: #fafafa;
  border-radius: 16px;
}

.empty h2 {
  margin-bottom: 0.5rem;
}

.empty p {
  color: #555;
  margin: 0;
}

@media (max-width: 900px) {
  .favourites-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 640px) {
  .favourites-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .refresh-btn {
    width: 100%;
  }

  .favourites-grid {
    grid-template-columns: 1fr;
  }
}
</style>
