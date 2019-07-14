<template>
  <div class="password-box">
    <mt-field
    class="common-input password-input"
    :value="value"
    :label="label"
    @input.native="$emit('input', $event.target.value)"
    :placeholder="placeholder"
    :type="type">
    <i class="icon icon-invisible" v-if="!isVisible" @click="isVisible = !isVisible"></i>
    <i class="icon icon-visible" v-if="isVisible" @click="isVisible = !isVisible"></i>
  </mt-field>
  <p class="forget-password" v-if="showForget" @click="$router.push('/forget_deal_password')">{{$t('common.forget_security_password')}}</p>
  <p class="forget-password" v-if="showForgetPsd" @click="$router.push('/forget_password')">{{$t('common.forget_psd')}}</p>
  </div>
</template>
<script>
export default {
  props: ['value', 'label', 'placeholder', 'showForget', 'showForgetPsd'],
  data() {
    return {
      isVisible: false,
      type: 'password'
    };
  },
  watch: {
    isVisible(val) {
      this.type = val ? 'text' : 'password';
    }
  }
};
</script>
<style lang="scss">
  .password-box {
      position: relative;
    .forget-password {
      font-size: 24px;
      line-height: 37px;
      color: #EA2525;
      position: absolute;
      top: 36px;
      right: 32px;
    }
    .password-input {
    .mint-field-other {
      height: 48px;
    }
    i {
      &.icon {
        width: 48px;
        height: 48px;
        margin-right: 15px;
      }
      &.icon-invisible {
        background-image: url('../../assets/img/icon/invisible.png');
      }
      &.icon-visible {
        background-image: url('../../assets/img/icon/visible.png');
      }
    }
  }
  }
</style>


