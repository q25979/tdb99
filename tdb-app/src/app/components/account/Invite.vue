<template>
  <main-container :title="$t('account.invite_title')" :hasTabbar="false" containerColor="#fff">
    <mt-button slot="left" icon="back" @click.native="$router.push('/account')"></mt-button>
    <div class="account-invite">
      <header>
        <span>{{memberProfile.nickname}}</span> {{$t('common.invite_code')}}
      </header>
      <div class="tips-1">
        {{$t('account.invite_tips1')}}
      </div>
      <div class="code">
        {{memberProfile.uid}}
      </div>
      <mt-button
        type="primary"
        v-clipboard:copy="memberProfile.uid"
        v-clipboard:success="copySuccess"
        v-clipboard:error="copyError">
        {{copyTxt}}
      </mt-button>
      <VueQrcode :value="`http://web.tdb99.com/register/${memberProfile.uid}`" tag="img" :options="{size: 310}"></VueQrcode>
      <div class="tips-2">
        {{$t('account.invite_tips2')}}
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
      copyTxt: this.$t('common.copy')
    };
  },
  computed: {
    memberProfile() {
      return this.state.memberProfile;
    }
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
  .account-invite {
    padding-bottom: 65px;
    text-align: center;
    font-family: PingFangSC-Regular;
    padding: 0 32px;
    &>header {
      font-size: 30px;
      color: #696969;
      margin-top: 57px;
      >span{
        color: #F2D479;
      }
    }
    &>.tips-1 {
      font-size: 24px;
      color: #9B9B9B;
      margin-top: 18px;
    }
    &>.code {
      font-family: PingFangSC-Medium;
      font-size: 40px;
      color: #222;
      margin-top: 43px;
    }
    &>.mint-button {
      display: block;
      border-radius: 48px;
      margin: 38px auto 0 auto;
      padding: 0 124px;
      height: 104px;
      line-height: 96px;
      font-family: PingFangSC-Medium;
      font-size: 36px;
      color: #FFFFFF;
    }
    &>img {
      display: block;
      width: 344px;
      height: 344px;
      border-radius: 16px;
      margin: 233px auto 0 auto;
    }
    &>.tips-2 {
      font-size: 24px;
      color: #9B9B9B;
      margin-top: 42px;
    }
  }
</style>

