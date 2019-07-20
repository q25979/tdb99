<template>
  <div class="country-select">
    <div class="mobile-input">
      <mt-field
          label=" "
          v-model="mobile"
          type="tel"
          :placeholder="$t('tips.enter_mobile')">
      </mt-field>
      <div class="country-code" @click="toggleList">
        <span>+{{currentData.code}}</span>
        <i class="arrow-icon"></i>
      </div>
    </div>
  </div>
</template>
<script>
  import {Cell, Field} from 'mint-ui';
  import store from 'app/store';
  import i18n from 'app/i18n';
  const localeList = i18n.localeList;
  export default {
    props: ['id'],
    data() {
      return {
        isShow: false,
        store: store,
        search: '',
        countries: [],
        tempCountries: []
      };
    },
    mounted() {
    },
    computed: {
      currentData: {
        get() {
          return store.state.countrySelect;
        },
        set(val) {
          this.store.state.countrySelect = val;
        }
      },
      activeLocale: {
        get() {
          return localeList.find(l => l.value === i18n.locale);
        },
        set(val) {
        }
      },
      currentLang: {
        get() {
          let lang = this.activeLocale.value;
          if(lang == 'zh_CN') {
            return 'cn';
          } else if(lang == 'zh_TW') {
            return 'hk';
          } else {
            return 'en';
          }
        }
      },
      mobile: {
        get() {
          return store.state.mobile;
        },
        set(val) {
          this.store.state.mobile = val;
        }
      },
    },
    methods: {
      toggleList() {
        this.$router.push(`/country_list/${this.id}`);
      },
    },
    components: {
      MtCell: Cell,
      MtField: Field,
    }
  };
</script>
<style lang="scss">
  .country-select {
    i.arrow-icon {
      display: inline-block;
      vertical-align: middle;
      width: 9px;
      height: 5px;
      background-image: url('../assets/imgs/arrow_down.png');
      background-size: 100% 100%;
    }
    &>.mobile-input {
      position: relative;
      .country-code {
        position: absolute;
        top: 0;
        left: 20px;
        width: 100px;
        height: 48px;
        line-height: 48px;
        font-size: 16px;
        span {
          color: #19BC9C;
        }
        i {
          margin-left: 5px;
          color: #888;
        }
      }
    }
    .mint-popup {
      height: 100%;
      overflow: scroll;
      .mint-header {
        height: 40px;
      }
      .mint-search {
        height: auto;
        .mint-searchbar {
          background: #eee;
        }
        .mint-searchbar-cancel {
          color: #19BC9C
        }
        .mint-search-list {
          display: none;
        }
      }
      .country-content {
        .mint-cell {
          .mint-cell-allow-right {
            display: none;
          }
          .mint-cell-wrapper {
            background-image: linear-gradient(0deg, #ededed, #ededed) !important;
          }
        }
      }
    }
  }
</style>
