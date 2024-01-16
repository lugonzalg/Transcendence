<template>
  <DefaultNavbar></DefaultNavbar>
  <div class="login-container" v-if="!showOTPVerification">
    <div class="login-info">
    </div>
    <div class="login-form">
      <h2>Iniciar Sesión</h2>
      <form @submit.prevent="login">
        <div class="form-group">
          <label for="username">Usuario:</label>
          <input type="text" id="username" v-model="credentials.username">
        </div>
        <div class="form-group">
          <label for="password">Contraseña:</label>
          <input type="password" id="password" v-model="credentials.password">
        </div>
        <button type="submit">Iniciar Sesión</button>
      </form>
    </div>
  </div>
  <OTPVerification v-if="showOTPVerification"></OTPVerification>
</template>
  
<script>

import axios from 'axios';
import DefaultNavbar from '../components/DefaultNavbar.vue';
import OTPVerification from '../components/OtpVerification.vue';

export default {
    name: 'LoginView',
    components: {
        DefaultNavbar,
        OTPVerification
    },
    data() {
        return {
            credentials: {
                username: '',
                password: ''
            }
        };
    },
    methods: {
        async login() {
            try {
                const response = await axios.post('lukas/api/login:5000', this.credentials);
                console.log(response.data);
                if (response.status === 200) {
                  console.log(response.data);
                  this.showOTPVerification = true;
            }
              }
            catch (error) {
                console.error('Error de inicio de sesión:', error);
            }
        }
    }

};

</script>
  
  <style scoped>

  .login-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
  }
    
  .login-form {
    width: 15%;
    padding: 20px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  }
  
  .form-group {
    margin-bottom: 15px;
  }
  
  label {
    display: block;
    margin-bottom: 5px;
  }
  
  input[type="text"], input[type="password"] {
    width: 100%;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 4px;
  }
  
  button {
    background-color: #4CAF50;
    color: white;
    padding: 10px 15px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    width: 100%;
  }
  
  button:hover {
    background-color: #45a049;
  }

  </style>
  