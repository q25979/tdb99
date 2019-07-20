import Vue from 'vue';
import Router from 'vue-router';

import App from 'app/App';
import Register from 'app/components/Register';
import CountryList from 'app/components/CountryList';

const routes = [{
  path: '',
  component: App, // 顶层路由，对应index.html
  children: [ // 二级路由。对应App.vue
    {
      path: '/register/:id',
      name: 'Register',
      component: Register,
    },
    {
      path: '/country_list/:id',
      name: 'CountryList',
      component: CountryList
    }
  ]
}]
;

Vue.use(Router);

const router = new Router({
  mode: 'history',
  routes,
  scrollBehavior() {
    return {y: 0};
  }
});

export default router;
