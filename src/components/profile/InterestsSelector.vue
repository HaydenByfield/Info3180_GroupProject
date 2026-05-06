<script setup>
// properties retrieved from the parent form
defineProps({
  modelValue: {
    type: Array,
    default: () => []
  },
  options: {
    type: Array,
    default: () => []
  },
  error: {
    type: String,
    default: ""
  }
});

const emit = defineEmits(["update:modelValue"]);

// if the interest is already selected we remove it, otherwise we add it
function toggleInterest(interest, selected) {
  if (selected.includes(interest)) {
    // filter it out
    emit("update:modelValue", selected.filter((i) => i !== interest));
    return;
  }
  // spread the old array and add the new one
  emit("update:modelValue", [...selected, interest]);
}
</script>

<template>
  <section class="interest-section">
    <div class="section-heading">
      <h3>Interests</h3>
      <p>Select at least 3 interests.</p>
    </div>

    <div class="interest-list">
      <!-- loop through all the available interests and show them as buttons -->
      <button
        v-for="interest in options"
        :key="interest"
        type="button"
        class="interest-chip"
        :class="{ selected: modelValue.includes(interest) }"
        @click="toggleInterest(interest, modelValue)"
      >
        {{ interest }}
      </button>
    </div>

    <p v-if="error" class="err">{{ error }}</p>
  </section>
</template>

<style scoped>
.interest-section {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.section-heading h3 {
  margin: 0;
  font-size: 1rem;
}

.section-heading p {
  margin: 0.2rem 0 0;
  color: #666;
  font-size: 0.9rem;
}

.interest-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.6rem;
}

/* default unselected state */
.interest-chip {
  border: 1px solid #ddd;
  background: white;
  color: #444;
  border-radius: 999px;
  padding: 0.55rem 0.85rem;
  cursor: pointer;
  font-weight: 600;
}

/* turns pink when clicked */
.interest-chip.selected {
  background: #e75480;
  color: white;
  border-color: #e75480;
}

.err {
  color: #b42318;
  font-size: 0.9rem;
  margin: 0;
}
</style>