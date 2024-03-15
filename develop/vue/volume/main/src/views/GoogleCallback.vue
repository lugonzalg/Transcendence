<template>
  <div>
    Hello World
  </div>
</template>

<script>

export default {
  mounted() {
    // Accessing route parameters
    console.log(this.$route.params);
    
    // Or if you're interested in query parameters
    console.log(this.$route.query);
  }
}
</script>

<style>
</style>