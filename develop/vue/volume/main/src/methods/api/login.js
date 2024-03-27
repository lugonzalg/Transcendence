//import router from '@/router';
import axiosInstance from '../axiosService';
//import axios from 'axios';

async function renew_token() {
  try {
    const res = getGateway('/refresh')
    console.log(res);

  } catch(error) {
    console.log(error);
  }
}

async function handle_error(error) {
  console.log(error);
  console.log(error.data);
  console.log(error.response);
  console.log(error.response.data);
  
  const err = error.response.data;

  if (err == "Expired Token") {
    renew_token();
  }
}

async function patchGateway(endpoint, data) {
  try {

    const res = await axiosInstance.patch(endpoint, data,{timeout: 1000});
    return res.data;

  } catch (error) {

      handle_error(error);
      console.error("Error in GET request: ", error);
      return null;
  }
}

async function postGateway(endpoint, data) {
  try {

    const res = await axiosInstance.post(endpoint, data,{timeout: 1000});
    return res.data;

  } catch (error) {

      handle_error(error);
      console.error("Error in GET request: ", error);
      return null;
  }
}

async function getGateway(endpoint, data) {
  try {

    const res = await axiosInstance.get(endpoint, data,{timeout: 1000});
    return res.data;

  } catch (error) {

      handle_error(error);
      console.error("Error in GET request: ", error);
      return null;
  }
}


//RegisterView @POST /create_user
async function register(credentials) {
    try {
        console.log("login/register");
        console.log("Credentials: ", credentials);
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
      if (error.response) {
        //return { success: false, data: null, error: 'Necesita verificación OTP', status: 428 };
        return { success: false, data: null, error: error.response.data.detail || 'Error desconocido.' };
      } else {
          console.error("Error making the request:", error);
          return { success: false, data: null, error: 'Necesita verificación OTP', status: 428 };
          //return { success: false, data: null, error: 'Error de red o desconocido.' };
      }
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


export { handleIntraRedirect, register, login,
  postGateway, getGateway, patchGateway};
