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
    path: '/session/new',
    name: 'NewSession',
    component: NewSession,
    meta: {
      requiresAuth: true,
      roles: ['admin']
    }
  },
  {
    path: '/session/edit',
    name: 'EditSession',
    component: EditSession,
    meta: {
      requiresAuth: true,
      roles: ['admin', 'pilot']
    }
  },
  {
    path: '/protocol',
    name: 'ProtocolOverview',
    component: ProtocolOverview,
    meta: {
      requiresAuth: true,
      roles: ['admin', 'pilot']
    }
  },
  {
    path: '/pilot/new',
    name: 'NewPilot',
    component: NewPilot,
    meta: {
      requiresAuth: true,
      roles: ['admin']
    }
  },
  {
    path: '/pilot/edit',
    name: 'EditPilot',
    component: EditPilot,
    meta: {
      requiresAuth: true,
      roles: ['admin']
    }
  },
  {
    path: '/pilot/reactivate',
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
 if(to.matched.some(record => record.meta.requiresAuth)) {
    if (store.getters.isLoggedIn) {
      console.log(store.getters.userInfo)
      next()
      return
    }
    next('/login')
  } else {
    next()
  }
})

export default router
