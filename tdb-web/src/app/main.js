// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import 'babel-polyfill';
import Vue from 'vue';
import router from 'app/router';
import http from 'app/http';
import i18n from 'app/i18n';
import 'app/plugins';
import 'app/apollo';
import 'app/assets/css/font-awesome.min.css';
import 'mint-ui/lib/style.min.css';

Vue.config.productionTip = false;

new Vue({
  router,
  http,
  i18n
}).$mount('#app');


