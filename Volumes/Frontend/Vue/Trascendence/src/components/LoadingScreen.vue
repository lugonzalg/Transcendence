<template>
  <div class="loader-wrapper">
    <div class="loader"></div>
  </div>
</template>

<script>
export default {
  name: 'LoadingScreen'
};
</script>

<style scoped>
  .loader-wrapper {
    display: flex;
    justify-content: center;
    align-items: center;
    position: fixed; /* Cubre toda la ventana del navegador */
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: black; /* Fondo totalmente negro */
  }

  .loader {
    width: 100px;
    height: 100px;
    box-shadow: 0px 20px 40px #ff4646, 0px -20px 40px #8949ff, 20px 0px 40px #ff07fb, -20px 0px 40px #ff07fb;
    border-radius: 10em;
    animation: rotate 1s linear infinite;
  }

  @keyframes rotate {
    from {
      transform: rotate(0deg);
    }
    to {
      transform: rotate(360deg);
    }
  }
</style>

  