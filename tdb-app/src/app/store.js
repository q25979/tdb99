import Vue from 'vue';
import router from 'app/router';
import {get} from 'app/axios';
import {uuid} from 'vue-uuid';
import {Decimal} from 'decimal.js';

const store = {
  bus: new Vue(),
  state: {
    memberProfile: {},
    unauth: false,
    uuid: uuid.v4(),
    countryCode: '86',
    countryAbbr: 'CN',
    selectAddress: '',
    activityType: '',
    rate: {
      CNY: '',
      USDT: ''
    }
  },
  getRate(cb) {
    get('/member/currency/currency').then(res => {
      store.state.rate.CNY = res.data.objects.filter((v) => {
        return v.country_code == 'CN';
      })[0]['usd_rate'];
      get('/member/currency/cryptocurrency').then(r => {
        let price = r.data.objects.filter((v) => {
          return v.currency_code == 'USDT';
        })[0]['usd_price'];
        store.state.rate.USDT = (new Decimal(1)).div(price).toString();
        if(cb == undefined) {
        } else {
          cb(store.state.rate);
        }
      });
    });
  },
  refreshUuid() {
    store.state.uuid = uuid.v4();
  },
  updateMemberProfile(data) {
    store.state.memberProfile = data;
    store.state.unauth = false;
  },
  refreshMemberProfile(cb = () => {}) {
    get('/member/user/current_user').then(res => {
      store.state.memberProfile = res.data;
      store.state.unauth = false;
      // if(res.data.state == 0) {
      //   router.push('/profile');
      // } else if(res.data.state == 1) {
      //   router.push('/answer');
      // } else {
      // }
      cb();
    })
    .catch(err => err);
  },
  logout() {
    store.state.memberProfile = null;
    localStorage.removeItem('token');
  },
  ifLogin(truePart, falsePart) {
    return this.state.memberProfile ? truePart : falsePart;
  },
  unauth() {
    store.state.memberProfile = null;
    if(router.app.$route.meta.tab != 'home' && router.app.$route.meta.requiresAuth) {
      store.state.unauth = true;
      router.push('/home');
    }
  },
  refreshSelectAddress() {
    if(router.app.$route.path !== '/account/address'){
      store.state.selectAddress = ''
    }
  }
};

export default store;
