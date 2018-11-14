import Vue from 'vue'
import Router from 'vue-router'
import store from '@/store'

import { isAuthenticated } from '@/utils'

const DefaultContainer = () => import('@/components/DefaultContainer')
const Dashboard = () => import('@/components/Pages/Dashboard')
const Login = () => import('@/components/Pages/Login')
const Page404 = () => import('@/components/Pages/Page404.vue')

Vue.use(Router)

let router = new Router({
  mode: 'history',
  linkActiveClass: 'open active',
  scrollBehavior: () => ({ y: 0 }),
  routes: [
    {
      path: '/',
      redirect: '/dashboard',
      name: 'Home',
      component: DefaultContainer,
      children: [
        {
          path: 'dashboard',
          name: 'Dashboard',
          component: Dashboard
        },
        {
          path: 'pages',
          name: 'Pages',
          redirect: '/pages/404',
          component: {
            render (c) { return c('router-view') }
          },
          children: [
            {
              path: '404',
              name: 'Page 404',
              component: Page404
            }
          ]
        }
      ]
    },
    {
      path: '/login',
      name: 'Login',
      component: Login
    },
    {
      path: '*',
      redirect: '/pages'
    }
  ]
})

router.beforeEach(function (to, from, next) {
  if (to.path !== '/login') {
    store.dispatch('UPDATE_USER_INFO', {token: store.getters.jwt || localStorage.jwt})
  }
  if (!isAuthenticated() && to.path !== '/login') {
    router.app.$toast.error({
      title: 'Error',
      message: 'No access - Please log in'
    })
    next('/login')
  } else if (isAuthenticated() && to.path === '/login') {
    next('/')
  } else {
    next()
  }
})

export default router
