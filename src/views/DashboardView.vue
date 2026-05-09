<script setup>
import { computed, onMounted, ref } from "vue";
import ProfileCard from "@/components/ProfileCard.vue";
import { user } from "@/user/user.js";

const { currentUser, loadCurrentUser } = user();
loadCurrentUser();

const cards = ref([]);
const loading = ref(false);
const error = ref("");
const toast = ref("");
const csrfToken = ref("");
const fallbackUser = {
  username: "there",
  age: "N/A",
  location: "Location not provided",
  bio: "No bio added yet.",
  imageUrl: "https://placehold.co/300x300?text=Profile"
};
const displayUser = computed(() => currentUser.value || fallbackUser);

// temporary data for testing, swap out once /matches is ready
const mockData = [];

fetch("/api/matches")
  .then(response => response.ok ? response.json() : [])
  .then(data => {
    mockData.splice(0, mockData.length, ...data);
    console.log("Fetched matches:", mockData);
  })
  .catch(() => {
    mockData.splice(0, mockData.length);
  });

//helper function to help with displaying the profile info for user
function normalise(p) {
  return {
    id: p.id,
    username: p.username || p.name || "Unknown User",
    age: p.age || "N/A",
    location: p.location || "Location not provided",
    bio: p.bio || "No bio added yet.",
    interests: p.interests || [],
    photo: p.photo || null
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

async function getCsrfToken() {
  if (csrfToken.value) return csrfToken.value;

  const response = await fetch("/api/csrf-token", {
    credentials: "include"
  });
  const data = await response.json();
  csrfToken.value = data.csrf_token;

  return csrfToken.value;
}

async function onSwipe(id, action) {
  error.value = "";

  try {
    const token = await getCsrfToken();
    const response = await fetch("/api/interact", {
      method: "POST",
      credentials: "include",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": token
      },
      body: JSON.stringify({
        user_id: id,
        action
      })
    });

    if (!response.ok) {
      throw new Error("Unable to save interaction.");
    }

    cards.value = cards.value.filter(p => p.id !== id);
    toast.value = (action === "like" ? "Profile liked." : "Profile passed.");

  } catch (err) {
    console.error(err);
    error.value = "Could not save your interaction. Please try again.";
  }
}

async function onFavourite(id) {
  error.value = "";

  try {
    const token = await getCsrfToken();
    const response = await fetch("/api/favourite", {
      method: "POST",
      credentials: "include",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": token
      },
      body: JSON.stringify({
        user_id: id
      })
    });

    if (!response.ok) {
      throw new Error("Unable to add favourite.");
    }

    toast.value = `Profile #${id} added to favourites.`;
  } catch (err) {
    console.error(err);
    error.value = "Could not add this profile to favourites. Please try again.";
  }
}

onMounted(loadProfiles);
</script>

<template>
  <main class="dash">
    <section class="profile-summary">
      <img
        class="profile-summary-img"
        :src="displayUser.imageUrl"
        :alt="`${displayUser.username}'s profile photo`"
      >

      <div class="profile-summary-content">
        <h1>Welcome, {{ displayUser.username }}!</h1>
        <p><strong>Age:</strong> {{ displayUser.age }}</p>
        <p><strong>Location:</strong> {{ displayUser.location }}</p>
        <p><strong>Bio:</strong> {{ displayUser.bio }}</p>

        <!--needs to link to edit profile component!-->
        <RouterLink :to="{ name: 'edit-profile' }" class="edit-profile-btn">
          Edit Profile
        </RouterLink>
        
      </div>
    </section>

    <section class="dash-header">
      <div>
        <h1>Discover Matches</h1>
        <p>Browse suggested profiles based on your preferences and shared interests.</p>
      </div>
      <button type="button" class="refresh-btn" @click="loadProfiles">Refresh</button>
    </section>

    <p v-if="toast" class="toast show">{{ toast }}</p>
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

.profile-summary {
  display: grid;
  grid-template-columns: 180px 1fr;
  align-items: stretch;
  margin-bottom: 1.5rem;
  overflow: hidden;
  border-radius: 10px;
  background: #fff;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.profile-summary-img {
  width: 100%;
  height: 100%;
  min-height: 180px;
  object-fit: cover;
}

.profile-summary-content {
  padding: 1.5rem;
}

.profile-summary-content h1 {
  margin: 0 0 0.75rem;
  color: #222;
  font-size: 1.7rem;
}

.profile-summary-content p {
  margin: 0.25rem 0;
  color: #444;
}

.profile-summary-content strong {
  color: #222;
}

.edit-profile-btn {
  display: inline-block;
  width: auto;
  margin-top: 0.8rem;
  border: none;
  border-radius: 10px;
  background: #e75480;
  color: #fff;
  font-weight: 700;
  padding: 0.75rem 1.1rem;
  cursor: pointer;
  text-decoration: none;
}

.edit-profile-btn:hover {
  background: #d94270;
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
  .profile-summary {
    grid-template-columns: 1fr;
  }

  .profile-summary-img {
    width: 100%;
    height: 220px;
    min-height: 0;
  }

  .dash-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .refresh-btn { width: 100%; }
  .grid { grid-template-columns: 1fr; }
}
</style>
