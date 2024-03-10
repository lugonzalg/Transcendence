import axios from 'axios';

const axiosInstance = axios.create({

    baseURL: 'http://localhost:4242/api/',
    timeout: 1000 // Timeout porsiaca ya haremos pruebas
    //headers: {'X-Custom-Header': 'foobar'} Aqui meteremos el bearer por ejemplo
});

export default axiosInstance;