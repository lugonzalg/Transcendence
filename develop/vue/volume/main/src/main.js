import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import 'bootstrap/dist/css/bootstrap.min.css';
import VueCookies from 'vue-cookies';
import secrets from './../secrets.json'; 

/*
    Inicialización de la aplicación Vue 2-3
    Importación de librerías globales
    Configuración global
    Estilos globales
    Importacion del componente raiz App.vue
    Integración de otras herramientas
*/

const app = createApp(App);
app.use(router);
app.use(VueCookies);
app.mount('#app');
