<script setup>

import Modal from '@/components/GameModal.vue'

import { ref, onMounted, onBeforeUnmount } from 'vue';

import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
import * as THREE from 'three';
import { getGateway } from '@/methods/api/login';

const showModal = ref(true)

const target = ref();


// Create the scene, camera, and renderer
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
camera.position.z = 5;

// Define a dashed line material
const dashedMaterial = new THREE.LineDashedMaterial({
  color: 0xffffff,
  dashSize: 0.5, // Adjust for longer dashes
  gapSize: 0.3, // Wider gaps for more distinct segments
});

// Function to create a 3D dashed paddle with fewer lines
function createDashedPaddle(xPos) {
  const paddleWidth = 1;
  const paddleHeight = 1;
  const paddleDepth = 4;

  // Define fewer vertices for the paddle edges
  const paddleEdges = [
    // Bottom face
    new THREE.Vector3(-paddleWidth / 2, -paddleHeight / 2, -paddleDepth / 2),
    new THREE.Vector3(paddleWidth / 2, -paddleHeight / 2, -paddleDepth / 2),
    new THREE.Vector3(paddleWidth / 2, -paddleHeight / 2, paddleDepth / 2),
    new THREE.Vector3(-paddleWidth / 2, -paddleHeight / 2, paddleDepth / 2),
    new THREE.Vector3(-paddleWidth / 2, -paddleHeight / 2, -paddleDepth / 2),

    // Top face
    new THREE.Vector3(-paddleWidth / 2, paddleHeight / 2, -paddleDepth / 2),
    new THREE.Vector3(paddleWidth / 2, paddleHeight / 2, -paddleDepth / 2),
    new THREE.Vector3(paddleWidth / 2, paddleHeight / 2, paddleDepth / 2),
    new THREE.Vector3(-paddleWidth / 2, paddleHeight / 2, paddleDepth / 2),
    new THREE.Vector3(-paddleWidth / 2, paddleHeight / 2, -paddleDepth / 2),

    // Connecting lines between top and bottom faces
    new THREE.Vector3(-paddleWidth / 2, -paddleHeight / 2, -paddleDepth / 2),
    new THREE.Vector3(-paddleWidth / 2, paddleHeight / 2, -paddleDepth / 2),
    new THREE.Vector3(paddleWidth / 2, -paddleHeight / 2, -paddleDepth / 2),
    new THREE.Vector3(paddleWidth / 2, paddleHeight / 2, -paddleDepth / 2),
    new THREE.Vector3(paddleWidth / 2, -paddleHeight / 2, paddleDepth / 2),
    new THREE.Vector3(paddleWidth / 2, paddleHeight / 2, paddleDepth / 2),
    new THREE.Vector3(-paddleWidth / 2, -paddleHeight / 2, paddleDepth / 2),
    new THREE.Vector3(-paddleWidth / 2, paddleHeight / 2, paddleDepth / 2)
  ];

  // Create the paddle geometry and dashed line object
  const geometry = new THREE.BufferGeometry().setFromPoints(paddleEdges);
  const line = new THREE.LineSegments(geometry, dashedMaterial);
  line.computeLineDistances(); // Enable dashing
  line.position.set(xPos, 0.51, 0); // Position the paddle
  return line;
}

// Create paddles
const p1_paddle = createDashedPaddle(-6.5);
const p2_paddle = createDashedPaddle(8);

// Add paddles to the scene
scene.add(p1_paddle);
scene.add(p2_paddle);

// Position paddles
p1_paddle.position.set(-6.5, 0.51, 0);
p2_paddle.position.set(8, 0.51, 0);

// Set the camera position behind p1_paddle and face p2_paddle
camera.position.set(-10, 5, 0); // Adjust the x-axis to be behind the first paddle
camera.lookAt(p2_paddle.position); // Make the camera look toward p2_paddle

// Initialize OrbitControls
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.05;

// Minimalist Field
const fieldWidth = 20; // Adjust as needed
const fieldHeight = 15;

// Create a dashed material for the field lines
const fieldDashedMaterial = new THREE.LineDashedMaterial({
  color: 0xffffff, // White color for field lines
  dashSize: 0.5,   // Length of dashes
  gapSize: 0.3,    // Gaps between dashes
});

