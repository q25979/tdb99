<template>
  <div class="lang-select">
    <mt-button slot="right" @click.native="showPopup">
      {{activeLocale.name}}
    </mt-button>
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
  import i18n from 'app/i18n';
  const localeList = i18n.localeList;
  export default {
    data() {
      return {
        picker: '',
        tempLang: '',
        isVisible: false,
        slots: [{
          flex: 1,
          values: ['中文', 'English', '한국어'],
          className: 'slot1',
          textAlign: 'center',
        }],
      };
    },
    mounted() {
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
        case 'zh':
          temp = '中文';
          break;
        case 'ko':
          temp = '한국어';
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
        console.log(this.tempLang);
        this.setLocale(this.tempLang);
        this.tempLang = '';
        this.isVisible = false;
      },
    }
  };

</script>
<style lang="scss">
  .mint-popup {
    width: 100%;
    .btn {
      text-align: right;
      button {
        border: none;
        color: #333 !important;
        padding: 10px 15px;
      }
    }
  }
</style>
