<template>
    <div class="flex min-h-screen">
        <SideBar/>
        <!-- Contenedor Principal que se extiende completamente -->
        <div class="main-content flex-grow p-4">
            <a>Algo por aqui logo del proyecto o algo</a>
            <div class=" profile-container w-full h-screen bg-gray-300 shadow-md rounded-lg p-6 overflow-auto">
                <h2 class="text-2xl font-bold mb-4">Editar Perfil</h2>
                <form class="space-y-4">
                    <!-- Image Upload -->
                    <div>
                        <label for="image" class="block text-sm font-medium text-black-300">Imagen de Perfil</label>
                        <input type="file" id="image" name="image" 
                            @change="handleImageUpload"
                            class="mt-1 block w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-md shadow-sm text-white focus:outline-none focus:border-blue-500">
                    </div>
                    <!-- Nombre -->
                    <div>
                        <label for="name" class="block text-sm font-medium text-black-300">Nombre</label>
                        <input type="text" id="name" name="name"
                            v-model="formData.username"
                            class="mt-1 block w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 text-white">
                    </div>
                    <!-- Correo Electrónico -->
                    <div>
                        <label for="email" class="block text-sm font-medium text-black-300">Porreo Electrónico</label>
                        <input type="email" id="email" name="email" 
                            v-model="formData.email"
                            class="mt-1 block w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 text-white">
                    </div>
                    <!-- Biografía -->
                    <div>
                        <label for="bio" class="block text-sm font-medium text-black-300">Biografía</label>
                        <textarea id="bio" name="bio" rows="3"
                            v-model="formData.bio"
                            class="mt-1 block w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 text-white"></textarea>
                    </div>
                    <!-- Botón de Guardar Cambios -->
                    <form class="space-y-4" @submit.prevent="handleSubmit">
                        <div>
                            <button type="submit" class="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-gray-900 bg-blue-500 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
                                Guardar Cambios
                            </button>
                        </div>
                    </form>
                </form>
            </div>
        </div>
    </div>
  
</template>
    
<script>

import SideBar from '@/components/SideBar';
import { patchGateway } from '@/methods/api/login';

export default {
    data () {
        return {
            formData : {
                username: '',
                email: '',
                bio: ''
            }
        }
    },
    methods: {

        handleImageUpload(event) {
            const file = event.target.files[0];
            this.formData.image = file;
        },

        handleSubmit() {
            console.log('Form data: ', this.formData);

            const formData = new FormData();
            formData.append('user_', JSON.stringify(this.formData)); // If `this.formData` contains the user profile data
            formData.append('image', this.formData.image); // Assuming `this.formData.image` is the file

            // Use FormData with your request instead of JSON
            const res = patchGateway('/user/profile', formData);
            console.log("start");
            for (let [key, value] of formData.entries()) {
                console.log(key, value);
            }
            console.log("end");


            console.log(res);
        }
    },
    name: 'ProfileView',
    components: {
        SideBar, 
    }
}
</script>
    
  
<style scoped>
  
  
</style>
    
    