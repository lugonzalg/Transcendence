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
                <div class="user-card bg-green-500 text-white p-6 rounded-lg shadow-lg flex items-center col-span-2">
                    <div class="image-container flex-none">
                        <img :src="userProfile.avatarUrl" alt="User's profile picture" class="w-full h-auto rounded-full">
                    </div>
                    <div class="text-container flex-grow">
                        <p class="text-lg font-semibold">{{ userProfile.username }}</p>
                        <p>{{ userProfile.additionalInfo }}</p>
                    </div>
                </div>
                <div class="bg-yellow-500 text-white p-6 rounded-lg shadow-lg flex items-center justify-center">
                    Noticias quotes o cosas de relevancia 
                </div>
                <div class="bg-red-500 text-white p-6 rounded-lg shadow-lg flex items-center justify-center">
                    Historial de partidas
                </div>
                <div class="bg-indigo-500 text-white p-6 rounded-lg shadow-lg flex items-center justify-center">
                    <div class="user-list-container">
                        <input class="bg-white text-black p-2 rounded" v-model="searchQuery" placeholder="Search for friends...">
                        <button @click="addFriend" class="bg-blue-500 text-white p-2 rounded">Add</button>
                        <ul class="list-none">
                            <li v-for="friend in friends" :key="friend.id" class="flex items-center py-2 space-x-4"
                                
                                :class="{
                                    'bg-blue-800': friend.status === 'pending' || friend.status === 'sent',
                                    'bg-yellow-500': friend.challenge === 1 || friend.challenge === 2
                                }">

                                <!-- Status Circle -->
                                <span
                                    :class="{
                                        'bg-green-500': friend.online,
                                        'bg-red-500': !friend.online
                                    }"
                                    class="inline-block w-3 h-3 rounded-full"></span>

                                <!-- Friend's Username -->
                                <span>{{ friend.username }}</span>

                                <!-- Challenge Notification Badge -->
                                <span v-if="friend.challenge === 2" class="bg-yellow-500 text-black p-1 rounded text-xs">
                                    Challenge Sent!
                                </span>
                                <div v-if="friend.challenge === 1" class="space-x-2">
                                    <!-- Challenge Received Badge -->
                                    <span class="bg-yellow-500 text-black p-1 rounded text-xs">
                                        Challenge Received!
                                    </span>
                                    <!-- Accept and Deny Buttons for Challenge -->
                                    <button @click="acceptChallenge(friend)" class="bg-blue-500 text-white p-1 rounded text-xs inline-flex items-center">
                                        &#x2714; Accept
                                    </button>
                                    <button @click="denyChallenge(friend)" class="bg-red-500 text-white p-1 rounded text-xs inline-flex items-center">
                                        &#x2716; Deny
                                    </button>
                                </div>

                                <div v-if="friend.challenge === 0" class="space-x-2">
                                    <!-- Buttons for pending friend requests -->
                                    <button v-if="friend.status === 'pending'" @click="acceptFriend(friend)" class="bg-blue-500 text-white p-1 rounded text-xs inline-flex items-center">
                                        &#x2714; Accept
                                    </button>
                                    <button v-if="friend.status === 'pending'" @click="denyFriend(friend)" class="bg-red-500 text-white p-1 rounded text-xs inline-flex items-center">
                                        &#x2716; Deny
                                    </button>

                                    <!-- Buttons for accepted friends -->
                                    <div v-if="friend.status === 'accepted'" class="space-x-2">
                                        <button v-if="friend.online" @click="startMatch(friend)" class="bg-green-500 text-white p-1 rounded text-xs inline-flex items-center">
                                            &#127919; Play
                                        </button>
                                        <button @click="denyFriend(friend)" class="bg-red-500 text-white p-1 rounded text-xs inline-flex items-center">
                                            &#10060; Delete
                                        </button>
                                    </div>
                                </div>

                                <!-- Accepted Challenge (Swords) -->
                                <div v-if="friend.challenge === 3" class="space-x-2">
                                    <span class="bg-red-500 text-white p-1 rounded text-xs inline-flex items-center">
                                        &#9876; Challenge Accepted!
                                    </span>
                                </div>
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>

