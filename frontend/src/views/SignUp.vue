<template>
  <div class="homepage">
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
      <div class="container">
        <a class="navbar-brand" href="/">
          <img
            src="@/assets/digite_logo.png"
            alt="Logo"
            width="150"
            height="15%"
            class="d-inline-block align-top"
          />
        </a>
        <ul class="nav justify-content-end">
          <li class="nav-item">
            <a class="nav-link" href="/login">Login</a>
          </li>
          <li class="nav-item active">
            <a class="nav-link text-white" href="/signup">Signup</a>
          </li>
        </ul>
      </div>
    </nav>
    <div
      class="hero text-white align-items-center justify-content-center text-center"
    >
      <br />
      <br />
      <br />
      <form
        @submit.prevent="handleSubmit"
        class="d-flex flex-column justify-content-center align-items-center"
      >
        <div class="form-outline mb-4">
          <label class="form-label" for="username">Full Nme</label>
          <br />
          <input
            v-model="name"
            type="text"
            class="form-control"
            id="name"
            placeholder="Enter Name"
            required
          />
        </div>
        <div class="form-outline mb-4">
          <label class="form-label" for="username">Username</label>
          <br />
          <input
            v-model="username"
            type="text"
            class="form-control"
            id="username"
            placeholder="This Cannot be changed Later!!"
            required
          />
        </div>
        <div class="form-outline mb-4">
          <label class="form-label" for="username">Email</label>
          <br />
          <input
            v-model="email"
            type="email"
            class="form-control"
            id="email"
            placeholder="Enter Email"
            required
          />
        </div>

        <div class="form-outline mb-4">
          <label class="form-label" for="password">Password</label>
          <input
            v-model="password"
            type="password"
            class="form-control"
            id="password"
            placeholder="Enter Password"
            required
          />
        </div>
        <div class="form-outline mb-4">
          <label for="avatar">Avatar</label>
          <div class="d-flex flex-wrap">
            <img
              v-for="avatar in avatars"
              :key="avatar.id"
              :src="avatar.src"
              @click="selectAvatar(avatar.id)"
              :class="{
                'border border-primary': selectedAvatarId === avatar.id,
              }"
              alt="Avatar"
              class="img-thumbnail rounded-circle mr-2"
              style="width: 100px; height: 100px"
            />
          </div>
        </div>
        <button type="submit" class="btn btn-dark">Register</button>
      </form>

      <div
        v-if="errors.length > 0"
        class="alert d-flex flex-column justify-content-center align-items-center"
      >
        <ul class="list-unstyled">
          <li v-for="error in errors" :key="error">
            <pre class="justify-content-center align-items-center">
              #######################################
                    {{ error }}
              #######################################
              </pre
            >
          </li>
        </ul>
      </div>
      <div v-if="msg.length > 0" class="alert alert-success">
        <ul>
          <li v-for="msg in msg" :key="msg">
            <pre>
            #######################################
                    {{ msg }}
            #######################################
            </pre>
          </li>
        </ul>
      </div>
    </div>
    <iframe
      src="https://kairon.nimblework.com/cdn/popupChatbox.html?botid=66220beaed03a5fa2752de6e&token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJnQUFBQUFCbUltdDRBbDdHVkVSRDlIMThfVG5vNVpyTC1wQzFaTlFiVk95TUd6NXVQYk5IUWlCUk40UXhqTkh1MDNBLXc1VlY3V3VLNzFpeDFtQlBQRkM1a1FXVjF3Q1AxZWpHNU5lbjlyRVNFTjUzcVhtajdIWkI5bjlsSkNYVGFUdVFsZlRQVmptc093ZnlIb0ExbzZUcC1EWVZsc0I0WFREVUY4d1c1SWhhaExCNTVkWkdKOEw3OHFHeG5rRDRIOG92bHhSTzZyNUJRX1hsLUlUd0IxSlNpcTRFdHM1YkRWazIteGxvdWthRmFLYTNyZklaVHdrU1dnOXliakZuVDNtNmpJaGlBUW9hbHhsX3JTaHBKWmdpTlJ0MUlsbEZiUUcxUlIxM0s5b09VUUI1TE5NQzJHaEo2MDNua3h0RERpd013T2tOM1VoWGFObFFEMWZLQk1kelUtOWlzcE9ReGc9PSIsInZlcnNpb24iOiIyLjAiLCJpYXQiOjE3MTM1MzE3Njh9.AHwUqB3Biz9cpMT-HZZsMc48N37jRL_TWySi2hMC68s"
      id="kairon-chatbox"
      frameborder="0"
      scrolling="no"
      style="
        margin: 0;
        padding: 0;
        position: fixed;
        right: 50px;
        bottom: 40px;
        overflow: hidden;
        z-index: 999999;
      "
      height="72px"
      width="72px"
    ></iframe>
    <footer class="footer bg-dark text-white text-center py-3">
      &copy; 2024 ChatApp
    </footer>
  </div>
</template>

