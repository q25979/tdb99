import Vue from 'vue';
import Router from 'vue-router';
import App from 'app/App';

import store from 'app/store';
import VueCookie from 'vue-cookie';

import Home from 'app/components/Home';
import account from './account';
import exchange from './exchange';
import quotes from './quotes';
import finance from './finance';
import auth from './auth';
import {get} from 'app/axios';
import { MessageBox } from 'mint-ui';

const routes = [
  {
    path: '/',
    name: 'App',
    component: App, // 顶层路由，对应index.html
    children: [
      {
        path: '/home',
        name: 'Home',
        component: Home,
        meta: {
          tab: 'home'
        },
      },
    ].concat(account, exchange, quotes, finance, auth)
  },
];

Vue.use(Router);

const router = new Router({
  // mode: 'history',
  routes,
  scrollBehavior() {
    return {y: 0};
  }
});

const exceptPaths = ['/answer', '/login', '/forget_password', '/profile', '/home']

router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth)) {
    get('/member/user/current_user').then(res =>{
      if(exceptPaths.indexOf(to.fullPath) == -1) {
        next();
        if(res.data.state == 0) {
          next('/profile');
        } else if(res.data.state == 1) {
          let title = '';
          let content = '';
          let startTxt = '';
          switch(VueCookie.get('hl')) {
          case 'en':
            title = 'Questionnaire evaluation';
            content = 'LEBO will receive a free value of two hundred dollars through the evaluation.';
            startTxt = 'Start';
            break;
          case 'ms':
            title = 'Penilaian soal selidik';
            content = 'LEBO akan menerima nilai percuma dua ratus dolar melalui penilaian.';
            startTxt = 'Mulakan';
            break;
          case 'vi':
            title = 'Đánh giá câu hỏi';
            content = 'LEBO sẽ nhận được giá trị miễn phí hai trăm đô la thông qua đánh giá.';
            startTxt = 'Bắt đầu';
            break;
          case 'th':
            title = 'การประเมินผลแบบสอบถาม';
            content = 'LEBO จะได้รับมูลค่าฟรีสองร้อยดอลลาร์ผ่านการประเมินผล';
            startTxt = 'เริ่มต้น';
            break;
          case 'kh':
            title = 'ការវាយតម្លៃកម្រងសំណួរ';
            content = 'LEBO នឹងទទួលបានតម្លៃឥតគិតថ្លៃពីររយដុល្លារតាមរយៈការវាយតម្លៃ។';
            startTxt = 'ចាប់ផ្តើម';
            break;
          default:
            title = '问卷测评';
            content = '通过测评将会免费获得价值两百美金的LEBO。';
            startTxt = '开始';
            break;
          }
          MessageBox({
            title: title,
            message: content,
            showConfirmButton: true,
            confirmButtonText: startTxt,
            closeOnClickModal: false
          }).then(res => {
            if (res === 'confirm') {
              next('/answer');
            }
          });
        }
      } else {
        next();
      }
    }).catch(err => {
      next({
        path: '/home',
        query: {
          redirect: to.fullPath
        }
      });
    })
  } else {
    next();
  }
});

export default router;
