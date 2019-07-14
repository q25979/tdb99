<template>
  <div class="mobile-input">
    <mt-field
      class="common-input"
      :value="value"
      :label="label"
      :placeholder="placeholder"
      @input.native="$emit('input', $event.target.value)">
    </mt-field>
    <mt-button class="country-select" @click.native="showPicker">
      <span>+{{countryCode}}</span>
      <i class="mintui mintui-fa fa fa-caret-down"></i>
    </mt-button>
    <mt-popup
      v-model="isVisible"
      position="bottom">
      <mt-picker :slots="slots" :value-key="`label_${activeLang}`" :showToolbar="true" ref="picker">
        <div class="picker-btn">
          <span @click="handleConfirm">
            {{$t('common.sure')}}
          </span>
        </div>
      </mt-picker>
    </mt-popup>
  </div>
</template>
<script>
import store from 'app/store';
import i18n from 'app/i18n';
const localeList = i18n.localeList;
export default {
  props: ['value', 'label', 'placeholder'],
  data() {
    const countryCodeList= require('../../assets/country_codes.json');
    return {
      isVisible: false,
      state: store.state,
      countryCodeList,
      activeLang: 'cn'
    };
  },
  created() {
  },
  mounted() {
    this.countryAbbr = 'CN';
    this.countryCode = '86';
    let lang = localeList.find(l => l.value === i18n.locale).value;
    this.activeLang = (lang == 'cn' || lang == 'hk') ? 'cn' : 'en';
  },
  computed: {
    slots() {
      return this.countryCodeList && [{
        values: this.countryCodeList
      }];
    },
    countryCode: {
      get() {
        return this.state.countryCode;
      },
      set(val) {
        this.state.countryCode = val;
      }
    },
    countryAbbr: {
      get() {
        return this.state.countryAbbr;
      },
      set(val) {
        this.state.countryAbbr = val;
      }
    }
  },
  methods: {
    showPicker() {
      this.isVisible = true;
      let arr = this.countryCodeList.filter((v, i) => {
        return v.abbr == this.countryAbbr;
      });
      this.$refs.picker.setValues(arr);
    },
    handleConfirm() {
      let val = this.$refs.picker.getValues()[0];
      this.countryAbbr = val.abbr;
      this.countryCode = val.code;
      this.isVisible = false;
    }
  },
  watch: {
  }
};
</script>
<style lang="scss">
  .mobile-input {
    position: relative;
    .picker-btn {
      text-align: right;
      height: 80px;
      line-height: 80px;
      display: flex;
      justify-content: flex-end;
      align-items: center;
      span {
        font-size: 30px;
        padding: 0 5px;
      }
    }
    input {
      padding-left: 165px !important;
    }
    .country-select {
      position: absolute;
      bottom: 0;
      left: 32px;
      padding-left: 25px;
      padding-right: 26px;
      height: 86px;
      background: transparent;
      box-shadow: none;
      border: 0;
      width: 140px;
      &:active, &:after {
        background: transparent;
      }
      &:before {
        position: absolute;
        content: '';
        width: 2px;
        height: 40px;
        background: #444053;
        right: 0;
        top: 23px;
      }
      label {
        display: flex;
        align-items: center;
        justify-content: space-between;
      }
      span {
        font-family: PingFangSC-Regular;
        font-size: 30px;
        color: #000;
      }
      i {
        font-size: 24px !important;
        color: #000;
      }
    }
  }
</style>