<script>
import router from "@/router";
import axios from "axios";
// const botId = '66220beaed03a5fa2752de6e';
// const token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJnQUFBQUFCbUltdDRBbDdHVkVSRDlIMThfVG5vNVpyTC1wQzFaTlFiVk95TUd6NXVQYk5IUWlCUk40UXhqTkh1MDNBLXc1VlY3V3VLNzFpeDFtQlBQRkM1a1FXVjF3Q1AxZWpHNU5lbjlyRVNFTjUzcVhtajdIWkI5bjlsSkNYVGFUdVFsZlRQVmptc093ZnlIb0ExbzZUcC1EWVZsc0I0WFREVUY4d1c1SWhhaExCNTVkWkdKOEw3OHFHeG5rRDRIOG92bHhSTzZyNUJRX1hsLUlUd0IxSlNpcTRFdHM1YkRWazIteGxvdWthRmFLYTNyZklaVHdrU1dnOXliakZuVDNtNmpJaGlBUW9hbHhsX3JTaHBKWmdpTlJ0MUlsbEZiUUcxUlIxM0s5b09VUUI1TE5NQzJHaEo2MDNua3h0RERpd013T2tOM1VoWGFObFFEMWZLQk1kelUtOWlzcE9ReGc9PSIsInZlcnNpb24iOiIyLjAiLCJpYXQiOjE3MTM1MzE3Njh9.AHwUqB3Biz9cpMT-HZZsMc48N37jRL_TWySi2hMC68s'
// const  kaironURL = 'https://kairon-api.nimblework.com';
// const origin = 'https://kairon.nimblework.com';
// const nudgeServer = 'https://kairon-nudge.nimblework.com';
// const initClient=()=>{fetch(`${kaironURL}/api/bot/${botId}/chat/client/config/${token}`,{headers:{Accept:'application/json','Content-Type':'application/json'}}).then(e=>e.json()).then(e=>{if(e.success){let t=e.data;t.container='#kairon-client-container',t.botId=`${botId}`,window.ChatClient?window.ChatClient(t):top.ChatClient&&top.ChatClient(t);let n=[{fetchURL:`${nudgeServer}/api/nudge/config/${botId}`},{fetchURL:`${nudgeServer}/api/nudge/message/list/${botId}`},];if(t.isNudgeEnabled){let i=[];n.map(e=>{i.push(e)});let a=i.map(e=>fetch(e.fetchURL,{headers:{'Content-Type':'application/json',authorization:`Bearer ${token}`}}).then(e=>e.ok?e.json():{}));Promise.all(a).then(e=>{if(e[0]?.data?.length&&e[1].data?.length){let n={botId:botId,dynamicNudgeData:e[0],nudgeMessagesList:e[1],container:'#kairon-nudge-container',nudge_url:nudgeServer,headers:t.headers,api_server_host_url:t.api_server_host_url},i=document.getElementsByTagName('body')[0],a=document.createElement('script');a.src=`${origin}/cdn/nudge_client.js`,a.id='kairon-nudge-script',a.onload=function(){window.NudgeClient&&new window.NudgeClient(n)},i.appendChild(a)}})}}})},body=document.getElementsByTagName('body')[0],container=document.createElement('div');container.id='kairon-client-container',(nudgeContainer=document.createElement('div')).id='kairon-nudge-container';const scriptTag=document.createElement('script');scriptTag.src=`${origin}/cdn/kairon_client.js`,scriptTag.onload=initClient,body.appendChild(container),body.appendChild(nudgeContainer),body.appendChild(scriptTag);
export default {
  data() {
    return {
      name: "",
      username: "",
      email: "",
      password: "",
      errors: [],
      msg: [],
      avatars: [
        {
          id: 1,
          src: "https://img.freepik.com/free-vector/user-circles-set_78370-4704.jpg?size=626&ext=jpg&ga=GA1.1.972355406.1713266629&semt=sph",
        },
        {
          id: 2,
          src: "https://img.freepik.com/free-photo/androgynous-avatar-non-binary-queer-person_23-2151100226.jpg?size=626&ext=jpg&ga=GA1.1.972355406.1713266629&semt=sph",
        },
        {
          id: 3,
          src: "https://img.freepik.com/premium-photo/memoji-happy-man-white-background-emoji_826801-6839.jpg?size=626&ext=jpg&ga=GA1.1.972355406.1713266629&semt=sph",
        },
        {
          id: 4,
          src: "https://img.freepik.com/free-psd/3d-illustration-person-with-long-hair_23-2149436197.jpg?size=626&ext=jpg&ga=GA1.1.972355406.1713266629&semt=sph",
        },
        {
          id: 5,
          src: "https://img.freepik.com/free-psd/3d-illustration-person-with-sunglasses_23-2149436188.jpg?size=626&ext=jpg&ga=GA1.1.972355406.1713266629&semt=sph",
        },
      ],
      selectedAvatarId: null,
    };
  },
  methods: {
    async handleSubmit() {
      this.errors = []; // Clear errors before submission
      this.msg = []; // Clear errors before submission
      try {
        const data = {
          name: this.name,
          username: this.username,
          email: this.email,
          password: this.password,
          roles: "users",
          avatarid: this.selectedAvatarId, // Include selected avatar id if available
        };
        const response = await axios.post("http://localhost:8000/signup", data);
        console.log(response.data["message"]);
        if (response.data["message"] === "Usernname already taken") {
          throw new Error("Usernname already taken");
        } else if (data.message == "Admin Already Exists") {
          throw new Error("Admin Already Exists!!");
        } else {
          console.log("Signup successful:", response.data);
          setTimeout(() => router.push("/login"), "5000");
          this.msg.push(
            "Signup Successfull!! You will be automatically Redirected..."
          );
        }
      } catch (error) {
        console.error(error);
        this.errors.push(error);
        setTimeout(() => (this.errors = []), "3000");
      }
    },
    selectAvatar(id) {
      this.selectedAvatarId = id;
    },
  },
};
</script>

<style>
.homepage {
  background-color: #212529; /* Dark background */
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}
.hero {
  flex: 1; /* Take up remaining space after navbar and footer */
  color: #fff; /* White text */
  background-color: black; /* Add subtle background pattern (optional) */
  background-size: cover;
  background-repeat: no-repeat;
}
.user-avatar {
  cursor: pointer;
}
</style>
