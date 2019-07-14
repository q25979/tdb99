<template>
  <main-container title="" containerColor="transparent" :hasTabbar="false">
    <mt-button slot="left" @click.native="$router.go(-1)">
      {{$t('common.cancel')}}
    </mt-button>
    <div class="auth-login">
      <header>
        {{$t('login.title')}}
      </header>
      <mobile-input v-model="mobile" :label="$t('common.mobile')" :placeholder="$t('tips.enter_mobile')"></mobile-input>
      <password-input v-model="password" :label="$t('common.psd')" :placeholder="$t('tips.enter_psd')" :showForgetPsd="true"></password-input>
      <captcha-input v-model="captcha_pin_code" :label="$t('common.verify_code')" :placeholder="$t('tips.enter_verify_code')"></captcha-input>
      <mt-button :disabled="!canSubmit" type="primary" @click="handleLogin">
       {{$t('common.login')}}
      </mt-button>
    </div>
  </main-container>
</template>
<script>
import MainContainer from 'app/components/elements/MainContainer';
import MobileInput from 'app/components/elements/MobileInput';
import PasswordInput from 'app/components/elements/PasswordInput';
import CaptchaInput from 'app/components/elements/CaptchaInput';
import store from 'app/store';
export default {
  data() {
    return {
      mobile: '',
      password: '',
      platform: 'web',
      state: store.state,
      captcha_pin_code: '',
    };
  },
  computed: {
    canSubmit() {
      return this.mobile && this.password;
    },
    uuid() {
      return this.state.uuid;
    },
    countryCode() {
      return this.state.countryCode;
    }
  },
  mounted() {
  },
  methods: {
    onDeviceReady() {
      this.platform = device.platform;
    },
    handleLogin() {
      window.scroll(0, 0);
      this.$post('/member/user/password_login', {
        mobile: this.mobile,
        password: this.password,
        captcha_pin_code: this.captcha_pin_code,
        platform: this.platform,
        uuid: this.uuid,
      })
      .then(resp => {
        localStorage.setItem('token', resp.data.token);
        this.$get('/member/user/current_user').then(res => {
          store.updateMemberProfile(res.data);
          this.$get('/member/news', {
            params: {
              per_page: 1,
              page: 1
            }
          }).then(r => {
            if(r.data.objects.length) {
              this.messagebox({
                message: r.data.objects[0].details,
                confirmButtonText: this.$t('common.sure'),
                closeOnClickModal: false
              }).then(a => {
                if(res.data.state == 0) {
                  this.$router.push('/profile');
                } else if(res.data.state == 1) {
                  this.$router.push('/answer');
                } else {
                  this.$router.push('/');
                }
              });
            } else {
                if(res.data.state == 0) {
                  this.$router.push('/profile');
                } else if(res.data.state == 1) {
                  this.$router.push('/answer');
                } else {
                  this.$router.push('/');
                }
            }
          }).catch(err => {
          });
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
            this.$refs.captchaInput.refreshImage();
          } else {
            this.messagebox({
              message: this.$t('errors.psd_error'),
              confirmButtonText: this.$t('common.sure')
            });
          }
        }
        if(err.code == 1004 || err.code == 1005 || err.code == 1006) {
          this.messagebox({
            message: this.$t('errors.verify_code_expired'),
            confirmButtonText: this.$t('common.sure')
          });
          this.$refs.captchaInput.refreshImage();
        }
      });
    },
  },
  components: {
    MainContainer,
    MobileInput,
    PasswordInput,
    CaptchaInput
  }
};
</script>
<style lang="scss" rel="stylesheet/scss">
  .auth-login {
    .mint-cell {
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
      box-shadow: none;
      border: 0;
      font-family: PingFangSC-Regular;
      font-size: 36px;
      margin-top: 81px;
      opacity: 1 !important;
      height: 104px;
    }
  }
</style>
