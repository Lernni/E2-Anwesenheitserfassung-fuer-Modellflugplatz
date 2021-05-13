<template>
  <div class="app">
    <div id="nav">
      <router-link to="/">Home</router-link> |
      <router-link to="/login">Login</router-link> | 
      <router-link to="/pilot-overview">Pilotenübersicht</router-link> | 
      <router-link to="/add-session">Flugsession nachtragen</router-link> | 
      <router-link to="/protocol-overview">Protokolldaten</router-link>
    </div>
    <div class="container">
      <router-view/>
    </div>
  </div>
</template>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}

#nav {
  padding: 30px;
}

#nav a {
  font-weight: bold;
  color: #2c3e50;
}

#nav a.router-link-exact-active {
  color: #42b983;
}
</style>
