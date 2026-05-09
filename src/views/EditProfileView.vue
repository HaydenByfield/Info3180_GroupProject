<script setup>
import { onMounted, ref } from "vue";
import { useRouter } from "vue-router";
import ProfileForm from "@/components/profile/ProfileForm.vue";
import { user } from "@/user/user.js";

/*
allows logged-in user update their existing profile.
This view loads the user's current profile data, passes it to ProfileForm,
then submits the updated profile details back to the backend.
*/

const profile = ref(null);
const isLoading = ref(false);
const isSubmitting = ref(false);


const errorMessage = ref("");

const serverError = ref("");

const successMessage = ref("");
const csrfToken = ref("");

const router = useRouter();
const { currentUser, loadCurrentUser } = user();

async function getCsrfToken() {
  if (csrfToken.value) return csrfToken.value;

  const response = await fetch("/api/csrf-token", {
    credentials: "include"
  });
  const data = await response.json();
  csrfToken.value = data.csrf_token;

  return csrfToken.value;
}

async function fetchCurrentProfile() {
  isLoading.value = true;
  errorMessage.value = "";
  serverError.value = "";

  try {
    const loadedUser = await loadCurrentUser();

    if (!loadedUser) {
      throw new Error("Unable to load your profile.");
    }

    profile.value = currentUser.value;
  } catch (error) {
    console.error(error);
    errorMessage.value =
      error.message || "Something went wrong while loading your profile.";
  } finally {
    isLoading.value = false;
  }
}

async function handleUpdateProfile(profileData) {
  isSubmitting.value = true;
  serverError.value = "";
  successMessage.value = "";

  try {
    const token = await getCsrfToken();
    const formData = new FormData();

    formData.append("name", profileData.name);
    formData.append("age", profileData.age);
    formData.append("bio", profileData.bio);
    formData.append("location", profileData.location);
    formData.append("radius", profileData.radius);
    formData.append("relationshipGoal", profileData.relationshipGoal);
    formData.append("occupation", profileData.occupation);
    formData.append("isPublic", profileData.isPublic);
    formData.append("interests", JSON.stringify(profileData.interests));

    if (profileData.profilePhoto) {
      formData.append("profilePhoto", profileData.profilePhoto);
    }

    const response = await fetch("/api/profile", {
      method: "PUT",
      credentials: "include",
      headers: {
        "X-CSRFToken": token
      },
      body: formData
    });

    const data = await response.json().catch(() => ({}));

    if (!response.ok) {
      throw new Error(data.message || "Unable to update profile.");
    }

    successMessage.value = "Profile updated successfully.";

    setTimeout(() => {
      router.push("/dashboard");
    }, 700);
  } catch (error) {
    console.error(error);
    serverError.value =
      error.message || "Something went wrong while updating your profile.";
  } finally {
    isSubmitting.value = false;
  }
}

onMounted(() => {
  fetchCurrentProfile();
});
</script>

<template>
  <main class="edit-profile-page">
    <section class="page-header">
      <h1>Edit Profile</h1>
      <p1>
        Update your profile details.
      </p1>
    </section>

    <section v-if="isLoading" class="loading-card">
      <p>Loading your profile...</p>
    </section>

    <section v-else-if="errorMessage" class="error-card">
      <p>{{ errorMessage }}</p>

      <button type="button" @click="fetchCurrentProfile">
        Retry...
      </button>
    </section>

    <section v-else-if="profile" class="form-card">
      <p v-if="successMessage" class="success-message">
        {{ successMessage }}
      </p>

      <ProfileForm
        :initial-profile="profile"
        submit-label="Update Profile"
        :is-submitting="isSubmitting"
        :server-error="serverError"
        @submit="handleUpdateProfile"
      />
    </section>
  </main>
</template>

<style scoped>
.edit-profile-page {
  width: min(950px, 92%);
  margin: 0 auto;
  padding: 2rem 0 3rem;
}

.page-header {
  margin-bottom: 1.5rem;
}

.page-header h1 {
  font-size: 2.2rem;
  margin: 0 0 0.5rem;
  color: #222;
}

.page-header p {
  max-width: 720px;
  margin: 0;
  color: #555;
  /*line-height: 1.6;*/
}

.form-card,
.loading-card,
.error-card {
  background: #ffffff;
  border-radius: 18px;
  padding: 1.5rem;
  box-shadow: 0 6px 22px rgba(0, 0, 0, 0.08);
}

.loading-card {
  color: #444;
}

.error-card {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  color: #b42318;
}

.error-card button {
  align-self: flex-start;
  border: none;
  border-radius: 10px;
  background: #e75480;
  color: white;
  font-weight: 700;
  padding: 0.75rem 1rem;
  cursor: pointer;
}

.success-message {
  background: #eaf8ef;
  color: #146c2e;
  padding: 0.85rem 1rem;
  border-radius: 10px;
  margin: 0 0 1.2rem;
}
/*using a media query for some of the features for the mobile screens*/
@media (max-width: 640px) {
  .edit-profile-page {
    padding-top: 1.25rem;
  }

  .page-header h1 {
    font-size: 1.8rem;
  }

  .form-card,
  .loading-card,
  .error-card {
    padding: 1rem;
    border-radius: 14px;
  }

  .error-card button {
    width: 100%;
  }
}
</style>
