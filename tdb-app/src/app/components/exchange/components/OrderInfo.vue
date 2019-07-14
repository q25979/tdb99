<template>
  <div class="order-info">
    <div class="order-title">{{$t('exchange.details_info')}}</div>
    <div class="item-info">
      <p class="left">{{$t('common.order_number')}}：</p>
      <p class="right">
        <span>
          {{details.number}}
        </span>
        <mt-button
          class="copy-btn"
          v-clipboard:copy="details.number"
          v-clipboard:success="copySuccess"
          v-clipboard:error="copyError">
          {{$t('common.copy')}}
        </mt-button>
      </p>
    </div>
    <div class="item-info">
      <p class="left">{{$t('common.created_at')}}：</p>
      <p class="right">
        <span class="text">
          {{details.created_timestamp | time}}
        </span>
      </p>
    </div>
    <div class="item-info" v-if="details.status == 2 || details.status == 4 || details.status == 8">
      <p class="left">{{$t('common.match_at')}}：</p>
      <p class="right">
        <span class="text">
          {{details.match_order.created_timestamp | time}}
        </span>
      </p>
    </div>
    <div class="item-info" v-if="details.status == 4 || details.status == 8">
      <p class="left">{{$t('common.pay_at')}}：</p>
      <p class="right">
        <span>
          {{details.updated_timestamp | time}}
        </span>
      </p>
    </div>
    <div class="item-info" v-if="!!getBuyMobile()">
      <p class="left">{{$t('exchange.details_buy_mobile')}}：</p>
      <p class="right">
        <span class="text">
          {{getBuyMobile()}}
        </span>
        <mt-button
          class="copy-btn"
          v-clipboard:copy="getBuyMobile()"
          v-clipboard:success="copySuccess"
          v-clipboard:error="copyError">
          {{$t('common.copy')}}
        </mt-button>
      </p>
    </div>
    <div class="item-info" v-if="!!getSellMobile()">
      <p class="left">{{$t('exchange.details_sell_mobile')}}：</p>
      <p class="right">
        <span class="text">
          {{getSellMobile()}}
        </span>
        <mt-button
          class="copy-btn"
          v-clipboard:copy="getSellMobile()"
          v-clipboard:success="copySuccess"
          v-clipboard:error="copyError">
           {{$t('common.copy')}}
        </mt-button>
      </p>
    </div>
  </div>
</template>
<script>
export default {
  props: ['details'],
  data() {
    return {};
  },
  methods: {
    copySuccess() {
      let index = this.toast({
        iconClass: 'icon icon-success-check',
        message: this.$t('copy.success')
      });
      setTimeout(v => {
        index.close();
      }, 15000);
    },
    copyError() {
      let index = this.toast({
        iconClass: 'icon icon-error-x',
        message: this.$t('copy.failed')
      });
      setTimeout(v => {
        index.close();
      }, 2000);
    },
    handleMobile(str) {
      if(str) {
        let arr = str.split(' ');
        if(arr.length == 2) {
          return `+${arr[0]}${arr[1]}`;
        } else {
          return '';
        }
      } else {
        return '';
      }
    },
    getSellMobile() {
      if(this.details) {
        if(this.details.side == 1) {
          if(!this.details.match_order.created_timestamp) {
            return '';
          } else {
            if(this.details.match_order.sell_user) {
              return this.handleMobile(this.details.match_order.sell_user.order_mobile);
            }
            return '';
          }
        } else {
          return this.details.user && this.handleMobile(this.details.user.order_mobile);
        }
      }
    },
    getBuyMobile() {
      if(this.details) {
        if(this.details.side == 2) {
          if(!this.details.match_order.created_timestamp) {
            return '';
          } else {
            if(this.details.match_order.buy_user) {
              return this.handleMobile(this.details.match_order.buy_user.order_mobile);
            }
            return '';
          }
        } else {
          return this.details.user && this.handleMobile(this.details.user.order_mobile);
        }
      }
    },
  },
  computed: {
  }
};
</script>
<style lang="scss">
  .order-info {
    padding: 32px 32px 15px;
    background-color: #fff;

    .order-title {
      font-family: PingFangSC-Regular;
      font-size: 28px;
      color: #222;
      line-height: 1;
      margin-bottom: 33px;
    }

    .item-info {
      display: flex;
      margin-bottom: 29px;
      align-items: center;
      p {
        font-family: PingFangSC-Regular;
        font-size: 24px;
        line-height: 1;
      }

      p.left {
        color: #9b9b9b;
        text-align: left;
        width: 40%;
      }

      p.right {
        width: 60%;
        color: #9b9b9b;
        text-align: right;
        display: flex;
        justify-content: flex-end;
        align-items: center;
        &>span {
          width: 100%;
        }
        .copy-btn {
          width: 120px;
          font-size: 24px;
          padding: 0;
          height: 40px;
          line-height: 40px;
          background-color: #fff;
          border-radius: 20px;
          margin-left: 15px;
        }
      }
    }
  }
</style>

