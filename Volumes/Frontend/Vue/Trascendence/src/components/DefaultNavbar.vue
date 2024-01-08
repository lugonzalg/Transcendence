<template>
    <div class="navbar">
        <nav class="navbar navbar-expand-lg bg-body-tertiary" data-bs-theme="dark">
          <div class="container-fluid">
            <a class="navbar-brand" @click="home">Trascendence</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
              <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarSupportedContent">
              <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                <li class="nav-item">
                  <a class="nav-link active" aria-current="page" href="#">Docs</a>
                </li>
                <li class="nav-item">
                  <a class="nav-link" href="https://github.com/Julen-Smith/Trascendence">Github</a>
                </li>
                <li class="nav-item dropdown">
                  <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                    About
                  </a>
                  <ul class="dropdown-menu">
                    <li><a class="dropdown-item" href="#">Wiki</a></li>
                    <li><a class="dropdown-item" href="localhost/Login">42</a></li>
                    <li><hr class="dropdown-divider"></li>
                    <li><a class="dropdown-item" href="#">Something else here</a></li>
                  </ul>
                </li>
              </ul>
            </div>
          </div>
        </nav>
        </div>
</template>
  
<script>
export default {
  name: 'DefaultNavbar',
  methods: {
        home() {
            this.$router.push('/');
        }
    }
}
</script>
  

<style scoped>
.navbar {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    z-index: 2;
  }
  
  .navbar li{
    margin-left: 50px;
  }
</style>
  