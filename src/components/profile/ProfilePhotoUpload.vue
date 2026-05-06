<script setup>
import { onBeforeUnmount, ref } from "vue";

const emit = defineEmits(["change"]);

// stores the preview image url so we can show it in the box
const previewUrl = ref("");
const err = ref("");

function onFileChange(e) {
  const file = e.target.files[0];
  err.value = "";

  if (!file) return;

  // make sure they actually picked an image and not like a pdf or something
  if (!file.type.startsWith("image/")) {
    err.value = "Please choose a valid image file.";
    return;
  }

  // 2MB limit
  if (file.size > 2 * 1024 * 1024) {
    err.value = "Image must be smaller than 2MB.";
    return;
  }

  // if there was already a preview we need to clear it first before making a new one
  if (previewUrl.value) URL.revokeObjectURL(previewUrl.value);

  // createObjectURL turns the file into a temporary url the browser can display
  previewUrl.value = URL.createObjectURL(file);

  // send the file up to the parent form
  emit("change", file);
}

// clean up the url when the component is removed so we dont leak memory
onBeforeUnmount(() => {
  if (previewUrl.value) URL.revokeObjectURL(previewUrl.value);
});
</script>

<template>
  <div class="photo-upload">
    <label for="profile-photo">Profile Photo</label>

    <!-- show the image preview if a photo was selected, otherwise show placeholder text -->
    <div class="preview-box">
      <img v-if="previewUrl" :src="previewUrl" alt="preview" />
      <span v-else>No photo selected</span>
    </div>

    <input id="profile-photo" type="file" accept="image/*" @change="onFileChange" />

    <p v-if="err" class="err">{{ err }}</p>
  </div>
</template>

<style scoped>
.photo-upload {
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
}

label {
  font-weight: 600;
  color: #333;
}

/* the box that shows the image preview before uploading */
.preview-box {
  width: 140px;
  height: 140px;
  border: 1px dashed #bbb;
  border-radius: 16px;
  display: grid;
  place-items: center;
  overflow: hidden;
  background: #fafafa;
  color: #777;
  font-size: 14px;
  text-align: center;
}

.preview-box img {
  width: 100%;
  height: 100%;
  object-fit: cover; /* makes sure the image fills the box without stretching */
}

input {
  font: inherit;
}

.err {
  color: #b42318;
  font-size: 0.9rem;
  margin: 0;
}
</style>