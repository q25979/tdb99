const en = require('app/i18n/locale/en.json');
const cn = require('app/i18n/locale/cn.json');
const kh = require('app/i18n/locale/kh.json');
const th = require('app/i18n/locale/th.json');
const ms = require('app/i18n/locale/ms.json');
const vi = require('app/i18n/locale/vi.json');


export const localeList = [ {
  name: '中文',
  value: 'cn',
  messages: {
    ...cn
  }
}, {
  name: 'English',
  value: 'en',
  messages: {
    ...en
  }
}, {
  name: 'Tiếng việt',
  value: 'vi',
  messages: {
    ...vi
  }
}, {
  name: 'Melayu',
  value: 'ms',
  messages: {
    ...ms
  }
}, {
  name: 'ไทย',
  value: 'th',
  messages: {
    ...th
  }
}, {
  name: 'ភាសាខ្មែរ',
  value: 'kh',
  messages: {
    ...kh
  }
}];

export const defaultLocale = localeList[0].value;
