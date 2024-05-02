<template>
  <div>
    <h1>Chat Room</h1>
    <div class="chat-container">
      <div v-for="message in messages" :key="message.id" class="message">
        <strong>{{ message.sender }}:</strong> {{ message.content }}
      </div>
    </div>
    <div class="input-container">
      <input
        v-model="messageInput"
        type="text"
        placeholder="Type your message..."
      />
      <button @click="sendMessage">Send</button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      messages: [],
      messageInput: "",
      socket: null,
    };
  },
  mounted() {
    this.socket = new WebSocket(`ws://localhost:8000/ws`);

    this.socket.onopen = () => {
      console.log("WebSocket connection established");
    };

    this.socket.onmessage = (event) => {
      const message = JSON.parse(event.data);
      this.messages.push(message);
    };

    this.socket.onclose = () => {
      console.log("WebSocket connection closed");
    };
  },
  methods: {
    sendMessage() {
      const sender = localStorage.getItem("sender");
      if (this.messageInput.trim() !== "") {
        const message = {
          content: this.messageInput,
          recipient_username: this.$route.params.recipient,
          sender_username: sender,
        };
        this.socket.send(JSON.stringify(message));
        this.messageInput = "";
      }
    },
  },
};
</script>

<style>
.chat-container {
  max-height: 300px;
  overflow-y: auto;
  border: 1px solid #ccc;
  padding: 10px;
}

.message {
  margin-bottom: 5px;
}

.input-container {
  margin-top: 10px;
}

input[type="text"] {
  width: 70%;
  padding: 5px;
  margin-right: 5px;
}

button {
  padding: 5px 10px;
  cursor: pointer;
}
</style>
