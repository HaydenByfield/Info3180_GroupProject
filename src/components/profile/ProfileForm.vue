<script setup>
import { reactive, ref, watch } from "vue";
import FormInput from "./FormInput.vue";
import InterestSelector from "./InterestsSelector.vue";
import ProfilePhotoUpload from "./ProfilePhotoUpload.vue";
import VisibilitySelector from "./VisibilitySelector.vue";

// this form is used for both creating and editing a profile
// the parent view will send the method to POST or PATCH depending on the creating or editing 
const props = defineProps({
  initialProfile: {
    type: Object,
    default: () => ({})
  },
  submitLabel: {
    type: String,
    default: "Save Profile"
  },
  isSubmitting: {
    type: Boolean,
    default: false
  },
  serverError: {
    type: String,
    default: ""
  }
});

const emit = defineEmits(["submit"]);

// all the interests users can pick from
const availableInterests = [
  "Music",
  "Travel",
  "Food",
  "Fitness",
  "Movies",
  "Art",
  "Gaming",
  "Reading",
  "Sports",
  "Dancing",
  "Tech"
];

// reactive holds all the form fields together so they update the UI automatically
const form = reactive({
  name: "",
  age: "",
  bio: "",
  location: "",
  radius: 20,
  interests: [],
  relationshipGoal: "",
  occupation: "",
  isPublic: true,
  profilePhoto: null
});

const errors = ref({});

// if initialProfile is passed in (edit mode), fill the form with the existing data
watch(
  () => props.initialProfile,
  (profile) => {
    form.name = profile.name || profile.username || "";
    form.age = profile.age || "";
    form.bio = profile.bio || "";
    form.location = profile.location || "";
    form.radius = profile.radius || 20;
    form.interests = profile.interests || [];
    form.relationshipGoal = profile.relationshipGoal || "";
    form.occupation = profile.occupation || "";
    form.isPublic = profile.isPublic ?? true; // default to public if not set
    form.profilePhoto = null;
  },
  { immediate: true } // runs immediately so the form is filled on load
);


//validation for form data entry
function validateForm() {
  const newErrors = {};//storing the errors to display during form entry

  if (!form.name.trim()) newErrors.name = "Name is required.";

  if (!form.age) {
    newErrors.age = "Age is required.";
  } else if (Number(form.age) < 18) {
    newErrors.age = "Users must be at least 18.";
  }

  if (!form.bio.trim()) newErrors.bio = "Bio is required.";

  if (!form.location.trim()) newErrors.location = "Location is required.";

  if (!form.radius || Number(form.radius) <= 0)
    newErrors.radius = "Enter a valid match radius.";

  // need at least 3 interests for user
  if (form.interests.length < 3)
    newErrors.interests = "Select at least 3 interests.";

  if (!form.relationshipGoal.trim())
    newErrors.relationshipGoal = "Relationship goal is required.";

  if (!form.occupation.trim())
    newErrors.occupation = "Occupation or school is required.";

  errors.value = newErrors;

  // if there are no keys in newErrors the form is valid
  return Object.keys(newErrors).length === 0;
}

// when the photo component emits a file we store it in the form
function onPhotoChange(file) {
  form.profilePhoto = file;
}

function onSubmit() {
  if (!validateForm()) return;
  emit("submit", { ...form });
}
</script>

<template>
  <form class="profile-form" @submit.prevent="onSubmit">
    <!--two column grid chosen-->
    <div class="form-grid">
      <FormInput
        id="name"
        v-model="form.name"
        label="Name"
        placeholder="Enter your name"
        :error="errors.name"
        required
      />

      <FormInput
        id="age"
        v-model="form.age"
        label="Age"
        type="number"
        placeholder="Enter your age"
        :error="errors.age"
        required
      />

      <FormInput
        id="location"
        v-model="form.location"
        label="Location"
        placeholder="Kingston, St. Andrew, Portmore..."
        :error="errors.location"
        required
      />

      <FormInput
        id="radius"
        v-model="form.radius"
        label="Match Radius (km)"
        type="number"
        placeholder="Example: 20"
        :error="errors.radius"
        required
      />

      <FormInput
        id="relationshipGoal"
        v-model="form.relationshipGoal"
        label="Relationship Goal"
        placeholder="Long-term, friendship, casual..."
        :error="errors.relationshipGoal"
        required
      />

      <FormInput
        id="occupation"
        v-model="form.occupation"
        label="Occupation / School"
        placeholder="Student, developer, designer..."
        :error="errors.occupation"
        required
      />
    </div>

    <!--given bio is textarea -->
    <div class="form-group full-width">
      <label for="bio">Bio <span class="required">*</span></label>

      <textarea
        id="bio"
        v-model="form.bio"
        placeholder="Tell people a little about yourself..."
        rows="5"
      ></textarea>

      <p v-if="errors.bio" class="err">{{ errors.bio }}</p>
    </div>

    <InterestSelector
      v-model="form.interests"
      :options="availableInterests"
      :error="errors.interests"
    />

    <ProfilePhotoUpload @change="onPhotoChange" />

    <VisibilitySelector v-model="form.isPublic" />

    <!-- show backend errors if the server returns something -->
    <p v-if="serverError" class="server-err">{{ serverError }}</p>

    <button type="submit" class="submit-btn" :disabled="isSubmitting">
      {{ isSubmitting ? "Saving..." : submitLabel }}
    </button>
  </form>
</template>

<style scoped>
.profile-form {
  display: flex;
  flex-direction: column;
  gap: 1.4rem;
  width: 100%;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.2rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

label {
  font-weight: 600;
  color: #333;
}

.required {
  color: #c0392b;
}

textarea {
  width: 100%;
  resize: vertical;
  padding: 0.75rem;
  border: 1px solid #ccc;
  border-radius: 10px;
  font: inherit;
}

textarea:focus {
  outline: none;
  border-color: #e75480;
}

.err,
.server-err {
  color: #b42318;
  font-size: 0.9rem;
  margin: 0;
}

/* server errors get a red background to stand out more */
.server-err {
  background: #fdecea;
  padding: 0.85rem 1rem;
  border-radius: 10px;
}

.submit-btn {
  align-self: flex-start;
  border: none;
  border-radius: 10px;
  background: #e75480;
  color: white;
  font-weight: 700;
  padding: 0.85rem 1.4rem;
  cursor: pointer;
}

/*greys out the button while its waiting for the server*/
.submit-btn:disabled {
  opacity: 0.65;
  cursor: not-allowed;
}

@media (max-width: 700px) {
  .form-grid { grid-template-columns: 1fr; }
  .submit-btn { width: 100%; }
}
</style>