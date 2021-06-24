<!--
  *** Navbar.vue ***
  - Navigationsleiste der Webseite
  - Autor: Lenny Reitz
  - Mail: lenny.reitz@htw-dresden.de
-->

<template>
  <b-navbar toggleable="lg" type="dark" variant="primary">
    <b-navbar-brand href="/">Modellflugplatz</b-navbar-brand>
    <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
    <b-collapse id="nav-collapse" is-nav>
      <b-navbar-nav v-if="isLoggedIn">
        <b-nav-item to="/sessions">Flugprotokoll</b-nav-item>
        <b-nav-item v-if="user.is_admin" to="/pilots">Pilotenübersicht</b-nav-item>
        <b-nav-item v-if="user.is_admin" to="/settings">Einstellungen</b-nav-item>
      </b-navbar-nav>

      <b-navbar-nav class="ml-auto">
        <b-nav-item-dropdown :disabled="!isLoggedIn" id="user-info" right>
          <template #button-content>
            <b-avatar class="avatar" :variant="isLoggedIn ? 'primary' : 'secondary'"></b-avatar>
            <b-nav-text v-if="isLoggedIn" class="mx-2">{{ user.name }}</b-nav-text>
          </template>
          <b-dropdown-item disabled>Nutzername: {{ user.username }}</b-dropdown-item>
          <b-dropdown-item disabled>Rolle: {{ user.is_admin ? 'Admin' : 'Pilot' }}</b-dropdown-item>
          <b-dropdown-divider></b-dropdown-divider>
          <b-dropdown-item @click="logout">Abmelden</b-dropdown-item>
        </b-nav-item-dropdown>
      </b-navbar-nav>
    </b-collapse>
  </b-navbar>
</template>

<script>
import store from '../store'
import VueRouter from 'vue-router'
const { isNavigationFailure, NavigationFailureType } = VueRouter

export default {
  name: "NavBar",
  data() {
    return {
      isLoggedIn: false,
      user: {}
    }
  },
  watch:  {
    // Beim Ausführen von logout() durch den Store wird die Seite nicht neu geladen
    // Zusätzlich zu mounted() müssen also Änderungen in der URL betrachtet werden
    // Folgende Zeile ist notwendig, damit beim serve nicht der Fehler no-unused-vars geworfen wird
    // eslint-disable-next-line no-unused-vars
    $route(to, from) {
      this.isLoggedIn = store.getters.isLoggedIn
      var user = store.getters.userInfo
      this.user = (user == '{}') ? {} : JSON.parse(user)

    }
  },
  mounted() {
    this.isLoggedIn = store.getters.isLoggedIn
    var user = store.getters.userInfo
    this.user = (user == '{}') ? {} : JSON.parse(user)
  },
  methods: {
    // store.dispatch() -> Aufruf der Funktion im Store
    logout: function () {
      store.dispatch('logout')
      .then(() => {
        // Duplication Route Error verhindern:
        // Wenn sich der Nutzer bereits auf /login befindet, wird die Seite nur neugeladen
        // siehe https://router.vuejs.org/guide/advanced/navigation-failures.html#detecting-navigation-failures
        this.$router.push('/login').catch(failure => {
          if (isNavigationFailure(failure, NavigationFailureType.duplicated)) {
            this.$router.go()
          }
        })
      })
    }
  },
}
</script>

<style scoped>
.avatar {
  border: 2px white solid;
}

#user-info {
  margin: -8px !important;
}

#nav-collapse {
  text-align: center;
}
</style>