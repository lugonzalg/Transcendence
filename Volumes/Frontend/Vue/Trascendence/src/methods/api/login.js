import axiosInstance from '../axiosService';

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
    axiosInstance.post('/login_log', data)
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
        const response = await axiosInstance.post('/create_user', credentials);
        return { success: true, data: response.data, error: null };
    } catch (error) {
        return { success: false, data: null, error: error.response.data.detail || 'Error desconocido.' };
    }
}

//LoginView @POST /login_user
async function login(credentials) {
    try {
        const response = await axiosInstance.post('/login_user', credentials);
        return { success: true, data: response.data, error: null };
    } catch (error) {
        return { success: false, data: null, error: error.response.data.detail || 'Error desconocido.' };
    }
}

async function handleIntraLogin() {
    try {
      // Redirigir al usuario a la intra
      //window.location.href = buildIntraURL(); // si buildeo la url desde el front necesito importar todas las variables de entorno del .env. Igual mejor una peticion al back?
      window.location.href = "https://api.intra.42.fr/oauth/authorize?client_id=u-s4t2ud-6b7efca18b23485e50a6d9bc6df43ecc1024f25f5cf92dc6fd473fcc8647e21c&redirect_uri=http%3A%2F%2Flocalhost%3A25671%2Fapi%2Flogin%2Fintra%2Fcallback&response_type=code";
    } catch (error) {
      console.error('Error al manejar el inicio de sesión con Intra 42:', error);
    }
}


  
export { handleIntraLogin };

export {collectBrowserData , sendDataToServer, register, login};