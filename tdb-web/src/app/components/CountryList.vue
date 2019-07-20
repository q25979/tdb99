<template>
  <div class="country-list">
    <div class="country-header">
      <mt-header :title="$t('common.search')">
        <mt-button icon="back" slot="left" @click.native="handleBack"></mt-button>
      </mt-header>
      <mt-search v-model="search" :cancel-text="$t('common.cancel')" :placeholder="$t('common.search')">
      </mt-search>
    </div>
    <div class="country-content">
      <mt-cell :title="`${item[currentLang]} (+${item.code})`" is-link
      v-for="(item, index) in countries" :key="index"
      @click.native="handleClick(item)"></mt-cell>
    </div>
  </div>
</template>
<script>
  import data from 'app/data';
  const {countries} = data;
  import {Cell, Field, Button, Search, Header} from 'mint-ui';
  import store from 'app/store';
  import i18n from 'app/i18n';
  const localeList = i18n.localeList;
  export default {
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
      this.getCountries();
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
    },
    methods: {
      getCountries() {
        this.$apollo.query({
          query: countries,
        }).then(({data}) => {
          this.countries = data.countries;
          this.tempCountries = data.countries;
        });
      },
      handleBack() {
        this.$router.push(`/register/${this.$route.params.id}`);
      },
      handleClick(val) {
        this.currentData = {
          code: val.code,
          abbr: val.abbr
        };
        this.$router.push(`/register/${this.$route.params.id}`);
      }
    },
    watch: {
      search(val) {
        this.countries = [];
        setTimeout(() => {
          if(val) {
            this.countries = this.tempCountries.filter((item) => {
              if(`(+${item.code})`.indexOf(val) >= 0) {
                return true;
              }
              if(this.currentLang == 'en') {
                return item[this.currentLang].toLowerCase().indexOf(val.toLowerCase()) >= 0;
              } else {
                return item[this.currentLang].indexOf(val) >= 0;
              }
            });
          } else {
            this.countries = this.tempCountries;
          }
        }, 100);
      }
    },
    components: {
      MtCell: Cell,
      MtField: Field,
      MtButton: Button,
      MtSearch: Search,
      MtHeader: Header
    }
  };
</script>
<style lang="scss">
  .country-list {
    height: 100%;
    overflow: scroll;
    .mint-header {
      height: 40px;
    }
    .mint-search {
      height: auto;
      .mint-searchbar-inner {
        height: 34px;
      }
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
    .country-header {
      position: sticky;
      top: 0;
      left: 0;
      width: 100%;
      z-index: 10000;
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
</style>
