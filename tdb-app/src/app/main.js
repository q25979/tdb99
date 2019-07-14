// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue';
import router from 'app/router';
import i18n from 'app/i18n';
const localeList = i18n.localeList;
import 'app/mint-ui';
import 'app/utils/rem';
import 'app/filter';
import store from 'app/store';
import VueCookies from 'vue-cookie';
import {Toast, MessageBox, Indicator} from 'mint-ui';
import VueClipboard from 'vue-clipboard2';
import VueCordova from 'vue-cordova';
Vue.use(VueClipboard);
Vue.use(VueCordova);
Vue.use(VueCookies);
import VueHighcharts from 'vue-highcharts';
Vue.use(VueHighcharts);

import gallery from 'img-vuer';
Vue.use(gallery);

// Vue.component('font-awesome-icon', FontAwesomeIcon);


// document.addEventListener("deviceready", () => {
//   // if(localStorage.getItem('theme') == 'dark') {
//   //   StatusBar.backgroundColorByHexString("#000");
//   //   StatusBar.styleLightContent();
//   // } else {
//   StatusBar.backgroundColorByHexString("#fff");
//   StatusBar.styleDefault();
//   // }
// }, false);

Vue.config.productionTip = false;
store.refreshMemberProfile();

Vue.prototype.toast = Toast;
Vue.prototype.messagebox = MessageBox;
Vue.prototype.load = Indicator;

import {get, post, put , deletes, upload} from 'app/axios';
Vue.prototype.$get = get;
Vue.prototype.$post = post;
Vue.prototype.$put = put;
Vue.prototype.$delete = deletes;
Vue.prototype.$upload = upload;


let locale= VueCookies.get('hl') || i18n.locale;
if (typeof locale === 'string') {
  locale = locale.replace(/'/g, '');
  locale = localeList.find(l => l.value === locale);
}
if (locale) {
  i18n.locale = locale.value;
}
new Vue({
  router,
  i18n
}).$mount('#app');
