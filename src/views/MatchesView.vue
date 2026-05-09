<script setup>
import { onMounted, ref } from "vue";
import { useRouter } from "vue-router";
import ProfileCard from "@/components/ProfileCard.vue";

const router = useRouter();

const matches = ref([]);
const isLoading = ref(false);
const errorMessage = ref("");

function normaliseMatch(match) {
  const id = match.id || match.user_id;

  return {
    id,
    username: match.username || match.name || `Matched User #${id}`,
    age: match.age || "N/A",
    location: match.location || "Location not provided",
    bio: match.bio || "No bio added yet.",
    interests: match.interests || [],
    photo: match.photo || null,
    imageUrl: match.imageUrl || null,
    chatroomId: match.chatroom_id || match.chatroomId || null
  };
}

async function loadMatches() {
  isLoading.value = true;
  errorMessage.value = "";

  try {
    const response = await fetch("/api/interact", {
      credentials: "include"
    });

    if (!response.ok) {
      throw new Error("Unable to load matches.");
    }

    const data = await response.json();
    matches.value = data.map(normaliseMatch);
  } catch (error) {
    console.error(error);
    errorMessage.value = error.message || "Unable to load matches.";
  } finally {
    isLoading.value = false;
  }
}

function openMessages(profileId) {
  console.log("Open messages for profile:", profileId);
  router.push("/messages");
}

onMounted(loadMatches);
</script>

<template>
  <main class="matches-page">
    <section class="matches-header">
      <div>
        <h1>Your Matches</h1>
        <p>People you matched with are ready for a conversation.</p>
      </div>
    </section>

    <section v-if="isLoading" class="empty">
      <h2>Loading matches...</h2>
    </section>

    <section v-else-if="errorMessage" class="empty">
      <h2>{{ errorMessage }}</h2>
    </section>

    <section v-else-if="matches.length" class="matches-grid">
      <ProfileCard
        v-for="match in matches"
        :key="match.id"
        :profile="match"
        :show-actions="false"
        :show-message-button="true"
        @message="openMessages"
      />
    </section>

    <section v-else class="empty">
      <h2>No matches yet</h2>
      <p>Keep discovering profiles and check back soon.</p>
    </section>
  </main>
</template>

<style scoped>
.matches-page {
  width: min(1100px, 92%);
  margin: 0 auto;
  padding: 2rem 0;
}

.matches-header {
  margin-bottom: 1.5rem;
}

.matches-header h1 {
  font-size: 2.2rem;
  margin: 0 0 0.4rem;
  color: #222;
}

.matches-header p {
  color: #555;
  margin: 0;
  max-width: 650px;
}

.matches-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.25rem;
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
}

@media (max-width: 900px) {
  .matches-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 640px) {
  .matches-grid {
    grid-template-columns: 1fr;
  }
}
</style>
