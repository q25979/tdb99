<template>
  <mt-field
    class="common-input sms-input"
    :value="value"
    :label="label"
    :placeholder="placeholder"
    type="number"
    @input.native="$emit('input', $event.target.value)">
    <count-down :mobile="mobile" :country="country"></count-down>
  </mt-field>
</template>
<script>
import CountDown from './CountDown';
export default {
  props: ['value', 'label', 'mobile', 'placeholder', 'country'],
  data() {
    return {};
  },
  watch: {
  },
  components: {
    CountDown
  }
};
</script>
<style lang="scss">
  .sms-input {
    .mint-field-other {
      height: 86px;
      margin-left: 15px;
      &:after {
        position: absolute;
        width: 2px;
        height: 48px;
        content: '';
        background: #878787;
        left: 0;
        top: 19px;
      }
    }
    img {
      height: 86px;
    }
  }
</style>
