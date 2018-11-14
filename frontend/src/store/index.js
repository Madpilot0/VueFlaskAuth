import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'
import router from '@/router'

Vue.use(Vuex)

let baseUrl = 'http://172.16.0.66/internal_routes/v1'

const state = {
  jwt: null,
  firstlastname: '',
  baseUrl: baseUrl
}
const actions = {
  LOGIN: function ({commit}, dataobj) {
    axios.post(baseUrl + '/login', dataobj)
      .then((response) => {
        commit('SET_USER_INFO', {data: response.data})
        router.app.$toast.success({
          title: 'Success',
          message: 'Logged in. Welcome ' + state.firstlastname
        })
        router.push('/')
      })
      .catch((response) => {
        router.app.$toast.error({
          title: 'Error',
          message: 'Couldn\'t login. Incorrect credentials'
        })
        console.log(response) // Catch error, show toastr
      })
  },
  LOGOUT: function ({commit}) {
    commit('LOGOUT_SESSION')
    router.push('/login')
  },
  UPDATE_USER_INFO: function ({commit}, dataobj) {
    commit('SET_USER_INFO', {data: dataobj})
  }
}
const mutations = {
  SET_USER_INFO: (state, {data}) => {
    // decompose token, store it all
    try {
      const userInfo = JSON.parse(atob(data.token.split('.')[1]))

      const exp = new Date(userInfo.exp * 1000)
      const now = new Date()

      if (now > exp) {
        throw new Error('Invalid date')
      }

      localStorage.jwt = data.token

      state.jwt = data.token
      state.firstlastname = userInfo.fln
    } catch (error) {
      router.app.$toast.error({
        title: 'Error',
        message: 'Session expired'
      })
      localStorage.jwt = null
      state.jwt = null
      state.firstlastname = ''
    }
  },
  LOGOUT_SESSION: (state) => {
    localStorage.jwt = null
    state.jwt = null
    state.firstlastname = ''
    router.push('/login')
  }
}
const getters = {
  jwt: state => state.jwt || (localStorage.jwt),
  firstlastname: state => state.firstlastname || 'Unknown',
  baseUrl: state => state.baseUrl
}

const store = new Vuex.Store({
  state,
  actions,
  mutations,
  getters
})

export default store
