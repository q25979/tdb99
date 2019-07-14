<template>
  <mt-field
    class="common-input captcha-input"
    :value="value"
    :label="label"
    :placeholder="placeholder"
    @input.native="$emit('input', $event.target.value)">
    <div class="img" @click="refreshImage">
      <img :src="imgSrc" alt="">
    </div>
  </mt-field>
</template>
<script>
import store from 'app/store';
import {uuid} from 'vue-uuid';
export default {
  props: ['value', 'label', 'placeholder'],
  data() {
    return {
      state: store.state,
      imgSrc: ''
    };
  },
  computed: {
    uuid() {
      return this.state.uuid;
    }
  },
  mounted() {
    this.getImage();
  },
  methods: {
    getImage() {
      this.imgSrc = `${BASE_URL}/captcha_pin_code?uuid=${this.uuid}`;
    },
    refreshImage() {
      store.refreshUuid();
      this.getImage();
    }
  },
  watch: {
  }
};
</script>
<style lang="scss">
  .captcha-input {
    .mint-cell-wrapper {
      position: relative;
    }
    .mint-cell-value {
      width: 340px;
    }
    .mint-field-other {
      height: 86px;
      position: absolute;
      right: 32px;
      top: 92px;
      width: 332px;
      &:after {
        display: none;
      }
      img {
        height: 86px;
      }
    }
  }
</style>
