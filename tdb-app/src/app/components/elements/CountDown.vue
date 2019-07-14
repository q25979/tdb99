<template>
  <div class="count-down">
    <mt-button plain @click.prevent="sendSms()" size="small" v-show="showGetSms" class="send-btn">
      {{$t('count_down.send')}}
    </mt-button>
    <mt-button plain v-show="!showGetSms" size="small" disabled class="resend-btn">
      ({{time}}){{$t('count_down.resend')}}
    </mt-button>
  </div>
</template>
<script>
  import store from 'app/store';
  export default{
    props: ['mobile', 'country'],
    data() {
      return {
        time: 60,
        interval: '',
        showGetSms: true,
        stop: false,
        state: store.state
      };
    },
    computed: {
      countryCode() {
        return this.country || this.state.countryCode;
      }
    },
    methods: {
      update() {
        if (this.time == 0) {
          this.showGetSms = true;
          this.stop = false;
          this.time = 60;
          clearInterval(this.interval);
        } else {
          this.time -= 1;
        }
      },
      start() {
        if (this.stop) {
          this.interval = setInterval(this.update, 1000);
        }
      },
      sendSms() {
        const mobile = this.$props.mobile;
        if (!mobile) {
          this.messagebox({
            message: this.$t('tips.enter_mobile'),
            confirmButtonText: this.$t('common.sure'),
          }).then(action => {
            return false;
          });
          return;
        }
        this.$post('/sms_pin_code', {
          country_code: this.countryCode,
          mobile: this.mobile
        }).then(res => {}).catch(err => {
            this.messagebox({
              message: this.$t('errors.mobile_code_not_match'),
              confirmButtonText: this.$t('common.sure'),
            }).then(action => {
              return false;
            });
          });
        this.stop = true;
        this.showGetSms = false;
        this.start();
      }
    }
  };
</script>
<style lang="scss">
  .count-down {
    height: 100%;
    position: relative;
    &:after {
      content: '';
      position: absolute;
      height: calc(100% - 40px);
      left: 0;
      top: 20px;
      width: 2px;
      background: #000;
    }
    .mint-button {
      height: 100%;
      border: 0 !important;
      font-size: 24px;
      &.send-btn {
        color: #EA2525;
      }
    }
  }
</style>
