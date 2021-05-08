import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import Login from '../views/Login.vue'
import PilotOverview from '../views/PilotOverview.vue'
import AddSession from '../views/AddSession.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/pilot-overview',
    name: 'PilotOverview',
    component: PilotOverview
  },
  {
    path: '/add-session',
    name: 'AddSession',
    component: AddSession
  },
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
