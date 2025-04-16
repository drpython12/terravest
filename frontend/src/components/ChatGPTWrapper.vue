<template>
  <div class="chat-wrapper">
    <div class="chat-header">
      <h3>TerraVest Portfolio Advisor</h3>
      <p>Ask how well this company aligns with your portfolio preferences.</p>
    </div>
    <div class="chat-box">
      <div class="messages">
        <div
          v-for="(message, index) in messages"
          :key="index"
          :class="['message', message.sender]"
        >
          <p>{{ message.text }}</p>
        </div>
      </div>
      <div class="chat-input">
        <input
          type="text"
          v-model="userInput"
          placeholder="Type your question here..."
          @keyup.enter="sendMessage"
        />
        <button @click="sendMessage">Send</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import axiosInstance from "@/axiosConfig";

const props = defineProps({
  company: {
    type: Object,
    required: true,
  },
  userPreferences: {
    type: Object,
    required: true,
  },
});

const messages = ref([
  {
    sender: "bot",
    text: "Hi! I’m ChatGPT. Ask me how well this company aligns with your portfolio preferences.",
  },
]);

const userInput = ref("");

const sendMessage = async () => {
  if (!userInput.value.trim()) return;

  // Add user message to the chat
  messages.value.push({ sender: "user", text: userInput.value });

  const currentInput = userInput.value;
  userInput.value = ""; // Clear input field

  try {
    // Send the user input, company data, and preferences to the backend
    const response = await axiosInstance.post("/api/chatgpt-advisor/", {
      question: currentInput,
      company: props.company,
      preferences: props.userPreferences,
    });

    // Add ChatGPT's response to the chat
    messages.value.push({ sender: "bot", text: response.data.answer });
  } catch (error) {
    console.error("Error communicating with ChatGPT:", error);
    messages.value.push({
      sender: "bot",
      text: "Sorry, I couldn't process your request. Please try again later.",
    });
  }
};
</script>

<style scoped>
.chat-wrapper {
  background: #ffffff;
  border-radius: 16px;
  padding: 20px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.chat-header {
  text-align: center;
  margin-bottom: 20px;
}

.chat-header h3 {
  font-size: 1.8rem;
  font-weight: bold;
  color: #333;
}

.chat-header p {
  font-size: 1rem;
  color: #666;
}

.chat-box {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.messages {
  max-height: 300px;
  overflow-y: auto;
  padding: 10px;
  background: #f9f9f9;
  border-radius: 8px;
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1);
}

.message {
  margin-bottom: 10px;
  padding: 10px;
  border-radius: 8px;
  max-width: 80%;
}

.message.user {
  background: #007aff;
  color: white;
  align-self: flex-end;
}

.message.bot {
  background: #e5e5ea;
  color: #333;
  align-self: flex-start;
}

.chat-input {
  display: flex;
  gap: 10px;
}

.chat-input input {
  flex: 1;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 8px;
  font-size: 1rem;
}

.chat-input button {
  padding: 10px 20px;
  background: #007aff;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
}

.chat-input button:hover {
  background: #005bb5;
}
</style>