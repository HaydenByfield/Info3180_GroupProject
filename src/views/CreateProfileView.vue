<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import ProfileForm from "@/components/profile/ProfileForm.vue";

//CreateProfileView handles the first-time profile creation page.

/******* imports the ProfileForm Companent

  This view ensures that:
  - we are converting the form into FormData
  - showing server errors
  - redirecting after successful entry
*/

const router = useRouter();

const isSubmitting = ref(false);
const serverError = ref("");
const successMessage = ref("");
const csrf_token = ref("")


const getCsrfToken = async () => {
    try{
        let response = await fetch('/api/csrf-token')
        let data = await response.json();
        csrf_token.value = data.csrf_token
        console.log(data)

    } catch(error){
        console.log(error)
    }
}
onMounted(() => {
    getCsrfToken();
})

async function handleCreateProfile(profileData) {
  isSubmitting.value = true;
  serverError.value = "";
  successMessage.value = "";

  try { 
    const formData = new FormData();

    ///Need to find a way to save the name from register view so that user does not have to reenter name
    //should invoke history state
    formData.append("name", profileData.name);
    formData.append("age", profileData.age);
    formData.append("bio", profileData.bio);
    formData.append("location", profileData.location);
    formData.append("radius", profileData.radius);
    formData.append("relationshipGoal", profileData.relationshipGoal);
    formData.append("occupation", profileData.occupation);
    formData.append("isPublic", profileData.isPublic);

    //the user interests are sent as a JSON string because value is array
    formData.append("interests", JSON.stringify(profileData.interests));

    if (profileData.profilePhoto) {
      formData.append("profilePhoto", profileData.profilePhoto);
    }
    console.log("INTERESTS SENT:", profileData.interests);
    console.log("FORMDATA INTERESTS:", JSON.stringify(profileData.interests));
    const response = await fetch("/api/profile", {
      method: "POST",
      credentials: "include",
      headers: {'X-CSRFToken': csrf_token.value},
      body: formData
    });
    
    const data = await response.json().catch(() => ({}));
    console.log(data)
    if (!response.ok) {
      throw new Error(data.message || "Unable to create profile.");
    }

    successMessage.value = "Profile created successfully.";

    //after profile is created push the user to view the dashboard
    router.push("/dashboard");
    } catch (error) {
        console.error(error);
        serverError.value = "Something went wrong. Please try again.";
    } finally {
  isSubmitting.value = false;
}
}
</script>

<template>
  <main class="create-profile-page">
    <section class="page-header">
      <h1>Create Your Profile</h1>
      <p>
        Complete your profile so DriftDater can suggest better matches based on your
        specific details.
      </p>
    </section>

    <section class="form-card">
      <p v-if="successMessage" class="success-message">
        {{ successMessage }}
      </p>

      <ProfileForm
        submit-label="Create Profile"
        :is-submitting="isSubmitting"
        :server-error="serverError"
        @submit="handleCreateProfile"
      />
    </section>
  </main>
</template>

<style scoped>
.create-profile-page {
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
  line-height: 1.6;
}

.form-card {
  background: #ffffff;
  border-radius: 18px;
  padding: 1.5rem;
  box-shadow: 0 6px 22px rgba(0, 0, 0, 0.08);
}

.success-message {
  background: #eaf8ef;
  color: #146c2e;
  padding: 0.85rem 1rem;
  border-radius: 10px;
  margin: 0 0 1.2rem;
}

@media (max-width: 640px) {
  .create-profile-page {
    padding-top: 1.25rem;
  }

  .page-header h1 {
    font-size: 1.8rem;
  }

  .form-card {
    padding: 1rem;
    border-radius: 14px;
  }
}
</style>