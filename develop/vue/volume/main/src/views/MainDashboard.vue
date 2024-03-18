<template>
    <div class="flex min-h-screen">
        <SideBar/>
        <div class="main-content flex-grow p-4 transition-margin duration-300 ease-in-out">
            <div class="grid grid-cols-3 gap-4 w-full h-full">
                <div class="bg-blue-500 text-white p-6 rounded-lg max-h-40 shadow-lg overflow-auto flex flex-col min-h-full hide-scrollbar">
                    <ul class="w-full">
                        <li v-for="num in 20" :key="num" class="py-2">Jugador {{ num }} 1500</li>
                    </ul>
                </div>
                <div class="bg-green-500 text-white p-6 rounded-lg shadow-lg flex items-center justify-center col-span-2">
                    Mini perfil card
                </div>
                <div class="bg-yellow-500 text-white p-6 rounded-lg shadow-lg flex items-center justify-center">
                    Noticias quotes o cosas de relevancia 
                </div>
                <div class="bg-red-500 text-white p-6 rounded-lg shadow-lg flex items-center justify-center">
                    Historial de partidas
                </div>
                <div class="bg-indigo-500 text-white p-6 rounded-lg shadow-lg flex items-center justify-center">
                    Amigos conectados e invitaciones
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import SideBar from '@/components/SideBar';

export default {
    name: 'MainDashboard',
    components: {
        SideBar  
    }
}
</script>

<style scoped>
.wrapper {
    display: flex;
    flex-direction: row;
    height: 100vh;
    width: 100%;
    background-color: #f4f4f4;
    transition: margin-left .25s ease-in-out;
}

.is-expanded .main-content {
    margin-left: 260px;
}

.main-content {
    flex-grow: 1; 
    transition: margin-left .25s ease-in-out; 
}

.hide-scrollbar::-webkit-scrollbar {
    display: none; /* para Chrome, Safari, y Opera */
}

.hide-scrollbar {
    -ms-overflow-style: none;  /* para Internet Explorer, Edge */
    scrollbar-width: none;  /* para Firefox */
}
</style>