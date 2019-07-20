import Vue from 'vue';

const store = {
  bus: new Vue(),
  state: {
    countrySelect: {
      code: '86',
      abbr: 'CN'
    },
    mobile: ''
  },
};

export default store;
