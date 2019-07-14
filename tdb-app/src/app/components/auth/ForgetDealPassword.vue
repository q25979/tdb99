<template>
  <main-container title="" containerColor="transparent" :hasTabbar="false" class="auth-container">
    <mt-button slot="left" icon="back" @click.native="$router.go(-1)">
      {{$t('common.back')}}
    </mt-button>
    <div class="auth-forget-security">
      <header>
        {{$t('forget_security_psd.title')}}
      </header>
      <div class="auth-code">
        <p>
          {{$t('forget_security_psd.tips1')}} <span>+{{memberProfile.country_code || '86'}} {{mobile}}</span> {{$t('forget_security_psd.tips2')}}
        </p>
      </div>
      <sms-input v-model="pin_code" :mobile="mobile" :country="memberProfile.country_code" :label="$t('common.verify_code')" :placeholder="$t('tips.enter_verify_code')"></sms-input>
      <password-input v-model="password" :label="$t('common.new_psd')" :placeholder="$t('rule.security_psd')"></password-input>
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
import PasswordInput from 'app/components/elements/PasswordInput';
import SmsInput from 'app/components/elements/SmsInput';
export default {
  data() {
    const numReg = /^\d{6}$/;
    return {
      mobile: '',
      password: '',
      pin_code: '',
      repassword: '',
      state: store.state,
      numReg
    };
  },
  mounted(){
    this.mobile = this.state.memberProfile.mobile;
  },
  methods: {
    handleClick() {
      window.scroll(0, 0);
      if(!(this.numReg.test(this.password) && this.numReg.test(this.repassword))) {
        this.messagebox({
          message: this.$t('rule.security_psd'),
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
      this.mobile = this.state.memberProfile.mobile;
      this.$post('/member/user/reset_security_password', {
        mobile: this.mobile,
        password: this.password,
        pin_code: this.pin_code
      })
      .then(resp => {
        this.messagebox({
          message: this.$t('success.reset_security_psd'),
          confirmButtonText: this.$t('common.sure')
        }).then(r => {
          this.password = '';
          this.pin_code = '';
          this.repassword = '';
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
    canSubmit() {
      return  this.password && this.pin_code && this.repassword;
    },
    memberProfile() {
      return this.state.memberProfile;
    }
  },
  components: {
    MainContainer,
    PasswordInput,
    SmsInput
  }
};
</script>
<style lang="scss" rel="stylesheet/scss">
  .auth-forget-security {
    .auth-code {
      font-size: 26px;
      line-height: 37px;
      padding: 0 32px;
      margin: 8px 0 16px;
      &>p {
        color: #545454;
        span {
          color: #000;
        }
      }
    }
    .mint-cell {
      background: transparent !important;
      .mint-cell-wrapper {
        background: transparent !important;
      }
    }
    &>header {
      margin-top: 32px;
      font-family: PingFangSC-Regular;
      font-size: 64px;
      color: #000;
      padding-left: 32px;
      margin-bottom: 24px;
    }
    &>.mint-button {
      border-radius: 49px;
      margin: 0 32px;
      display: block;
      width: calc(100% - 64px);
      box-shadow: none;
      border: 0;
      font-family: PingFangSC-Regular;
      font-size: 36px;
      margin-top: 88px;
      opacity: 1 !important;
    }
  }
</style>