// Function to create a dashed rectangular field with a centerline
function createDashedField(fieldWidth, fieldHeight) {
  const fieldGroup = new THREE.Group();

  // Define the field boundary points
  const boundaryPoints = [
    new THREE.Vector3(-fieldWidth / 2, 0, -fieldHeight / 2), // Bottom-left
    new THREE.Vector3(-fieldWidth / 2, 0, fieldHeight / 2),  // Top-left
    new THREE.Vector3(fieldWidth / 2, 0, fieldHeight / 2),   // Top-right
    new THREE.Vector3(fieldWidth / 2, 0, -fieldHeight / 2),  // Bottom-right
    new THREE.Vector3(-fieldWidth / 2, 0, -fieldHeight / 2)  // Close the loop
  ];

  // Create a dashed line for the field boundary
  const boundaryGeometry = new THREE.BufferGeometry().setFromPoints(boundaryPoints);
  const boundaryLine = new THREE.Line(boundaryGeometry, fieldDashedMaterial);
  boundaryLine.computeLineDistances(); // Enable dashing
  fieldGroup.add(boundaryLine);

  // Create a dashed line for the midline
  const midlinePoints = [
    new THREE.Vector3(0, 0, -fieldHeight / 2), // Bottom-center
    new THREE.Vector3(0, 0, fieldHeight / 2)   // Top-center
  ];
  const midlineGeometry = new THREE.BufferGeometry().setFromPoints(midlinePoints);
  const midlineLine = new THREE.Line(midlineGeometry, fieldDashedMaterial);
  midlineLine.computeLineDistances(); // Enable dashing
  fieldGroup.add(midlineLine);

  return fieldGroup;
}

// Create and position the dashed field
const field = createDashedField(fieldWidth, fieldHeight);
field.position.y = 0.01; // Slightly above the plane to prevent z-fighting
scene.add(field);

// Set the renderer background to black or transparent
renderer.setClearColor(0x000000, 1); // Black background

// Function to create a 3D dashed disc
function createDashedDiscWithPerimeters(radius, numVerticalLines = 6, thickness = 0.5) {
  const discGroup = new THREE.Group();
  const discHeightOffset = thickness / 2;

  // Create the top and bottom perimeter circles
  const topCirclePoints = [];
  const bottomCirclePoints = [];

  for (let i = 0; i <= numVerticalLines; i++) {
    const angle = (i / numVerticalLines) * 2 * Math.PI;
    const x = Math.cos(angle) * radius;
    const z = Math.sin(angle) * radius;

    topCirclePoints.push(new THREE.Vector3(x, discHeightOffset, z));
    bottomCirclePoints.push(new THREE.Vector3(x, -discHeightOffset, z));
  }

  // Create dashed line for the top circle
  const topCircleGeometry = new THREE.BufferGeometry().setFromPoints(topCirclePoints);
  const topCircleLine = new THREE.Line(topCircleGeometry, dashedMaterial);
  topCircleLine.computeLineDistances(); // Enable dashing
  discGroup.add(topCircleLine);

  // Create dashed line for the bottom circle
  const bottomCircleGeometry = new THREE.BufferGeometry().setFromPoints(bottomCirclePoints);
  const bottomCircleLine = new THREE.Line(bottomCircleGeometry, dashedMaterial);
  bottomCircleLine.computeLineDistances(); // Enable dashing
  discGroup.add(bottomCircleLine);

  // Create vertical lines connecting the top and bottom circles
  for (let i = 0; i < numVerticalLines; i++) {
    const angle = (i / numVerticalLines) * 2 * Math.PI;
    const x = Math.cos(angle) * radius;
    const z = Math.sin(angle) * radius;

    const verticalPoints = [
      new THREE.Vector3(x, discHeightOffset, z),
      new THREE.Vector3(x, -discHeightOffset, z)
    ];

    // Create dashed line for the vertical connection
    const verticalGeometry = new THREE.BufferGeometry().setFromPoints(verticalPoints);
    const verticalLine = new THREE.Line(verticalGeometry, dashedMaterial);
    verticalLine.computeLineDistances(); // Enable dashing
    discGroup.add(verticalLine);
  }

  return discGroup;
}

// Create and position the 3D dashed disc
const ball = createDashedDiscWithPerimeters(0.5, 8, 0.2); // Adjust parameters as needed
ball.position.set(0, 0.5, 0);
scene.add(ball);

// Define ball velocity and initial direction
const ballVelocity = new THREE.Vector3(0.05, 0, 0.00); // Adjust speed values as needed

// Initialize player scores
let p1Score = 0;
let p2Score = 0;

