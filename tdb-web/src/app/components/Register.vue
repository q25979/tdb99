<template>
  <div class="register">
    <lang-select></lang-select>
    <div class="mobile-form">
      <div class="logo">
        <div class="img">
          <img src="../assets/imgs/logo.png" alt="">
        </div>
        <div class="text">
          TDB
        </div>
      </div>
      <country-select :id="sponsor">
      </country-select>
      <mt-field
        :label="$t('common.code')"
        :placeholder="$t('tips.enter_code')"
        v-model="pinCode">
        <mt-button class="send-btn" :plain="true" @click.native="handleSend" v-if="!isSend">
          {{sendText}}
        </mt-button>
        <mt-button class="send-btn" :plain="true" v-else>
          {{$t('common.resend')}}({{time}}s)
        </mt-button>
      </mt-field>
      <mt-field
        :label="$t('common.login_psd')"
        :placeholder="$t('tips.enter_password')"
        type="password"
        v-model="loginPsd"></mt-field>
      <mt-field
        :label="$t('common.repsd')"
        :placeholder="$t('tips.enter_repsd')"
        type="password"
        v-model="reloginPsd"></mt-field>
      <mt-field
        :label="$t('common.security_psd')"
        :placeholder="$t('tips.enter_security_password')"
        type="password"
        v-model="securityPsd"></mt-field>
      <mt-field
        :label="$t('common.resecurity')"
        :placeholder="$t('tips.enter_resecurity')"
        type="password"
        v-model="resecurityPsd"></mt-field>
      <mt-field
        :label="$t('common.sponsor')"
        v-model="sponsor"
        disabled></mt-field>
    </div>
    <div class="submit-button">
      <div>
        <mt-button type="primary" @click.native="handleSubmit" :disabled="!isFill">{{$t('common.sign_up')}}</mt-button>
      </div>
      <div>
        <a href="http://download.tdb99.com">{{$t('tips.download')}}</a>
      </div>
    </div>
  </div>
