import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import Login from '../views/Login.vue'
import Signin from '../views/Signin.vue'
import PilotOverview from '../views/PilotOverview.vue'
import NewSession from '../views/NewSession.vue'
import ProtocolOverview from '../views/ProtocolOverview.vue'
import NewPilot from '../views/NewPilot.vue'
import EditPilot from '../views/EditPilot.vue'
import ReactivatePilot from '../views/ReactivatePilot.vue'

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
    path: '/signin',
    name: 'Signin',
    component: Signin
  },
  {
    path: '/pilots',
    name: 'PilotOverview',
    component: PilotOverview
  },
  {
    path: '/session/new',
    name: 'NewSession',
    component: NewSession
  },
  {
    path: '/protocol',
    name: 'ProtocolOverview',
    component: ProtocolOverview
  },
  {
    path: '/pilot/new',
    name: 'NewPilot',
    component: NewPilot
  },
  {
    path: '/pilot/edit',
    name: 'EditPilot',
    component: EditPilot
  },
  {
    path: '/pilot/reactivate',
    name: 'ReactivatePilot',
    component: ReactivatePilot
  },
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
