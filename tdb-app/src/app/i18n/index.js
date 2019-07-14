import Vue from 'vue';
import VueI18n from 'vue-i18n';
import {localeList, defaultLocale} from './locales';
import VueCookie from 'vue-cookie';

const messages = localeList.reduce((result, locale) => {
  result[locale.value] = locale.messages;
  return result;
}, {});


class VueI18nEx extends VueI18n {
  _initVM(data) {
    const silent = Vue.config.silent;
    Vue.config.silent = true;
    this._vm = new Vue({data});
    Vue.config.silent = silent;
  }
  get localeList() {
    return localeList;
  }
}

Vue.use(VueI18nEx);
const i18n = new VueI18nEx({
  locale: localeList.find(l => l.value == VueCookie.get('hl'))?VueCookie.get('hl') : defaultLocale,
  fallbackLocale: defaultLocale,
  messages
});


export default i18n;