</template>
<script>
  import CountrySelect from 'app/components/CountrySelect';
  import LangSelect from 'app/components/LangSelect';
  import {Cell, Button, Field, Indicator, Search, MessageBox} from 'mint-ui';

  import store from 'app/store';
  import data from 'app/data';
  import i18n from 'app/i18n';
  const localeList = i18n.localeList;
  const {sendSmsCode, mobileRegister} = data;

  const mobileReg = /^\d+$/;
  const codeReg = /^[a-zA-Z0-9]*$/;
  const securityReg = /^\d{6}$/;

  export default {
    data() {
      return {
        pinCode: '',
        loginPsd: '',
        reloginPsd: '',
        isSend: false,
        time: 60,
        sponsor: '',
        securityPsd: '',
        resecurityPsd: '',
        store
      };
    },
    mounted() {
      this.sponsor = this.$route.params.id;
    },
    computed: {
      isFill() {
        return this.pinCode && this.mobile && this.loginPsd && this.securityPsd && this.reloginPsd && this.resecurityPsd;
      },
      isScroll() {
        return this.countryArr.length > 3;
      },
      sendText() {
        return this.$t('common.send_code');
      },
      countryCode: {
        get() {
          return this.store.state.countrySelect.code;
        }
      },
      countryAbbr: {
        get() {
          return this.store.state.countrySelect.abbr;
        }
      },
      activeLocale: {
        get() {
          return localeList.find(l => l.value === i18n.locale);
        },
        set(val) {
        }
      },
      mobile: {
        get() {
          return this.store.state.mobile;
        }
      }
    },
    methods: {
      handleSubmit() {
        if(!mobileReg.test(this.mobile)) {
          MessageBox({
            message: this.$t('errors.valid_mobile'),
            confirmButtonText: this.$t('common.ok')
          });
          return false;
        }
        if(!codeReg.test(this.pinCode)) {
          MessageBox({
            message: this.$t('errors.pin_code.format_error'),
            confirmButtonText: this.$t('common.ok')
          });
          return false;
        }
        if(this.loginPsd.length < 6 || this.loginPsd.length > 20) {
          MessageBox({
            message: this.$t('errors.valid_login_psd'),
            confirmButtonText: this.$t('common.ok')
          });
          return false;
        }

        if(this.reloginPsd !== this.loginPsd) {
          MessageBox({
            message: this.$t('errors.psd_not_same'),
            confirmButtonText: this.$t('common.ok')
          });
          return false;
        }

        if(!securityReg.test(this.securityPsd)) {
          MessageBox({
            message: this.$t('tips.enter_security_password'),
            confirmButtonText: this.$t('common.ok')
          });
          return false;
        }

        if(this.resecurityPsd !== this.securityPsd) {
          MessageBox({
            message: this.$t('errors.security_not_same'),
            confirmButtonText: this.$t('common.ok')
          });
          return false;
        }
        Indicator.open({
          text: this.$t('tips.registering'),
          spinnerType: 'fading-circle'
        });
        this.$apollo.mutate({
          mutation: mobileRegister,
          variables: {
            mobileRegister: {
              mobile: this.mobile,
              pin_code: this.pinCode,
              password: this.loginPsd,
              security_password: this.securityPsd,
              sponsor_uid: this.$route.params.id,
              country_code: this.countryCode,
              country_abbr: this.countryAbbr
            }
          }
        }).then(({data}) => {
          Indicator.close();
          if(data.mobileRegister.code == 200) {
            // let linkLang = this.activeLocale.value;
            // let urlLang = '';
            // if(linkLang == 'zh_CN') {
            //   urlLang = 'cn';
            // } else if(linkLang == 'zh_TW') {
            //   urlLang = 'hk';
            // } else {
            //   urlLang = 'en';
            // }
            MessageBox({
              message: this.$t('success.register_success'),
              confirmButtonText: this.$t('common.ok')
            }).then(() => {
              let nextPage = document.createElement('a');
              nextPage.setAttribute('href', 'http://download.tdb99.com');
              nextPage.click();
            });
          } else {
            this.caseCode(data.mobileRegister.code);
          }
        });
      },
      handleSend() {
        if(!this.mobile) {
          MessageBox({
            message: this.$t('tips.enter_mobile'),
            confirmButtonText: this.$t('common.ok')
          });
          return false;
        } else if(!mobileReg.test(this.mobile)) {
          MessageBox({
            message: this.$t('errors.valid_mobile'),
            confirmButtonText: this.$t('common.ok')
          });
          return false;
        }
        MessageBox({
          message: `${this.$t('tips.send_msg')}: +${this.countryCode} ${this.mobile}`,
          cancelButtonText: this.$t('common.cancel'),
          confirmButtonText: this.$t('common.ok'),
          showCancelButton: true
        }).then(action => {
          if(!this.isSend && action == 'confirm') {
            Indicator.open({
              text: this.$t('common.sending'),
              spinnerType: 'fading-circle'
            });
            this.$apollo.mutate({
              mutation: sendSmsCode,
              variables: {
                country_code: `+${this.countryCode}`,
                mobile: this.mobile,
              }
            }).then(({data}) => {
              Indicator.close();
              if(data.sendSmsCode.code == 200) {
                MessageBox({
                  message: this.$t('tips.send_success'),
                  confirmButtonText: this.$t('common.ok')
                });
                this.isSend = true;
                let interval = setInterval(() => {
                  this.time--;
                  if(this.time <= 0) {
                    clearInterval(interval);
                    this.isSend = false;
                    this.time = 60;
                  }
                }, 1000);
              } else {
                MessageBox({
                  message: this.$t('errors.system_error'),
                  confirmButtonText: this.$t('common.ok')
                });
              }
            });
          }
        });
      },
      caseCode(code) {
        let message = '';
        switch (code) {
        case 1002:
          message = this.$t('errors.register.sms_code_wrong');
          break;
        case 1005:
          message = this.$t('errors.register.sms_code_invalid');
          break;
        case 1011:
          message = this.$t('errors.mobile.has_registered', {mobile: this.mobile});
          break;
        case 1004:
          message = this.$t('errors.register.too_many_times');
          break;
        case 1001:
          message = this.$t('errors.register.link_invalid');
          break;
        default:
          message = this.$t('errors.system_error');
          break;
        }
        MessageBox({
          message: message,
          confirmButtonText: this.$t('common.ok')
        });
      },
    },
    watch: {
    },
    components: {
      MtCell: Cell,
      MtButton: Button,
      MtField: Field,
      MtSearch: Search,
      LangSelect,
      CountrySelect
    }
  };
