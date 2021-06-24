<!--
  *** App.vue ***
  - Startseite der Vue App
  - Autor: Lenny Reitz
  - Mail: lenny.reitz@htw-dresden.de
-->

<template>
  <div class="app">
    <NavBar/>
    <div class="container pt-4">
      <!-- router-view wird vom Vue Router als Einstiegspunkt für die Darstellung der Seiten verwendet -->
      <router-view/>
    </div>
  </div>
</template>

<script>
import NavBar from '@/components/NavBar.vue'

export default {
  name: "App",
  components: {
    NavBar
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

h2, h4, .last-ping-info {
  text-align: center;
}

.footer-buttons {
  display: flex;
  justify-content: center;
}

@media (min-width: 576px) {
  h2, h4 {
    text-align: start;
  }

  .last-ping-info {
    text-align: right;
  }

  .footer-buttons {
    display: block;
    justify-content: start;
  }
}
</style>