function updateScoreboard() {
  // Update the score text of each player without affecting the images
  document.querySelector("#p1_score span").innerText = `P1: ${p1Score}`;
  document.querySelector("#p2_score span").innerText = `P2: ${p2Score}`;
}

// Flash duration and particle material
const flashDuration = 100;
const particleMaterial = new THREE.PointsMaterial({ color: 0xff0000, size: 0.1 });

// Function to flash an object
function flashObject(object, flashColor) {
  const originalMaterial = object.material;
  object.material = new THREE.MeshBasicMaterial({ color: flashColor });

  setTimeout(() => {
    object.material = originalMaterial;
  }, flashDuration);
}

// Set the initial speed factor for the ball
let speedFactor = 1.1; // Increase this value to make the ball speed up faster
let maxSpeed = 1; // Set a limit on how fast the ball can move
// Paddle width and collision boundaries (adjust to fit the paddle size)
const paddleWidth = 4;

// Function to increase ball speed
function increaseBallSpeed() {
  ballVelocity.multiplyScalar(speedFactor);

  // Cap the speed if it exceeds the maximum
  if (ballVelocity.length() > maxSpeed) {
    ballVelocity.setLength(maxSpeed);
  }
}

// Function to handle ball deflection based on paddle collision
function deflectBall(paddle, direction) {
  // Calculate the relative position of the ball on the paddle
  const relativeIntersectZ = ball.position.z - paddle.position.z;
  const normalizedRelativeIntersectionZ = (relativeIntersectZ / (paddleWidth / 2));
  const bounceAngle = normalizedRelativeIntersectionZ * (Math.PI / 4); // Up to 45-degree bounce

  // Adjust the ball's velocity based on the bounce angle
  ballVelocity.x = direction * Math.cos(bounceAngle) * Math.abs(ballVelocity.x);
  ballVelocity.z = Math.sin(bounceAngle) * Math.abs(ballVelocity.x);

  // Increase ball speed after deflection
  increaseBallSpeed();

  // Flash paddle and create particle burst
  flashObject(paddle, 0xff0000);
  //createParticleBurst(ball.position);
}

// Update the ball position and detect collisions
function updateBall() {
  // Move the ball based on its current velocity
  ball.position.add(ballVelocity);

  // Check for collisions with P1 paddle
  if (ball.position.x - 0.5 < p1_paddle.position.x + 0.5 &&
      ball.position.x + 0.5 > p1_paddle.position.x - 0.5 &&
      ball.position.z > p1_paddle.position.z - 2 &&
      ball.position.z < p1_paddle.position.z + 2) {
    deflectBall(p1_paddle, 1); // Bounce to the right (positive x direction)
  }

  // Check for collisions with P2 paddle
  else if (ball.position.x + 0.5 > p2_paddle.position.x - 0.5 &&
           ball.position.x - 0.5 < p2_paddle.position.x + 0.5 &&
           ball.position.z > p2_paddle.position.z - 2 &&
           ball.position.z < p2_paddle.position.z + 2) {
    deflectBall(p2_paddle, -1); // Bounce to the left (negative x direction)
  }

  // Check for boundary collisions (top and bottom)
  if (ball.position.z - 0.5 < -fieldHeight / 2 || ball.position.z + 0.5 > fieldHeight / 2) {
    ballVelocity.z = -ballVelocity.z; // Invert the z-axis velocity
  }

  // Update scores and reset ball if it goes out of bounds horizontally
  if (ball.position.x - 0.5 < -fieldWidth / 2) {
    p2Score++; // P2 gains a point
    resetBall();
  } else if (ball.position.x + 0.5 > fieldWidth / 2) {
    p1Score++; // P1 gains a point
    resetBall();
  }

  updateEnvironment(); // Check and update environment visuals
  updateScoreboard(); // Refresh scoreboard display
}

// Create wireframe materials for the flash state
const paddleWireframeMaterial = new THREE.MeshBasicMaterial({ color: 0x00aa00, wireframe: true });
const ballWireframeMaterial = new THREE.MeshBasicMaterial({ color: 0xff0000, wireframe: true });

// Ensure flashes start when scores reach a high threshold
function updateEnvironment() {
  const maxScore = Math.max(p1Score, p2Score);
  
  if (maxScore >= 8) {
    const ratio = 0.5;//(maxScore - 8) / 2;
    const fieldColor = new THREE.Color(0.2 + 0.8 * ratio, 0, 0);
    scene.background = new THREE.Color(0.1 + 0.4 * ratio, 0, 0);

  } else {
    //field.material.color.set(0x333333);
    scene.background = new THREE.Color(0x000000);
  }
}

