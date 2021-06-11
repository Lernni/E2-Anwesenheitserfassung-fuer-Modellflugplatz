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

export const $axios = axios

const token = localStorage.getItem('token')
console.log(token)
if (token) {
  $axios.defaults.headers.common['token'] = token
}

$axios.defaults.baseURL = process.env.VUE_APP_BACKEND_API

Vue.prototype.$axios = $axios

new Vue({
  router, store,
  render: h => h(App)
}).$mount('#app')