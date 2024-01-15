<template>
  <DefaultNavbar></DefaultNavbar>
  <div class="register-container">
    <div class="register-form">
      <h2>Registro</h2>
      <form @submit.prevent="register">
        <div class="form-group">
          <label for="username">Usuario:</label>
          <input type="text" id="username" v-model="credentials.username">
        </div>
        <div class="form-group">
          <label for="email">Email:</label>
          <input type="email" id="email" v-model="credentials.email">
        </div>
        <div class="form-group">
          <label for="password">Contraseña:</label>
          <input type="password" id="password" v-model="credentials.password">
        </div>
        <div class="form-group">
          <label for="confirmPassword">Confirmar Contraseña:</label>
          <input type="password" id="confirmPassword" v-model="confirmPassword">
        </div>
        <button type="submit" :disabled="!isFormValid">Registrarse</button>
      </form>
    </div>
  </div>
  </template>
  
  <script>
import DefaultNavbar from '@/components/DefaultNavbar.vue';

import axios from 'axios';
  export default {
    name: 'RegisterView',
    components: { DefaultNavbar },
    data() {
    return {
      credentials: {
        username: '',
        email: '',
        password: ''
      },
      confirmPassword: ''
    };
  },
  computed: {
    isFormValid() {
      return this.credentials.password === this.confirmPassword && this.credentials.email;
    }
  },
  methods: {
    async register() {
      if (!this.isFormValid) {
        alert('Las contraseñas no coinciden o el email está vacío.');
        return;
      }
      
      const response = await axios.post('http://65.109.174.85:25671/api/login/create_user', this.credentials);
                console.log(response.data);
                if (response.status === 200) {
                  console.log(response.data);
    }
  }
}
};
  </script>
  
  <style scoped>
  .register-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh; 
  }
  
  .register-form {
    width: 15%; 
    padding: 20px;
    background: white; 
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1); 
  }
  
  .form-group {
    margin-bottom: 15px;
  }
  
  label {
    display: block;
    margin-bottom: 5px;
  }
  
  input[type="text"], input[type="email"], input[type="password"] {
    width: 100%;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 4px;
    box-sizing: border-box;
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
  
  button:disabled {
    background-color: #cccccc;
    cursor: default;
  }
  </style>
  