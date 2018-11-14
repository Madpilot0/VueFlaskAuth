import Vue from 'vue'
import App from './App'
import router from './router'
import store from './store'
import CxltToastr from 'cxlt-vue2-toastr'
import 'cxlt-vue2-toastr/dist/css/cxlt-vue2-toastr.css'
import BootstrapVue from 'bootstrap-vue'
import Vuex from 'vuex'

Vue.config.productionTip = false

var toastConfig = {
  position: 'top center',
  timeOut: 2000
}

Vue.use(CxltToastr, toastConfig)
Vue.use(BootstrapVue)
Vue.use(Vuex)

Vue.directive('focus', {
  inserted: function (el) {
    el.focus()
  }
})

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  render: h => h(App)
})
