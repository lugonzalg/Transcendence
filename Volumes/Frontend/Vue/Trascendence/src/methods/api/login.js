import router from '@/router';
import axiosInstance from '../axiosService';
//import axios from 'axios';


// Se encarga de recoger los datos del navegador y enviarlos al servidor
// Home View
function collectBrowserData() {
    const data = {
    browserName: navigator.appName,
    browserVersion: navigator.appVersion,
    userAgent: navigator.userAgent,
    language: navigator.language,
    platform: navigator.platform,
    screenResolution: `${screen.width}x${screen.height}`,
  };
  sendDataToServer(data);
}

//HomeView @POST /login_log
async function sendDataToServer(data) {
    axiosInstance.post('https://trascendende.tech/api/login/log', data,  { timeout: 5000 })
    .then((response) => {
      console.log('Datos enviados al servidor:', response);
    })
    .catch((error) => {
      console.error('Error al enviar datos:', error);
    });
}

//RegisterView @POST /create_user
async function register(credentials) {
    try {
        const response = await axiosInstance.post('/login/register', credentials);
        return { success: true, data: response.data, error: null };

    } catch (error) {
        return { success: false, data: null, error: error.response.data.detail || 'Error desconocido.' };
    }
}

//LoginView @POST /login_user
async function login(credentials) {
    try {
        const response = await axiosInstance.post('/login/default', credentials);
        return { success: true, data: response.data, error: null };

    } catch (error) {
        if (error.response.status == 428)
            router.push('/otp');

        return { success: false, data: null, error: error.response.data.detail || 'Error desconocido.' };
    }
}

async function handleIntraRedirect() {
    try {
      // Peticion de build url al back
     // const response = await axios.get('http://localhost:4242/api/intra');
      // Redireccion a la url
      window.location.href = 'https://trascendence.tech/api/intra';
    
    } catch (error) {
      console.error('Error al manejar el inicio de sesión con Intra 42:', error);
    }
}


export { handleIntraRedirect ,collectBrowserData , sendDataToServer, register, login};
