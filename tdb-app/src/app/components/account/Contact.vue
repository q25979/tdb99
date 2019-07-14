<template>
  <main-container :title="$t('account.contact_title')" :hasTabbar="false" containerColor="#fff">
    <mt-button slot="left" icon="back" @click.native="$router.push('/account')"></mt-button>
    <div class="account-service">
      <img src="../../assets/img/service.png">
      <div class="tips-1">{{$t('account.contact_tips')}}</div>
      <mt-button
        type="primary"
        v-clipboard:copy="contact"
        v-clipboard:success="copySuccess"
        v-clipboard:error="copyError">
        {{copyTxt}}
      </mt-button>
      <div class="tips-2">
        {{$t('common.wechat_account')}}：{{contact}}
      </div>
    </div>
  </main-container>
</template>
<script>
import store from 'app/store';
import MainContainer from 'app/components/elements/MainContainer';
import VueQrcode from '@xkeshi/vue-qrcode';
export default {
  data() {
    return {
      state: store.state,
      copyTxt: this.$t('account.contact_copy_txt'),
      contact: ''
    };
  },
  computed: {
    memberProfile() {
      return this.state.memberProfile;
    }
  },
  mounted() {
    this.$get('/member/setting').then(res => {
      this.contact = res.data.value.contact_us;
    });
  },
  methods: {
    copySuccess() {
      this.copyTxt = this.$t('copy.success');
    },
    copyError() {
      this.copyTxt = this.$t('copy.failed');
    }
  },
  components: {
    MainContainer,
    VueQrcode
  }
};
</script>
<style lang="scss">
  .account-service {
    padding-bottom: 65px;
    text-align: center;
    font-family: PingFangSC-Regular;
    padding: 0 32px;
    &>header {
      font-size: 34px;
      color: #545454;
      margin-top: 64px;
      >span{
        color: #485EF0;
      }
    }
    &>.tips-1 {
      font-size: 30px;
      color: #000;
      margin-top: 19px;
    }
    &>.code {
      font-family: PingFangSC-Medium;
      font-size: 64px;
      color: #000;
      margin-top: 40px;
    }
    &>.mint-button {
      display: block;
      border-radius: 48px;
      margin: 266px auto 0 auto;
      padding: 0 102px;
      height: 96px;
      line-height: 96px;
      font-family: PingFangSC-Medium;
      font-size: 36px;
      color: #FFFFFF;
    }
    &>img {
      display: block;
      width: 366px;
      height: 366px;
      border-radius: 16px;
      margin: 112px auto 0 auto;
    }
    &>.tips-2 {
      font-size: 24px;
      color:rgba(105,105,105,1);
      margin-top: 36px;
      font-weight: 500;
    }
  }
</style>

