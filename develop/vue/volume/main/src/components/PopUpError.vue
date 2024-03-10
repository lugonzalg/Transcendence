<template>
  <div class="popup">
    <div class="popup-inner">
      <p>{{ errorMessage }}</p>
      <button @click="close" class="popup-close">Cerrar</button>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    errorMessage: String
  },
  data() {
    return {
      isVisible: true
    };
  },
  methods: {
    close() {
      this.isVisible = false;
      this.$emit('close');
    }
  }
}
</script>

<style lang="scss" scoped>
.popup{
  position:fixed;
  top:0;
  left:0;
  right:0;
  bottom:0;
  z-index:99;
  background-color: rgba(0,0,0,0.2);
  display: flex;
  align-items: center;
  justify-content: center;
}

.popup-inner{
  background: white;
  padding: 32px;
}
</style>
  