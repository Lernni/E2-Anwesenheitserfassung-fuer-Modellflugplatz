<template>
  <div class="app">
    <div id="nav">
      <router-link to="/">Home</router-link> |
      <router-link to="/login">Login</router-link> | 
      <router-link to="/signup">Registrieren</router-link> | 
      <router-link to="/pilots">Pilotenübersicht</router-link> | 
      <router-link to="/session/new">Flugsession nachtragen</router-link> | 
      <router-link to="/session/edit">Flugsession bearbeiten</router-link> | 
      <router-link to="/protocol">Protokolldaten</router-link> | 
      <router-link to="/pilot/new">Pilot erstellen</router-link> | 
      <router-link to="/pilot/edit">Pilot bearbeiten</router-link> | 
      <router-link to="/pilot/reactivate">Pilot reaktivieren</router-link> | 
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

h2, .last-ping-info {
  text-align: center;
}

.submit-button-group {
  display: flex;
  justify-content: center;
}

@media (min-width: 576px) {
  h2 {
    text-align: start;
  }

  .last-ping-info {
    text-align: right;
  }

  .submit-button-group {
    display: block;
  }
}
</style>
