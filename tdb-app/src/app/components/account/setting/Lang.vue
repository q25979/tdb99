<template>
  <main-container :title="$t('account.lang')" :hasTabbar="false">
    <mt-button icon="back" slot="left" @click.native="$router.go(-1)"></mt-button>
    <div class="account-setting-lang">
      <mt-cell
        v-for="(item, index) in dataList"
        :key="index"
        :title="item.label"
        is-link
        @click.native="handleClick(item.lang)">
        <i class="icon icon-check" v-if="activeLang == item.lang"></i>
      </mt-cell>
    </div>
  </main-container>
</template>
<script>
import MainContainer from 'app/components/elements/MainContainer';
import i18n from 'app/i18n';
const localeList = i18n.localeList;
export default {
  data() {
    return {
      activeLang: 'cn',
      dataList: [{
        lang: 'en',
        label: 'English'
      }, {
        lang: 'cn',
        label: '中文'
      }, {
        lang: 'ms',
        label: 'Melayu'
      }, {
        lang: 'th',
        label: 'ไทย'
      }, {
        lang: 'kh',
        label: 'ភាសាខ្មែរ'
      }, {
        lang: 'vi',
        label: 'Tiếng việt'
      }],
    };
  },
  mounted() {
    this.activeLang = localeList.find(l => l.value === i18n.locale).value;
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
    handleClick(lang) {
      this.activeLang = lang;
      this.setLocale(this.activeLang);
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

  },
  watch: {
  },
  components: {
    MainContainer
  }
};
</script>
<style lang="scss">
  .account-setting-lang {
    i {
      width: 44px;
      height: 44px;
      &.icon-check {
        background-image: url('../../../assets/img/icon/check.png');
      }
    }
    .mint-cell {
      &:first-child {
        margin-top: 40px;
      }
      .mint-cell-wrapper {
        .mint-cell-value {
          margin: 0;
        }
        .mint-cell-allow-right {
          display: none;
        }
      }
    }
  }
</style>

