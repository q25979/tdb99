const en = require('app/i18n/locale/en.json');
const zhCN = require('app/i18n/locale/zh_CN.json');
const zhTW = require('app/i18n/locale/zh_TW.json');
const ja = require('app/i18n/locale/ja.json');
const ko = require('app/i18n/locale/ko.json');


export const localeList = [{
  name: '简体中文',
  value: 'zh_CN',
  messages: {
    ...zhCN
  }
}, {
  name: 'English',
  value: 'en',
  messages: {
    ...en
  }
}, {
  name: '繁体中文',
  value: 'zh_TW',
  messages: {
    ...zhTW
  }
}, {
  name: '한국어',
  value: 'ko',
  messages: {
    ...ko
  }
}, {
  name: '日語',
  value: 'ja',
  messages: {
    ...ja
  }
}];

export const defaultLocale = localeList[0].value;