</script>
<style lang="scss">
  @import "../style/mixin";
  .register {

    position: relative;
    min-height: 100%;
    background: #fff;

    input:disabled,
    input[disabled]{
      color: #000 !important;
      -webkit-text-fill-color: rgba(0, 0, 0, 1);
      -webkit-opacity: 1;
    }

    .mobile-form {
      margin-top: 6px;
      position: relative;

      .logo {
        margin-bottom: 10px;
        .img {
          text-align: center;
          img {
            width: px2rem(56px);
            height: px2rem(56px);
          }
        }
        .text {
          text-align: center;
          margin-top: 10px;
          font-size: 18px;
          color: #000;
          font-weight: 500;
        }
      }

      .country-select {
        .mint-cell {
          .mint-cell-wrapper {
            background-image: none;
          }
        }
      }

      .mobile-region {
        i.mint-cell-allow-right {
          display: none;
        }
        .mint-cell-value {
          margin-right: 0;
          span {
            display: inline-block;
            margin-right: 10px;
          }
        }
      }
      .send-btn {
        border-color: transparent;
        border-radius: 0;
        font-size: 16px;
        border-left-color: #ededed;
        height: 24px;
        color: #19BC9C;
        margin-top: 1px;
      }

      .country-list {
        position: absolute;
        width: 100%;
        z-index: 1;
        .mint-cell-wrapper {
          padding: 0 20px;
        }
        .mint-cell-value {
          margin-right: 0;
        }
        i.mint-cell-allow-right {
          display: none;
        }
        .mint-search {
          height: 198px;
          .mint-search-list {
            padding-top: 0;
            margin-top: 44px;
            height: 154px;
            .mint-search-list-warp {
              max-height: 154px;
              border: 10px solid #d9d9d9;
              border-top: 0;
            }
            .no-tips {
              text-align: center;
              height: 144px;
              line-height: 144px;
              background-color: #fff;
              font-size: px2rem(16px);
            }
          }
        }
        &.isScroll {
          .mint-search {
            .mint-search-list {
              .mint-search-list-warp {
                overflow-y: scroll;
              }
            }
          }
        }
      }
    }
    .submit-button {
      text-align: center;
      margin-top: 20px;
      padding-bottom: 20px;
      .mint-button {
        width: calc(100% - 30px);
        height: 35px;
      }
      &>div:last-child {
        margin-top: 15px;
      }
      a {
        display: inline-block;
        width: calc(100% - 30px);
        height: 35px;
        line-height: 35px;
        background-color: #19BC9C;
        border-radius: 4px;
        color: #fff;
        font-size: 18px;
      }
    }
    .tips {
      padding: 0 10px 10px 10px;
      margin-top: 20px;
      font-size: px2rem(13px);
    }
    .fade-enter-active, .fade-leave-active {
      transition: opacity .5s
    }
    .fade-enter, .fade-leave-to {
      opacity: 0
    }

    .mint-searchbar-inner {
      height: 30px;
      input {
        height: 30px;
      }
      .mintui-search {
        font-size: px2rem(16px);
      }
    }
  }
</style>
