<script setup>
/*
  Reusable input field used across profile forms.
  Keeps labels, errors, and input styling consistent.
*/

defineProps({
  id: {
    type: String,
    required: true
  },
  label: {
    type: String,
    required: true
  },
  modelValue: {
    type: [String, Number],
    default: ""
  },
  type: {
    type: String,
    default: "text"
  },
  placeholder: {
    type: String,
    default: ""
  },
  error: {
    type: String,
    default: ""
  },
  required: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(["update:modelValue"]);
</script>

<template>
  <div class="form-group">
    <label :for="id">
      {{ label }}
      <span v-if="required" class="required">*</span>
    </label>

    <input
      :id="id"
      :type="type"
      :value="modelValue"
      :placeholder="placeholder"
      :aria-invalid="Boolean(error)"
      @input="emit('update:modelValue', $event.target.value)"
    />

    <p v-if="error" class="error-message">
      {{ error }}
    </p>
  </div>
</template>

<style scoped>
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

input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ccc;
  border-radius: 10px;
  font: inherit;
}

input:focus {
  outline: none;
  border-color: #e75480;
}

.error-message {
  margin: 0;
  color: #b42318;
  font-size: 0.9rem;
}
</style>