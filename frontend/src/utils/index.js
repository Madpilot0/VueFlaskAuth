import Vue from 'vue'
import store from '@/store'

export const EventBus = new Vue()

function isValidJWT (jwt) {
  if (!jwt || jwt.split('.').length < 3) {
    return false
  }
  try {
    const data = JSON.parse(atob(jwt.split('.')[1]))
    const exp = new Date(data.exp * 1000)
    const now = new Date()
    return now < exp
  } catch (error) {
    return false
  }
}

export function isAuthenticated () {
  let jwt = localStorage.jwt || store.getters.jwt
  return isValidJWT(jwt)
}
