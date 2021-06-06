import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import Login from '../views/Login.vue'
import Signup from '../views/Signup.vue'
import PilotOverview from '../views/PilotOverview.vue'
import NewSession from '../views/NewSession.vue'
import EditSession from '../views/EditSession.vue'
import ProtocolOverview from '../views/ProtocolOverview.vue'
import NewPilot from '../views/NewPilot.vue'
import EditPilot from '../views/EditPilot.vue'
import ReactivatePilot from '../views/ReactivatePilot.vue'
import store from '../store'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    meta: {
      requiresAuth: true,
      roles: ['admin', 'pilot']
    }
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: {
      requiresAuth: false
    }
  },
  {
    path: '/signup',
    name: 'Signup',
    component: Signup,
    meta: {
      requiresAuth: false
    }
  },
  {
    path: '/pilots',
    name: 'PilotOverview',
    component: PilotOverview,
    meta: {
      requiresAuth: true,
      roles: ['admin']
    }
  },
  {
    path: '/sessions/new',
    name: 'NewSession',
    component: NewSession,
    meta: {
      requiresAuth: true,
      roles: ['admin']
    }
  },
  {
    path: '/sessions/edit',
    name: 'EditSession',
    component: EditSession,
    meta: {
      requiresAuth: true,
      roles: ['admin', 'pilot']
    }
  },
  {
    path: '/sessions',
    name: 'ProtocolOverview',
    component: ProtocolOverview,
    meta: {
      requiresAuth: true,
      roles: ['admin', 'pilot']
    }
  },
  {
    path: '/pilots/new',
    name: 'NewPilot',
    component: NewPilot,
    meta: {
      requiresAuth: true,
      roles: ['admin']
    }
  },
  {
    path: '/pilots/edit',
    name: 'EditPilot',
    component: EditPilot,
    meta: {
      requiresAuth: true,
      roles: ['admin']
    }
  },
  {
    path: '/pilots/reactivate',
    name: 'ReactivatePilot',
    component: ReactivatePilot,
    meta: {
      requiresAuth: true,
      roles: ['admin']
    }
  },
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

router.beforeEach((to, from, next) => {
  if (!to.meta.requiresAuth) return next()

  if (store.getters.isLoggedIn) {
    var userInfo = JSON.parse(store.getters.userInfo)
    if (userInfo.is_admin) return next()
    if (to.meta.roles.includes('pilot')) return next()
  }

  return next("/login")
})

export default router
