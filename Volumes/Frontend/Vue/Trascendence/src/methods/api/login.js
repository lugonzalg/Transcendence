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



export {collectBrowserData , sendDataToServer, register, login};