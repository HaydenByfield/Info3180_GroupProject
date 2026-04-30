<script setup>
/*ProfileCard is a reusable display card for user profiles.

  It is used to show suggested matches on the dashboard and can also be reused
  later for search results, favourites, or matched users.

  Parent components should pass in a profile object and listen for:
  - interact: emitted when the user clicks Like or Pass
  - favorite: emitted when the user clicks Favorite

  Version 1 (April 30, 2026)
*/

const props = defineProps({
  profile: {
    type: Object,
    required: true
  }
});

const emit = defineEmits(["interact", "favorite"]);

// Fallback image used when the backend does not return a profile picture.
const defaultProfileImage = "https://placehold.co/600x400?text=Profile";

/*
  Returns the best available display name.

  The backend may return either username or name depending on the endpoint,
  so this keeps the component safe while the API is still being finalized.
*/
function getDisplayName() {
  return props.profile.name || props.profile.username || "Unknown User";
}
</script>

<template>
  <article class="profile-card">
    <!-- Profile image uses backend image if available or it gives a placeholder. -->
    <img
      class="profile-image"
      :src="profile.imageUrl || profile.profile_picture || defaultProfileImage"
      :alt="`${getDisplayName()}'s profile picture`"
    />

    <div class="profile-content">
      <!-- Main profile information. -->
      <h2>{{ getDisplayName() }}, {{ profile.age || "N/A" }}</h2>

      <p class="location">
        {{ profile.location || "Location not provided" }}
      </p>

      <p class="bio">
        {{ profile.bio || "No bio added yet." }}
      </p>

      <!-- Interests only display when the profile has at least one interest. -->
      <div v-if="profile.interests?.length" class="interests">
        <span v-for="interest in profile.interests" :key="interest">
          {{ interest }}
        </span>
      </div>

      <!--Button clicks are emitted to the parent view. 
      for keeping the api out of reusable profilecard component -->
      <div class="actions">
        <button type="button" class="pass-btn" @click="emit('interact', profile.id, 'pass')">
          Pass
        </button>

        <button type="button" class="favorite-btn" @click="emit('favorite', profile.id)">
          Favorite
        </button>

        <button type="button" class="like-btn" @click="emit('interact', profile.id, 'like')">
          Like
        </button>
      </div>
    </div>
  </article>
</template>

<style scoped>
/* Main card container used for each suggested profile. */
.profile-card {
  display: flex;
  flex-direction: column;
  background: #ffffff;
  border-radius: 18px;
  overflow: hidden;
  box-shadow: 0 6px 22px rgba(0, 0, 0, 0.08);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

/* Small hover effect improves the card interaction without affecting layout. */
.profile-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 10px 28px rgba(0, 0, 0, 0.12);
}

/* Ensures all profile images have a consistent card height. */
.profile-image {
  width: 100%;
  height: 240px;
  object-fit: cover;
  background: #f4f4f4;
}

/* Contains the text details and action buttons. */
.profile-content {
  display: flex;
  flex-direction: column;
  flex: 1;
  padding: 1.25rem;
}

.profile-content h2 {
  margin: 0;
  font-size: 1.35rem;
  color: #222;
}

.location {
  margin: 0.35rem 0 0;
  color: #777;
  font-size: 0.95rem;
}

/* Bio is limited to keep cards similar in height when many profiles are shown. */
.bio {
  margin: 0.9rem 0;
  color: #555;
  line-height: 1.5;
  font-size: 0.95rem;
}

/* Interest chips support the project requirement for profile hobbies/interests. */
.interests {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-top: auto;
}

.interests span {
  background: #fff0f5;
  color: #c63f6f;
  padding: 0.35rem 0.7rem;
  border-radius: 999px;
  font-size: 0.82rem;
  font-weight: 600;
}

/* Action buttons are grouped at the bottom of the card. */
.actions {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 0.65rem;
  margin-top: 1.25rem;
}

.actions button {
  border: none;
  border-radius: 10px;
  padding: 0.75rem 0.5rem;
  font-weight: 700;
  cursor: pointer;
  transition: opacity 0.2s ease, transform 0.2s ease;
}

.actions button:hover {
  opacity: 0.9;
  transform: translateY(-1px);
}

.pass-btn {
  background: #f1f1f1;
  color: #444;
}

.favorite-btn {
  background: #fff4d6;
  color: #8a6400;
}

.like-btn {
  background: #e75480;
  color: white;
}

/* Tablet layout keeps images slightly shorter for balanced cards. */
@media (max-width: 900px) {
  .profile-image {
    height: 220px;
  }
}

/* Mobile layout stacks buttons to prevent crowding on small screens. */
@media (max-width: 520px) {
  .profile-card {
    border-radius: 14px;
  }

  .profile-image {
    height: 210px;
  }

  .profile-content {
    padding: 1rem;
  }

  .actions {
    grid-template-columns: 1fr;
  }
}
</style>