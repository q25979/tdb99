<template>
  <div>
    <mt-header title=" ">
      <mt-button slot="right" @click.native="showPopup" class="lang-title">
        {{activeLocale.name}}
      </mt-button>
    </mt-header>
    <mt-popup v-model="isVisible" position="bottom" ref="popup">
      <div class="btn">
        <mt-button :plain="true" @click.native="selectLang">
          {{$t('common.sure')}}
        </mt-button>
      </div>
      <mt-picker :slots="slots" @change="onValuesChange"></mt-picker>
    </mt-popup>
  </div>
</template>
<script>
  import {Header, Button, Picker, Popup} from 'mint-ui';
  import i18n from 'app/i18n';
  const localeList = i18n.localeList;
  export default {
    props: ['showBack'],
    data() {
      return {
        picker: '',
        tempLang: '',
        isVisible: false,
        slots: [{
          flex: 1,
          values: ['繁体中文', 'English', '简体中文', '日語', '한국어'],
          className: 'slot1',
          textAlign: 'center',
        }],
      };
    },
    mounted() {
      let currentlang = this.$cookie.get('hl') || i18n.locale;
      this.setLocale(currentlang);
    },
    computed: {
      activeLocale: {
        get() {
          return localeList.find(l => l.value === i18n.locale);
        },
        set(val) {
          this.setLocale(val);
        }
      }
    },
    methods: {
      showPopup() {
        let temp = '';
        switch(this.activeLocale.value) {
        case 'en':
          temp = 'English';
          break;
        case 'zh_TW':
          temp = '繁体中文';
          break;
        case 'zh_CN':
          temp = '简体中文';
          break;
        case 'ko':
          temp = '한국어';
          break;
        case 'ja':
          temp = '日語';
          break;
        }
        this.isVisible = true;
        this.picker.setSlotValue(0, temp);
      },
      setLocale(locale) {
        if (typeof locale === 'string') {
          locale = localeList.find(l => l.value === locale);
        }
        if (locale) {
          i18n.locale = locale.value;
          this.$cookie.set('hl', i18n.locale, 365);
        }
      },
      onValuesChange(picker, value) {
        let locale = localeList.find(l => l.name === value[0]);
        this.tempLang = locale;
        this.picker = picker;
      },
      selectLang() {
        this.setLocale(this.tempLang);
        this.tempLang = '';
        this.isVisible = false;
      }
    },
    components: {
      MtHeader: Header,
      MtButton: Button,
      MtPicker: Picker,
      MtPopup: Popup
    }
  };

</script>
<style lang="scss">
  .lang-title {
    color: #212121 !important;
    margin-top: 12px;
  }
  .mint-popup {
    width: 100%;
    .btn {
      text-align: right;
      button {
        border: none;
        color: #19BC9C;
      }
    }
  }
</style>