import ws from '@/services/websocket'
import SideBar from '@/components/SideBar';
import { getGateway, postGateway } from '@/methods/api/login';

export default {
    name: 'MainDashboard',
    components: {
        SideBar  
    },
    data() {
        return {
            userProfile: {
                avatarUrl: '/avatar/default.png',
                username: 'default',
                additionalInfo: 'Some info',
            },
        friends: [], // To store the list of users
        searchQuery: '', // For the search input
        chatSocket: null
        };
    },
    mounted() {
        this.userEvents();
    },
    async created() {
        const user_profile = await getGateway('/user/profile');

        if (user_profile != null) {
            this.userProfile.avatarUrl = user_profile.avatar;
            this.userProfile.username = user_profile.username;
        }

        await this.fetchFriends();
    },
    methods: {
        async addFriend() {

            try {
                const res = await postGateway('/user/add', {username: this.searchQuery});
                if (res) {

                    const newFriend = {
                        username: res.username,
                        status: 'sent',
                        id: res.id
                    };

                    this.friends.push(newFriend);
                }
            } catch (error) {
                console.error("Error fetching users:", error);
            }
        },
        async startMatch(friend) {
            // Implementation of starting a match with this friend
            console.log(`Starting match with ${friend.username}`);
            // Add your match starting logic here
            const res = postGateway('/user/challenge', {id: friend.id})

            if (res) {
                friend.challenge = 2;
            }
        },
        async denyFriend(friend) {
            // Remove the friend from the list or change status
            // Optionally, notify server about the denial

            try {
                const response = await postGateway('/user/friend/request', {id: friend.id, status: 0});
                if (response) {

                    const index = this.friends.findIndex(f => f.id === friend.id);
                    if (index != -1) {
                        this.friends.splice(index, 1);
                    }
                }
                friend.status = 'denied';
            } catch (error) {
                console.error("Error denying friend request:", error);
            }
        },
        async acceptFriend(friend) {
            // Example: Update friend status locally

            // Optionally, send this information to the server
            try {
                await postGateway('/user/friend/request', {id: friend.id, status: 1});
                friend.status = 'accepted';
            } catch (error) {
                console.error("Error accepting friend request:", error);
            }
        },
        async acceptChallenge(friend) {

            const res = postGateway('/user/challenge/response', {response: 1, id: friend.id});
            if (res) {

                const index = this.friends.findIndex(f => f.id === friend.id);

                if (index != -1) {
                    this.friends[index].challenge = 3;
                }
            }
        },
        async denyChallenge(friend) {

            const res = postGateway('/user/challenge/response', {response: 0, id: friend.id});
            if (res) {
                const index = this.friends.findIndex(f => f.id === friend.id);

                if (index != -1) {
                    this.friends[index].challenge = 0;
                }
                console.log(res);
            }
        },
        async fetchFriends() {
            try {
                this.friends = await getGateway('/user/friend/list');

                console.log('friends: ', this.friends);

                this.friends.forEach((friend) => {

                    console.log('friend object', friend);
                    if (friend.status == 1)
                        friend.status ='pending';
                    else if (friend.status == 0)
                        friend.status ='sent';
                    else
                        friend.status ='accepted';
                });
            } catch (error) {
                console.error("Error fetching friends:", error);
            }
        },
        async userEvents() {
            // Replace with your WebSocket URL
            console.log("Initialize websocket");
            this.chatSocket = ws;

            this.chatSocket.onmessage = (event) => {
                const data = JSON.parse(event.data);
                console.log('user event: ', data.type);
                const info = data.message;

                if (data.type == 1) { //add user
                    const newFriend = {
                        username: info.username,
                        status: 'pending',
                        id: info.id,
                        challenge: info.challenge,
                        online: info.online
                    };

                    this.friends.push(newFriend);
                }
                else if (data.type == 2) { //accept user
                    const index = this.friends.findIndex(f => f.id === info.id);

                    if (index != -1) {
                        this.friends[index].status = 'accepted';
                        this.friends[index].online = info.online;
                        this.friends[index].challenge = info.challenge;
                        console.log(this.friends[index]);
                    }

                }
                else if (data.type == 3) { //decline user

                    const index = this.friends.findIndex(f => f.id === info.id);

                    if (index != -1) {
                        this.friends.splice(index, 1);
                    }
                }
                else if (data.type == 4) { //receive challenge

                    const index = this.friends.findIndex(f => f.id === info.id);

                    if (index != -1) {
                        this.friends[index].challenge = 1;
                    }
                }
                else if (data.type == 5) { //accept challenge

                    const index = this.friends.findIndex(f => f.id === info.id);

                    if (index != -1) {
                        this.friends[index].challenge = 3;
                    }
                    //jump to game create connection
                }
                else if (data.type == 6) { //decline challenge

                    const index = this.friends.findIndex(f => f.id === info.id);

                    if (index != -1) {
                        this.friends[index].challenge = 0;
                    }
                }
                else if (data.type == 7) {
                    console.log("add user to tournament");
                }
                else if (data.type == 8) { //create match
                    //console.log(info);
                    localStorage.setItem("view", JSON.stringify(info["view"]));
                    localStorage.setItem("p1", JSON.stringify(info["1"]));
                    localStorage.setItem("p2", JSON.stringify(info["2"]));
                    
                    // In a component
                    this.$router.push({ path: '/game'});
                }
                //document.getElementById('chat-log').value += (data.message + '\n');
            };

            this.chatSocket.onclose = (event) => {
                console.log(event);
                console.log('Chat socket closed unexpectedly');
            };
        }
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

.user-card {
    display: flex;
    align-items: center;
}

.image-container {
    flex: 0 0 25%; /* Fixed 25% width */
    max-width: 25%;
}

.text-container {
    flex: 1; /* Takes the remaining space */
}

img {
    max-width: 100%; /* Ensures image is responsive within its container */
    height: auto; /* Keeps the aspect ratio of the image */
}

.user-list-container {
    display: flex;
    flex-direction: column;
    width: 100%;
}

ul.list-none {
    padding: 0;
    margin-top: 10px;
    overflow-y: auto;
    max-height: 300px; /* Adjust based on your design */
}

li {
    margin-bottom: 10px;
}

#addFriend {
    margin-bottom: 10px;
    /* Add more styling */
}

#userList {
    list-style-type: none;
    /* Style for the user list */
}

