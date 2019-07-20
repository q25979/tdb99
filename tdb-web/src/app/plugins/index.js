import Vue from 'vue';
import VueCookie from 'vue-cookie';

const config = {
  locale: VueCookie.get('hl')
};

Vue.use(VueCookie);
Vue.use(config);


