<template>
  <div class="result">
    <div class="inner">
      <div class="icon">
        <img src="../assets/imgs/success.png" alt="">
      </div>
      <div class="tips-register">
        {{$t('tips.register_success')}}
      </div>
      <div class="tips-download">
        {{$t('tips.download')}}
      </div>
    </div>
    <div class="download">
      <mt-button type="primary" @click.native="handleClick">{{$t('tips.download_btn')}}</mt-button>
    </div>
  </div>
</template>
<script>
  import i18n from 'app/i18n';
  const localeList = i18n.localeList;
  import {Button} from 'mint-ui';
  export default {
    data() {
      return {
        downloadLink: ''
      };
    },
    computed: {
      activeLocale: {
        get() {
          return localeList.find(l => l.value === i18n.locale);
        },
        set(val) {
        }
      }
    },
    mounted() {
      // let isPC = function() {
      //   let userAgentInfo = navigator.userAgent.toLowerCase();
      //   let Agents = ['android', 'iphone', 'symbianOS', 'windows phone', 'ipad', 'ipod'];
      //   let flag = true;
      //   for(let v = 0; v < Agents.length; v++) {
      //     if (userAgentInfo.indexOf(Agents[v]) > 0) {
      //       flag = false; break;
      //     }
      //   }
      //   return flag;
      // };
      // let isPCFlag = isPC();
      let browser = {
        versions: function() {
          let u = navigator.userAgent;
          return {
            trident: u.indexOf('Trident') > -1,
            presto: u.indexOf('Presto') > -1,
            webKit: u.indexOf('AppleWebKit') > -1,
            gecko: u.indexOf('Gecko') > -1 && u.indexOf('KHTML') == -1,
            mobile: !!u.match(/AppleWebKit.*Mobile.*/),
            ios: !!u.match(/\(i[^;]+;( U;)? CPU.+Mac OS X/),
            android: u.indexOf('Android') > -1 || u.indexOf('Linux') > -1,
            iPhone: u.indexOf('iPhone') > -1,
            iPad: u.indexOf('iPad') > -1,
            webApp: u.indexOf('Safari') == -1
          };
        }(),
        language: (navigator.browserLanguage || navigator.language).toLowerCase()
      };
      let linkLang = this.activeLocale.value;
      let urlLang = '';
      if(linkLang == 'zh_CN') {
        urlLang = 'cn';
      } else if(linkLang == 'zh_TW') {
        urlLang = 'hk';
      } else {
        urlLang = 'en';
      }
      if(browser.versions.ios) {
        this.downloadLink = `http://${DOWNLOAD_URL}/${urlLang}/download`;
      } else if(browser.versions.android) {
        this.downloadLink = `http://${DOWNLOAD_URL}/${urlLang}/download`;
      } else {
        this.downloadLink = `http://${DOWNLOAD_URL}/${urlLang}/download`;
      }
    },
    methods: {
      handleClick() {
        window.location.href = this.downloadLink;
      }
    },
    components: {
      MtButton: Button,
    },
  };
</script>
<style lang="scss">
  @import '../style/mixin';

  .result {
    .inner {
      background: #fff;
      text-align: center;
      .icon {
        padding-top: 40px;
        padding-bottom: 10px;
        text-align: center;
        img {
          width: px2rem(74px);
          height: px2rem(74px);
        }
      }
      .tips-register {
        font-size: px2rem(17px);
        padding: 8px 0;
      }
      .tips-download {
        padding-bottom: 30px;
        font-size: px2rem(14px);
        color: #545454;
      }
    }
    .download {
      margin-top: 32px;
      button {
        width: calc(100% - 30px);
        margin: 0 15px;
        height: 48px;
      }
    }
  }
</style>
