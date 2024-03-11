<template>
    <div class="displaySquare" :style="{ backgroundColor: backgroundColor }">
      <h3>{{ title }}</h3>
      <p>{{ description }}</p>
    </div>
  </template>
  
  <script>
  export default {
    name: 'displaySquare',
    props: {
      title: String,
      description: String,
      backgroundColor: String,
    },
  };
  </script>
  
  <style>
  .square {
    width: 200px; 
    height: 200px; 
    padding: 20px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    margin: 10px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
  }
  </style>
  