.bg-blue-800 {
    background-color: #1e3a8a; /* This is the typical dark blue color in Tailwind */
}

.text-xs {
    font-size: 0.75rem; /* Smaller text size */
}
.inline-flex {
    display: inline-flex;
    align-items: center; /* Center items vertically */
}
.p-1 {
    padding: 0.25rem; /* Smaller padding */
}

.bg-green-500 {
    background-color: #10B981; /* Adjust this to your preferred green color */
}

.bg-red-500 {
    background-color: #EF4444; /* Adjust this to your preferred red color */
}

.inline-block {
    display: inline-block;
}

.w-3 {
    width: 12px; /* Adjust to your desired size */
}

.h-3 {
    height: 12px; /* Adjust to your desired size */
}

.rounded-full {
    border-radius: 9999px; /* Makes the div circular */
}

.mr-2 {
    margin-right: 8px; /* Adjust spacing as needed */
}

.bg-yellow-500 {
    background-color: #F59E0B; /* Yellow color */
}

.text-black {
    color: black;
}

.p-1 {
    padding: 0.25rem; /* Adjust padding */
}

.rounded {
    border-radius: 0.25rem;
}

.text-xs {
    font-size: 0.75rem;
}

.bg-yellow-200 {
    background-color: #FEF3C7; /* Light yellow shade */
}

</style>