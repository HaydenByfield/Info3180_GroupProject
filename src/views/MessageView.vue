<script setup>
import { computed, ref } from "vue";

const activeChatId = ref(1);
const newMessage = ref("");

// get actual chats here from the backend
const chats = ref([
  {
    id: 1,
    name: "Alice",
    messages: [
      {
        id: 1,
        text: "hihi how are you doing so far?",
        sentByMe: true
      },
      {
        id: 2,
        text: "I'm doing great, thanks for asking! How about you?",
        sentByMe: false
      },
      {
        id: 3,
        text: "I'm good too! Just enjoying the app so far.",
        sentByMe: true
      },
      {
        id: 4,
        text: "Bye!",
        sentByMe: true
      }
   ]
  },
  {
    id: 2,
    name: "Jordan",
    messages: [
      {
        id: 1,
        text: "Are we still on for later?",
        sentByMe: false
      }
    ]
  },
  {
    id: 3,
    name: "Taylor",
    messages: [
      {
        id: 1,
        text: "That sounds good to me.",
        sentByMe: false
      }
    ]
  }
]);

const activeChat = computed(() => {
  return chats.value.find((chat) => chat.id === activeChatId.value);
});

function selectChat(chatId) {
  activeChatId.value = chatId;
}

function sendMessage() {
  const text = newMessage.value.trim();

  if (!text || !activeChat.value) {
    return;
  }

  // send the message to the backend here, and add it to the chat if it works
  activeChat.value.messages.push({
    id: Date.now(),
    text,
    sentByMe: true
  });

  newMessage.value = "";
}
</script>

<template>
  <main class="messages-page">
    <h1>Messages</h1>

    <section class="messages-panel">
      <aside class="chat-list" aria-label="Active chats">
        <button
          v-for="chat in chats"
          :key="chat.id"
          type="button"
          class="chat-list-item"
          :class="{ active: chat.id === activeChatId }"
          @click="selectChat(chat.id)"
        >
          {{ chat.name }}
        </button>
      </aside>

      <section v-if="activeChat" class="chat-box" :aria-label="`Chat with ${activeChat.name}`">
        <div class="chat-messages">
          <p
            v-for="message in activeChat.messages"
            :key="message.id"
            class="message-bubble"
            :class="{ sent: message.sentByMe, received: !message.sentByMe }"
          >
            {{ message.text }}
          </p>
        </div>

        <form class="message-form" @submit.prevent="sendMessage">
          <input
            v-model="newMessage"
            type="text"
            placeholder="Type a message..."
            aria-label="Type a message"
          />
          <button type="submit">Send</button>
        </form>
      </section>
    </section>
  </main>
</template>

<style scoped>
.messages-page {
  width: min(1100px, 92%);
  margin: 0 auto;
  padding: 2rem 0;
}

.messages-page h1 {
  margin: 0 0 1rem;
  color: #222;
  font-size: 2.2rem;
}

.messages-panel {
  display: grid;
  grid-template-columns: minmax(190px, 260px) 1fr;
  min-height: 360px;
  overflow: hidden;
  border: 1px solid #ededed;
  border-radius: 10px;
  background: white;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.chat-list {
  border-right: 1px solid #ededed;
  background: #fafafa;
}

.chat-list-item {
  width: 100%;
  padding: 1rem;
  border: 0;
  border-bottom: 1px solid #ededed;
  background: transparent;
  color: #222;
  font-weight: 700;
  text-align: left;
  cursor: pointer;
}

.chat-list-item:hover,
.chat-list-item.active {
  background: #fff0f5;
  color: #b93767;
}

.chat-box {
  display: grid;
  grid-template-rows: 1fr auto;
  min-width: 0;
}

.chat-messages {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  min-height: 240px;
  padding: 1rem;
  overflow-y: auto;
}

.message-bubble {
  max-width: min(65%, 520px);
  margin: 0;
  padding: 0.75rem 1rem;
  border-radius: 8px;
  line-height: 1.4;
}

.message-bubble.sent {
  align-self: flex-end;
  background: #e75480;
  color: white;
}

.message-bubble.received {
  align-self: flex-start;
  background: #f5f5f5;
  color: #444;
}

.message-form {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 0.75rem;
  padding: 0.9rem;
  border-top: 1px solid #ededed;
  background: #fafafa;
}

.message-form input {
  min-width: 0;
  padding: 0.75rem 0.9rem;
  border: 1px solid #ddd;
  border-radius: 8px;
}

.message-form button {
  padding: 0.75rem 1.2rem;
  border: 0;
  border-radius: 10px;
  background: #e75480;
  color: white;
  font-weight: 700;
  cursor: pointer;
}

.message-form button:hover {
  background: #d94270;
}

@media (max-width: 700px) {
  .messages-page {
    width: min(100% - 2rem, 1100px);
  }

  .messages-panel {
    grid-template-columns: 1fr;
  }

  .chat-list {
    display: flex;
    overflow-x: auto;
    border-right: 0;
    border-bottom: 1px solid #ededed;
  }

  .chat-list-item {
    width: auto;
    min-width: 120px;
    border-right: 1px solid #ededed;
    border-bottom: 0;
  }

  .message-bubble {
    max-width: 85%;
  }
}
</style>
