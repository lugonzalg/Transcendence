<template>

  <DefaultNavbar></DefaultNavbar>

  <div class="login-container" v-if="!showOTPVerification">
    <div class="login-info">
    </div>
    <div class="login-form">
      <h2>Iniciar Sesión</h2>
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label for="username">Usuario:</label>
          <input type="text" id="username" v-model="credentials.username">
        </div>
        <div class="form-group">
          <label for="password">Contraseña:</label>
          <input type="password" id="password" v-model="credentials.password">
        </div>
        <button type="submit">Iniciar Sesión</button>
        <GoogleLogin></GoogleLogin>
        <!-- Boton Login Intra 42 -->
        <div>
         <button class="button_intra" @click=redirectToIntra >Registrarse con Intra 42</button>
        </div>
      </form>
    </div>
    
  </div>

  <PopUpError v-if="popupTriggers.responseTrigger" :error-message="errorMessage" @close="popupTriggers.responseTrigger = false"></PopUpError>
  
  <OTPVerification v-if="showOTPVerification"></OTPVerification>

</template>
  
<script>

import GoogleLogin from '@/components/GoogleLogin.vue';
import DefaultNavbar from '@/components/DefaultNavbar.vue';
import VueCookies from 'vue-cookies';
import OTPVerification from '@/components/OtpVerification.vue';
import PopUpError from '@/components/PopUpError.vue';
import { login } from '@/methods/api/login.js';
import { ref } from 'vue';



export default {
  name: 'LoginView',
  components: { GoogleLogin, DefaultNavbar, OTPVerification, PopUpError },
  setup() {
    const errorMessage = ref('');
    const popupTriggers = ref({
      responseTrigger: false,
      timmedTrigger: false
    });
    const credentials = ref({
      username: '',
      password: ''
    });
    return { credentials , popupTriggers, errorMessage};
  },
  methods: 
  {
    async handleLogin() {
      const { success, error } = await login(this.credentials);
      if (!success) {
        this.errorMessage = error;
        this.popupTriggers.responseTrigger = true;
      } else {
        //this.showOTPVerification = true;
        this.$router.push('/lobby');
        VueCookies.set('session_cookie', 'futurojwt', '3600000');
      }
    },
    redirectToIntra() {

      //De momento redirigimos al churro de url (contruida a pelo con los valores client_id, redirect_uri... de la pagina de app de la intra). Al ser siempre la misma, igual no estrictamente necesario crear un endpoint para construirla. 
      const externalURL ='https://api.intra.42.fr/oauth/authorize?client_id=u-s4t2ud-6b7efca18b23485e50a6d9bc6df43ecc1024f25f5cf92dc6fd473fcc8647e21c&redirect_uri=http%3A%2F%2Flocalhost%3A25671%2Fapi%2Flogin%2Fintra%2Fcallback&response_type=code';
      const windowFeatures = 'width=400,height=400,resizable=yes,scrollbars=yes';
      window.open(externalURL, windowFeatures); //Abre pesatña y no ventana

    }
  }
};

</script>
  
<style scoped>

.login-container
{
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}
    
.login-form 
{
  width: 15%;
  padding: 20px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  width:50vh;
}
  
.form-group 
{
    margin-bottom: 15px;
}
  
label 
{
  display: block;
  margin-bottom: 5px;
}
  
input[type="text"], input[type="password"] 
{
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
}
  
button 
{
  background-color: #4CAF50;
  color: white;
  padding: 10px 15px;
  margin: 10px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  width: 100%;
}

button:hover 
{
  background-color: #45a049;
}

.button_intra{
  background-color: black;
  color: white;
  padding: 10px 15px;
  margin-top: 10px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  width: 100%;
  hover: 
}
.button_intra:hover {
  background-color: black; 
}

</style>