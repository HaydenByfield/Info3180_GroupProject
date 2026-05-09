import { ref } from "vue";

const currentUser = ref(null);
const loadingUser = ref(false);
const userError = ref("");

function formatUser(data) {
  const profile = data.profile || {};

  return {
    id: data.id,
    username: data.username,
    email: data.email,
    name: profile.name || data.username,
    age: profile.age || "N/A",
    location: profile.location || "Location not provided",
    bio: profile.bio || "No bio added yet.",
    relationship: profile.relationship || "",
    relationshipGoal: profile.relationship || "",
    occupation: profile.occupation || "",
    photo: profile.photo || null,
    imageUrl: profile.photo
      ? `/uploads/${profile.photo}`
      : "https://placehold.co/300x300?text=Profile"
  };
}

async function loadCurrentUser() {
  loadingUser.value = true;
  userError.value = "";

  try {
    const response = await fetch("/api/me", {
      credentials: "include"
    });

    if (!response.ok) {
      userError.value = "Could not load current user.";
      currentUser.value = null;
      return null;
    }

    const data = await response.json();
    currentUser.value = formatUser(data);

    return currentUser.value;
  } catch (error) {
    userError.value = "Could not load current user.";
    currentUser.value = null;
    return null;
  } finally {
    loadingUser.value = false;
  }
}

function clearCurrentUser() {
  currentUser.value = null;
}

export function user() {
  return {
    currentUser,
    loadingUser,
    userError,
    loadCurrentUser,
    clearCurrentUser
  };
}
