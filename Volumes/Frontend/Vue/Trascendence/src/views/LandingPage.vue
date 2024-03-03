<template>

  <DefaultNavbar2/>
  <div class="d-flex justify-content-center align-items-center" style="height: 100vh;">
    <div class="text-center d-flex flex-column align-items-center">
      <h1 class="title-custom-font fs-1">Transcendence</h1>
      <div class="d-flex justify-content-center">
        <button class="btn btn-primary m-2">Acceder</button>
        <button class="btn btn-primary m-2">Registro</button>
      </div>
    </div>
  </div>

</template>
    
<script>
  import DefaultNavbar2 from '@/components/DefaultNavbar2.vue';

  export default 
  {
    name: 'LandingPage',
    componentes:
    {
      DefaultNavbar2,
    },
    components: { DefaultNavbar2 }
  }

</script>
    

<style scoped>

  .title-custom-font
  {
    font-family: Squid;
    src: url('~@/assets/Fonts/Game Of Squids.ttf');
  }

</style>
    
    