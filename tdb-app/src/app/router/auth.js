import Login from 'app/components/auth/Login';
import ForgetPassword from 'app/components/auth/ForgetPassword';
import ForgetDealPassword from 'app/components/auth/ForgetDealPassword';
import Answer from 'app/components/auth/Answer';
import Profile from 'app/components/auth/Profile';

export default [
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: {
      tab: 'home'
    },
  },
  {
    path: '/forget_password',
    name: 'ForgetPassword',
    component: ForgetPassword,
    meta: {
      tab: 'home'
    },
  },
  {
    path: '/forget_deal_password',
    name: 'ForgetDealPassword',
    component: ForgetDealPassword,
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: '/answer',
    name: 'Answer',
    component: Answer,
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: '/profile',
    name: 'AuthProfile',
    component: Profile,
    meta: {
      requiresAuth: true
    }
  }
];