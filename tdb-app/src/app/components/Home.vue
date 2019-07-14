<template>
  <div class="home">
    <mt-button class="lang-btn" @click.native="$router.push('/account/setting/lang')">
      {{$t('account.lang')}}
    </mt-button>
    <mt-button class="signin-btn" @click.native="$router.push('/login')" type="primary">
      {{$t('common.login')}}
    </mt-button>
    <div class="tips">
      {{$t('common.app_tips')}} <span>《{{$t('common.protol')}}》</span>
    </div>
  </div>
</template>
<script>
export default {
  data() {
    return {};
  }
};
</script>
<style lang="scss">
  .home {
    background-image: url('../assets/img/bg/bg_index.png');
    background-repeat: no-repeat;
    background-size: 100% 100%;
    height: 100%;
    position: relative;
    .mint-button {
      position: absolute;
      box-shadow: none;
      border: 0;
      &.lang-btn {
        top: 67px;
        right: 32px;
        padding: 0;
        height: auto;
        background: transparent;
        font-family: PingFangSC-Regular;
        font-size: 30px;
        color: #F2D479;
      }
      &.signin-btn {
        box-shadow: 0 2px 10px 3px rgba(43,57,166,0.30);
        font-family: PingFangSC-Medium;
        font-size: 36px;
        color: #FFFFFF;
        width: calc(100% - 96px);
        left: 48px;
        bottom: 232px;
        height: 96px;
      }
    }
    .tips {
      position: absolute;
      font-size: 26px;
      color: rgba(255,255,255,0.70);
      line-height: 36px;
      span {
        color: #F2D479;
      }
      bottom: 111px;
      left: 48px;
      width: calc(100% - 96px);
    }
  }
</style>