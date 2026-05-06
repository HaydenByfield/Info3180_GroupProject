<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import ProfileCard from "@/components/ProfileCard.vue";

const router = useRouter();

const matches = ref([
  {
    id: 1,
    username: "Alice Wonder",
    age: 25,
    location: "Kingston",
    bio: "Love hiking and adventure. Let's explore the world together.",
    interests: ["Hiking", "Travel", "Adventure"],
    imageUrl: "https://placehold.co/600x400?text=Alice"
  },
  {
    id: 2,
    username: "Emma",
    age: 23,
    location: "Montego Bay",
    bio: "Artist and creative soul. Let's create art together.",
    interests: ["Art", "Music", "Food"],
    imageUrl: "https://placehold.co/600x400?text=Emma"
  },
  {
    id: 3,
    username: "Noah",
    age: 26,
    location: "St. Andrew",
    bio: "Always looking for good coffee, live music, and weekend plans.",
    interests: ["Coffee", "Music", "Movies"],
    imageUrl: "https://placehold.co/600x400?text=Noah"
  }
]);

function openMessages(profileId) {
  console.log("Open messages for profile:", profileId);
  router.push("/messages");
}
</script>

<template>
  <main class="matches-page">
    <section class="matches-header">
      <div>
        <h1>Your Matches</h1>
        <p>People you matched with are ready for a conversation.</p>
      </div>
    </section>

    <section v-if="matches.length" class="matches-grid">
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
