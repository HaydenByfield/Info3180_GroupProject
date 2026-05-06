<script setup>
// just a true/false for whether the profile is public or not
defineProps({
  modelValue: {
    type: Boolean,
    default: true
  }
});

const emit = defineEmits(["update:modelValue"]);
</script>

<template>
  <section class="visibility-card">
    <div>
      <h3>Profile Visibility</h3>
      <!-- explains what public actually means so the user isnt confused -->
      <p>Public profiles can appear in match suggestions and search results.</p>
    </div>

    <label class="switch"> 
    <!-- using switch to wrap the checkbox and the text together-->
    <!-- label was used instead of div so that this also toggles the checkbox--> 
      <input
        type="checkbox"
        :checked="modelValue"
        v-on:change="emit('update:modelValue', $event.target.checked)"
      />
      <!--checked = Public while unchecked = Private-->
      <!--Vue dynamic Binding the checkbox's checked state to the modelValue property -->
      <!-- show Public or Private depending on the checkbox state -->
      <span>{{ modelValue ? "Public" : "Private" }}</span>
    </label>
  </section>
</template>

<style scoped>
.visibility-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: #fafafa;
  border-radius: 14px;
}

h3 {
  margin: 0 0 0.25rem;
  font-size: 1rem;
}

p {
  margin: 0;
  color: #666;
  font-size: 0.9rem;
}

/* the checkbox and the Public/Private label sit side by side */
.switch {
  display: flex;
  gap: 0.5rem;
  align-items: center;
  font-weight: 700;
  color: #444;
}

input {
  width: 18px;
  height: 18px;
  accent-color: #e75480; /* makes the checkbox match the app color */
}

@media (max-width: 600px) {
  .visibility-card {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>