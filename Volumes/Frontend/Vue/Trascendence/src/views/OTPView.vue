<template>
  <DefaultNavbar></DefaultNavbar>

  <div class="otp-view">
    <div class="otp-form-container">
      <p>OTP View</p>
      <form @submit.prevent="verifyOTP">
        <input v-model="otp" type="text" placeholder="Enter OTP" />
        <button type="submit">Verify</button>
      </form>
    </div>
  </div>
</template>
    
<script>
import DefaultNavbar from '@/components/DefaultNavbar.vue';

export default {
  name: 'OTPView',
  components: {
    DefaultNavbar
  },
  data() {
    return {
      otp: ''
    };
  },
  methods: {
    verifyOTP() {
      // OTP verification logic goes here
      console.log('Entered OTP:', this.otp);
      this.otp = '';
    }
  }
}
</script>
    
<style>
.otp-view {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh; /* Use full viewport height */
}

.otp-form-container {
  text-align: center;
}

input {
  margin-bottom: 10px;
}

button {
  margin-top: 10px;
}
</style>