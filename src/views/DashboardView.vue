<script setup>
import { onMounted, ref } from "vue";
import ProfileCard from "@/components/ProfileCard.vue";

const cards = ref([]);
const loading = ref(false);
const error = ref("");
const toast = ref("");

// temporary data for testing, swap out once /matches is ready
const mockData = [
  {
    id: 1,
    username: "Maya",
    age: 22,
    location: "Kingston",
    bio: "Coffee lover, beach walks, and live music.",
    interests: ["Music", "Travel", "Food"],
    imageUrl: "https://placehold.co/600x400?text=Maya"
  },
  {
    id: 2,
    username: "Andre",
    age: 24,
    location: "St. Andrew",
    bio: "Into fitness, movies, and weekend adventures.",
    interests: ["Fitness", "Movies", "Hiking"],
    imageUrl: "https://placehold.co/600x400?text=Andre"
  },
  {
    id: 3,
    username: "Leah",
    age: 23,
    location: "Portmore",
    interests: ["Art", "Food", "Travel"],
    imageUrl: "https://placehold.co/600x400?text=Leah"
  }
];

//helper function to help with displaying the profile info for user
function normalise(p) {
  return {
    id: p.id,
    username: p.username || p.name || "Unknown User",
    age: p.age || "N/A",
    location: p.location || "Location not provided",
    bio: p.bio || "No bio added yet.",
    interests: p.interests || [],
    imageUrl: p.imageUrl || p.profile_picture || "https://placehold.co/600x400?text=Profile"
  };
}

function loadProfiles() {
  loading.value = true;
  error.value = "";
  toast.value = "";

  setTimeout(() => {
    cards.value = mockData.map(normalise);
    loading.value = false;
  }, 400);
}

function onSwipe(id, action) {
  cards.value = cards.value.filter(p => p.id !== id);
  toast.value = action === "like" ? "Profile liked." : "Profile passed.";
}

function onFavourite(id) {
  toast.value = `Profile #${id} added to favourites.`;
}

onMounted(loadProfiles);
</script>

<template>
  <main class="dash">
    <section class="dash-header">
      <div>
        <h1>Discover Matches</h1>
        <p>Browse suggested profiles based on your preferences and shared interests.</p>
      </div>
      <button type="button" class="refresh-btn" @click="loadProfiles">Refresh</button>
    </section>

    <p v-if="toast" class="toast">{{ toast }}</p>
    <p v-if="error" class="err">{{ error }}</p>

    <section v-if="loading" class="status-box">
      <p>Loading suggested matches...</p>
    </section>

    <section v-else-if="cards.length" class="grid">
      <ProfileCard
        v-for="p in cards"
        :key="p.id"
        :profile="p"
        @interact="onSwipe"
        @favorite="onFavourite"
      />
    </section>

    <section v-else class="empty">
      <h2>No profiles available</h2>
      <p>Try refreshing later or updating your preferences.</p>
    </section>
  </main>
</template>

<style scoped>
.dash {
  width: min(1100px, 92%);
  margin: 0 auto;
  padding: 2rem 0;
}

.dash-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.dash-header h1 {
  font-size: 2.2rem;
  margin: 0 0 0.4rem;
}

.dash-header p {
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

.grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.25rem;
}

.toast,
.err,
.status-box {
  padding: 0.9rem 1rem;
  border-radius: 10px;
  margin-bottom: 1rem;
}

.toast {
  background: #fff0f5;
  color: #b93767;
}

.err {
  background: #fdecea;
  color: #b42318;
}

.status-box {
  background: #f5f5f5;
  color: #444;
}

.empty {
  text-align: center;
  padding: 3rem 1rem;
  background: #fafafa;
  border-radius: 16px;
}

.empty h2 { margin-bottom: 0.5rem; }
.empty p { color: #555; }

@media (max-width: 900px) {
  .grid { grid-template-columns: repeat(2, 1fr); }
}

@media (max-width: 640px) {
  .dash-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .refresh-btn { width: 100%; }
  .grid { grid-template-columns: 1fr; }
}
</style>