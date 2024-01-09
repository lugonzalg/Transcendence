<template>
  <div id="app">
    <router-view></router-view>
  </div>
</template>

<script>
import axios from 'axios';

export default {

  name: 'App',
  mounted() {
    this.collectBrowserData();
  },
  methods: {
    collectBrowserData() {
      const data = {
      browserName: navigator.appName,
      browserVersion: navigator.appVersion,
      userAgent: navigator.userAgent,
      language: navigator.language,
      platform: navigator.platform,
      screenResolution: `${screen.width}x${screen.height}`,
      
    };
    this.sendDataToServer(data);
    },
    sendDataToServer(data) {
    axios.post('lukas/logs', data)
      .then(response => {
        console.log('Datos enviados al servidor:', response);
      })
      .catch(error => {
        console.error('Error al enviar datos:', error);
      });
  }
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #000000;
}
</style>
