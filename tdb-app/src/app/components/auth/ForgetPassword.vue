<template>
  <main-container title="" containerColor="transparent" :hasTabbar="false">
    <mt-button slot="left" @click.native="$router.go(-1)">
      {{$t('common.cancel')}}
    </mt-button>
    <div class="auth-forget-password">
      <header>
       {{$t('forget_psd.title')}}
      </header>
      <mobile-input v-model="mobile" :label="$t('common.mobile')" :placeholder="$t('tips.enter_mobile')"></mobile-input>
      <sms-input v-model="pin_code" :mobile="mobile" :label="$t('common.sms_code')" :placeholder="$t('tips.enter_sms_code')"></sms-input>
      <password-input v-model="password" :label="$t('common.new_psd')" :placeholder="$t('tips.enter_new_psd')"></password-input>
      <password-input v-model="repassword" :label="$t('common.confirm_psd')" :placeholder="$t('tips.enter_new_psd_again')"></password-input>
      <mt-button :disabled="!canSubmit" type="primary" @click.native="handleClick">
        {{$t('common.sure')}}
      </mt-button>
    </div>
  </main-container>
</template>
<script>
import store from 'app/store';
import MainContainer from 'app/components/elements/MainContainer';
import MobileInput from 'app/components/elements/MobileInput';
import PasswordInput from 'app/components/elements/PasswordInput';
import SmsInput from 'app/components/elements/SmsInput';
export default {
  data() {
    const numReg = /^[a-zA-Z\w]{6,20}$/;
    return {
      mobile: '',
      password: '',
      pin_code: '',
      repassword: '',
      state: store.state,
      numReg
    };
  },
  methods: {
    handleClick() {
      window.scroll(0, 0);
      if(!(this.numReg.test(this.password) && this.numReg.test(this.repassword))) {
        this.messagebox({
          message: this.$t('rule.login_psd'),
          confirmButtonText: this.$t('common.sure')
        });
        return false;
      } else if(this.repassword !== this.password) {
        this.messagebox({
          message: this.$t('errors.password_twice_not_same'),
          confirmButtonText: this.$t('common.sure')
        });
        return false;
      }
      this.$post('/member/user/reset_password', {
        mobile: this.mobile,
        password: this.password,
        pin_code: this.pin_code,
        country_code: this.countryCode,
      })
      .then(resp => {
        localStorage.setItem('token', resp.data.token);
        store.refreshMemberProfile(() => {
          this.$router.push('/');
        });
      })
      .catch(err => {
        if(err.code == 1001) {
          this.messagebox({
            message: this.$t('errors.mobile_not_exist'),
            confirmButtonText: this.$t('common.sure')
          });
        }

        if(err.code == 1002) {
          if(err.message.pin_code) {
            this.messagebox({
              message: this.$t('errors.verify_code_error'),
              confirmButtonText: this.$t('common.sure')
            });
          } else {
            this.messagebox({
              message: this.$t('errors.psd_error'),
              confirmButtonText: this.$t('common.sure')
            });
          }
        }
        if(err.code == 1004 || err.code == 1005) {
          this.messagebox({
            message: this.$t('errors.verify_code_expired'),
            confirmButtonText: this.$t('common.sure')
          });
        }
      });
    }
  },
  computed: {
    countryCode() {
      return this.state.countryCode;
    },
    canSubmit() {
      return this.mobile && this.password && this.pin_code && this.repassword;
    }
  },
  components: {
    MainContainer,
    MobileInput,
    PasswordInput,
    SmsInput
  }
};
</script>
<style lang="scss" rel="stylesheet/scss">
  .auth-forget-password {
    .mint-cell {
      background: transparent !important;
      .mint-cell-wrapper {
        background: transparent !important;
      }
    }
    &>header {
      margin-top: 58px;
      font-family: PingFangSC-Regular;
      font-size: 64px;
      color: #222;
      padding-left: 32px;
      margin-bottom: 37px;
      line-height: 1;
    }
    &>.mint-button {
      margin: 0 32px;
      display: block;
      width: calc(100% - 64px);
      height: 104px;
      box-shadow: none;
      border: 0;
      font-family: PingFangSC-Regular;
      font-size: 36px;
      margin-top: 81px;
      opacity: 1 !important;
    }
  }
</style>
