<template>
    <DefaultNavbar/>
    <div class="lobby-page">   
      <div class="find_game">1

      </div>
      <div>2</div>
      <div>3</div>
      <div>4</div>
      <div>5</div>
      <div>6</div>
      <div>7</div>
    </div>
    <ChatBox/>
</template>
    
<script>

import DefaultNavbar from '@/components/DefaultNavbar.vue';
import ChatBox from '@/components/ChatBox.vue';

export default 
{
  name: 'LobbyView',
  components: 
  {
    DefaultNavbar,
    ChatBox
  },
  
}


//
//  column-gap: 10px;
//row-gap: 10px;
</script>
   
<style scoped>

.lobby-page
{
  background: lightcoral;
  border: 3px solid black;
  display: grid;
  grid-template-columns:repeat(4, 1fr);
  grid-template-rows: repeat(35px, 1fr, 100px);
  min-height: 100vh;
  gap : 10px;
  padding: 4px;

}

.find_game{
  grid-column: 2 / 3;
  grid-row: 1 / 28;
}
.lobby-page div{
  background: lightblue;
  border:2px solid black;
  border-radius: 6px;
  border-radius: 16px;
}


</style>
    