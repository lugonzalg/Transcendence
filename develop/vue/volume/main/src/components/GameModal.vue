<script setup>

import { getGateway } from '@/methods/api/login';

const props = defineProps({
  show: Boolean,
  player1: Object,
  player2: Object
})

const handleClick = async () => {
  const res = getGateway('/game/start')

  console.log(res);
}
</script>

<template>
    <Transition name="modal">
        <div v-if="show" class="modal-mask">
            <div class="modal-container">
                <div class="modal-header">
                    <div class="player-container">
                        <div class="player player-1">
                            <img :src="player1.avatar" alt="Player 1" class="player-icon">
                            <h3>{{ player1.username }}</h3>
                        </div>
                        <h3 class="vs">vs</h3>
                        <div class="player player-2">
                            <img :src="player2.avatar" alt="Player 2" class="player-icon">
                            <h3>{{ player2.username }}</h3>
                        </div>
                    </div>
                </div>

                <div class="modal-footer">
                    <slot name="footer">
                        <p>Waiting for both players to be ready...</p>
                        <button class="modal-default-button" @click="handleClick">Start</button>
                    </slot>
                </div>

            </div>
        </div>
    </Transition>
</template>

<style>
.modal-mask {
  position: fixed;
  z-index: 9998;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.7);
  display: flex;
  transition: opacity 0.3s ease;
}

.modal-container {
  width: 400px;
  margin: auto;
  padding: 20px 30px;
  border: 2px dashed #000;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.33);
  transition: all 0.3s ease;
}

.modal-header, .modal-footer {
  padding: 10px;
  color: #000; /* Black text for better contrast */
}

.modal-header h3 {
  margin-top: 0;
  color: #000; /* Black color for the header text */
}

.modal-body {
  padding: 20px;
  background-color: #e3e3e3; /* Light gray background for the body */
  border: 1px solid #ccc; /* Subtle border */
}

.modal-default-button {
  padding: 8px 16px;
  background-color: #3b3636;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.modal-default-button:hover {
  background-color: #333; /* Darker on hover */
}

/* Enhancing entrance and exit transitions */
.modal-enter-from, .modal-leave-to {
  opacity: 0;
}

.modal-enter-from .modal-container,
.modal-leave-to .modal-container {
  transform: scale(1.1);
}

.player {
  display: flex;
  align-items: center;
  justify-content: center;
}

.player-1 {
  align-self: flex-end; /* Ensures Player 1 is on the right */
}

.player-2 {
  align-self: flex-start; /* Ensures Player 2 is on the left */
}

.player-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%; /* Ensures full use of the modal's width */
}

.vs {
  align-self: center; /* Center the 'vs' text */
}


.player-icon {
  width: 60px; /* Example size, adjust as needed */
  height: 60px; /* Maintain aspect ratio */
  border-radius: 50%; /* Circular icons */
  margin: 0 10px;
}

/*
 * The following styles are auto-applied to elements with
 * transition="modal" when their visibility is toggled
 * by Vue.js.
 *
 * You can easily play with the modal transition by editing
 * these styles.
 */

.modal-enter-from {
  opacity: 0;
}

.modal-leave-to {
  opacity: 0;
}

.modal-enter-from .modal-container,
.modal-leave-to .modal-container {
  -webkit-transform: scale(1.1);
  transform: scale(1.1);
}
</style>