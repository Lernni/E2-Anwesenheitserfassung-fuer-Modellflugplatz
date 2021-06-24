/*
  *** App.vue ***
  - Startskript der Vue App
  - Autor: Lenny Reitz
  - Mail: lenny.reitz@htw-dresden.de
*/

import Vue from 'vue'
import App from './App.vue'
import store from './store'
import router from './router'
import { BootstrapVue, BootstrapVueIcons } from 'bootstrap-vue'
import Vuelidate from 'vuelidate'
import axios from 'axios'

import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap-vue/dist/bootstrap-vue.css';

Vue.use(BootstrapVue)
Vue.use(BootstrapVueIcons)
Vue.use(Vuelidate)

/* 
 * $axios ist eine modifizierte Variante von axios, die in allen Vue Komponenten benutzt werden kann
 * Falls der Browser noch einen Token im Cache hinterlegt hat, wird dieser beim Aufruf bzw. Neuladen 
 * der Seite standardmäßig in den Request-Header geschrieben. Jedes Mal wenn $axios benutzt wird, um
 * einen Request abzuschicken, wird dann automatisch der entsprechende Token zur Authentifzierung 
 * mitgeschickt.
 */

export const $axios = axios

const token = localStorage.getItem('token')
if (token) {
  $axios.defaults.headers.common['token'] = token
}

/* 
 * Je nachdem, ob die Vue App im Developement Modus (npm run serve) gestartet oder in den 
 * Production Modus exportiert wird (npm run build), vergibt Vue anhand der Variable VUE_APP_BACKEN_API
 * die URL des Backends, die standardmaäßig bei Requests mit $axios verwendet werden soll. 
 * VUE_APP_BACKEN_API ist definiert in '.env' für den Development Modus und in '.env.production' für
 * den Production Modus.
 */

$axios.defaults.baseURL = process.env.VUE_APP_BACKEND_API

// Definiere $axios als globalen Prototyp
Vue.prototype.$axios = $axios

new Vue({
  // Einbinden von Vue Router und Vuex Store
  router, store,
  render: h => h(App)
}).$mount('#app')