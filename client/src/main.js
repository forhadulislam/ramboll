// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'

Vue.config.productionTip = false
Vue.http.headers.common['Access-Control-Allow-Origin'] = 'http://127.0.0.1:5000'
Vue.http.headers.common['Access-Control-Request-Method'] = '*'

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  template: '<App/>',
  components: { App }
})
