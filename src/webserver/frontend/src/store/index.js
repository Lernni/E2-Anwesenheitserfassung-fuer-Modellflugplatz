import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'
import { $axios } from '../main'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    status: '',
    token: localStorage.getItem('token') || '',
    user: localStorage.getItem('user') || '{}'
  },
  actions: {
    login({commit}, loginCredentials) {
      return new Promise((resolve, reject) => {
        commit('auth_request')
        axios.post("/login", loginCredentials)
        .then(response => {
          const token = response.data.token
          const user = response.data.user
          localStorage.setItem('token', token)
          localStorage.setItem('user', JSON.stringify(user))
          console.log(localStorage.getItem('user'))
          $axios.defaults.headers.common['token'] = token
          commit('auth_success', {token, user})
          resolve(response)
        }).catch(error => {
          commit('auth_error')
          localStorage.removeItem('token')
          reject(error)
        })
      })
    },
    logout({commit}) {
      return new Promise((resolve, reject) => {
        commit('logout')
        localStorage.removeItem('token')
        localStorage.removeItem('user')
        delete $axios.defaults.headers.common['token']
        resolve()
        reject()
      })
    }
  },
  mutations: {
    auth_request(state) {
      state.status = 'loading'
    },
    auth_success(state, payload) {
      state.status = 'success'
      state.token = payload.token
      state.user = JSON.stringify(payload.user)
    },
    auth_error(state) {
      state.status = 'error'
    },
    logout(state) {
      state.status = ''
      state.token = ''
      state.user = '{}'
    },
  },
  getters: {
    isLoggedIn: state => !!state.token,
    authStatus: state => state.status,
    userInfo: state => state.user
  }
})