// Function to reset the ball to the center
function resetBall() {
  ball.position.set(0, 0.5, 0);
  ballVelocity.set((Math.random() > 0.5 ? 1 : -1) * 0.05, 0, (Math.random() > 0.5 ? 1 : -1) * 0.05); // Randomize initial direction
  
  // Apply initial speed factor
  ballVelocity.multiplyScalar(speedFactor);
}

// Track the state of keys for controlling the paddles
const keyState = {
  a: false,
  d: false,
  ArrowLeft: false,
  ArrowRight: false
};

// Event handlers for updating key states
function onKeyDown(event) {
  if (event.key in keyState) keyState[event.key] = true;
}

function onKeyUp(event) {
  if (event.key in keyState) keyState[event.key] = false;
}

// Update paddles based on the current key state
function updatePaddles() {
  const paddleSpeed = 0.1;

  // Control P1 with "a" (left) and "d" (right)
  if (p1_paddle.position.z > -5.4 && keyState.a) p1_paddle.position.z -= paddleSpeed;
  if (p1_paddle.position.z < 5.4 && keyState.d) p1_paddle.position.z += paddleSpeed;

  // Control P2 with "ArrowLeft" (left) and "ArrowRight" (right)
  if (p2_paddle.position.z > -5.4 && keyState.ArrowLeft) p2_paddle.position.z -= paddleSpeed;
  if (p2_paddle.position.z < 5.4 && keyState.ArrowRight) p2_paddle.position.z += paddleSpeed;
}

// Animation loop
function animate() {
  requestAnimationFrame(animate);

  // Update the paddles' positions
  updatePaddles();
  updateBall();
  //logCameraPosition();

  // Update controls for camera movement
  controls.update();


  // Render the updated scene
  renderer.render(scene, camera);
}

// Append the renderer's DOM element and set up resize event listener
onMounted(() => {


  const player_1 = null;
  const player_2 = null;

  console.log("Mounted", showModal.value);
  console.log("player_1", player_1);
  console.log("player_2", player_2);
  const res = getGateway('/user/profile');
  if (res) {
    console.log(res);
  }

  target.value.appendChild(renderer.domElement);

  // Add window resize event listener
  window.addEventListener('resize', resizeRenderer);

  // Add keyboard event listeners
  window.addEventListener('keydown', onKeyDown);
  window.addEventListener('keyup', onKeyUp);

  // Start the animation loop
  animate();
});

onBeforeUnmount(() => {
  // Remove event listeners on unmount
  window.removeEventListener('resize', resizeRenderer);
  window.removeEventListener('keydown', onKeyDown);
  window.removeEventListener('keyup', onKeyUp);
});

// Resize handler to adjust the camera and renderer sizes
function resizeRenderer() {
  const width = window.innerWidth;
  const height = window.innerHeight;
  renderer.setSize(width, height);
  camera.aspect = width / height;
  camera.updateProjectionMatrix();
}

function setReady() {
  playerReady.value = true;
  // Send this status to the server or check for opponent's status if necessary
}

</script>

<template>
  <div ref="target" style="width: 100%; height: 100vh;"></div>
    <Teleport to="body">
      <!-- use the modal component, pass in the prop -->
      <modal :player1="this.player_1" :player2="this.player_2" :show="showModal" @close="showModal = false">
        <template #header>
          <h3>Custom Header</h3>
        </template>
      </modal>
    </Teleport>
    <div id="scoreboard">
      <div class="score-item" id="p1_score">
        <img src="https://ikerketa.com/avatar/1.png" alt="P1 Icon">
        <span>P1: 0</span>
      </div>
      <div class="score-item" id="p2_score">
        <img src="https://ikerketa.com/avatar/1.png" alt="P2 Icon">
        <span>P2: 0</span>
      </div>
  </div>
</template>

<style>
#scoreboard {
  position: absolute;
  top: 10px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 20px;
  background-color: rgba(0, 0, 0, 0.5);
  padding: 10px;
  border-radius: 10px;
  font-size: 24px;
  color: white;
}

.score-item {
  display: flex;
  align-items: center;
  gap: 10px;
}

.score-item img {
  width: 30px;
  height: 30px;
}

</style>