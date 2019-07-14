<template>
  <div class="detail-header">
    <div class="title">
      <div class="title-left">
        <span :class="['sell-icon',{'is-sell': isSell}]"></span>{{isSell ? $t('order.sell_order') : $t('order.buy_order')}}
        <div v-if="details.side == 2 || details.status != 1 && details.status != 16">
          <i
            v-for="(item, index) in imgArr"
            :key="index"
            :class="`icon ${item.key}`">
          </i>
        </div>
      </div>
      <div class="title-right">
       {{getStatus(details.status)}}
      </div>
    </div>
    <div class="sell-content">
      <div class="left">{{$t('order.payment_amount')}}: </div>
      <div class="money-amount right">￥{{details.payment_amount}}</div>
    </div>
    <div class="sell-content" v-if="details.payment_amount_usdt">
      <div class="left">{{$t('order.payment_amount')}}: </div>
      <div class="money-amount right">{{details.payment_amount_usdt}} USDT</div>
    </div>
    <div class="sell-content">
      <div class="left">{{$t('order.buy_count')}}: </div>
      <div class="right">{{details.amount}}</div>
    </div>
    <div class="sell-content">
      <div class="left">{{$t('order.buy_price')}}: </div>
      <div class="right">${{details.current_price | currency}}</div>
    </div>
  </div>
</template>

<script>
  import {Decimal} from 'decimal.js';
  import store from 'app/store';
  export default {
    props:['isSell', 'details', 'imgArr'],
    data() {
      return {
        state: store.state
      };
    },
    mounted() {
    },
    computed: {
      rate() {
        return this.state.rate;
      }
    },
    methods: {
      getTotal() {
        if(this.details.payment) {
          if(this.details.payment.type == 3) {
            return `${new Decimal(this.details.amount || 0).times(this.details.current_price || 0).times(this.rate.USDT).toFixed(8)} USDT`;
          } else {
            return `￥${new Decimal(this.details.amount || 0).times(this.details.current_price || 0).times(this.rate.CNY).toFixed(2)}`;
          }
        } else {
          return '￥0.00';
        }
      },
      getStatus(v) {
        switch(v) {
        case 1:
          return this.$t('order.status_1');
        case 2:
          return this.$t('order.status_2');
        case 4:
          return this.$t('order.status_4');
        case 8:
          return this.$t('order.status_8');
        case 16:
          return this.$t('order.status_16');
        }
      },
      getPayment(val) {
        let text = '';
        let key = '';
        if(val == 0) {
          text = this.$t('common.bank_card');
          key = 'bank';
        } else if(val == 1) {
          text = this.$t('common.wechat');
          key = 'wechat';
        } else if(val == 2) {
          text = this.$t('common.alipay');
          key = 'alipay';
        } else if(val == 3) {
          text = 'USDT';
          key = 'usdt';
        }
        return {
          label: text,
          value: val,
          key: key
        };
      },
    }
  }
</script>

<style lang="scss">
  .detail-header {
     padding: 38px 32px 16px;
     background-color: #fff;
    .title {
      display: flex;
      justify-content: space-between;
      margin-bottom: 40px;
      align-items: center;
      .title-left { 
        font-family: PingFangSC-Regular;
        font-size: 28px;
        color: #222;
        letter-spacing: 0;
        line-height: 48px;
        display: flex;
        align-items: center;
        &>div {
          display: flex;
          align-items: center;
        }
        .sell-icon {
          display: inline-block;
          width: 12px;
          height: 36px;
          background-color:  #CD941B;
          margin-top: 6px;
          margin-right: 20px;
        }
        .sell-icon.is-sell {
          background-color: #CD941B;
        }
        i {
          width: 36px;
          height: 36px;
          margin-right: 24px;
          &:first-of-type {
            margin-left: 48px;
          }
        }
      }

      .title-right {
        font-size: 24px;
        color: #EA2525;
        letter-spacing: 0;
        text-align: right;
        line-height: 42px;
      }
    }
    .sell-content {
      display: flex;
      justify-content: space-between;
      align-items: center;
      & > div {
        font-family: PingFangSC-Regular;
        font-size: 24px;
        color: #9b9b9b;
        line-height: 1;
        margin-bottom: 29px;
      }

      .left {
        text-align: left;
      }

      .right {
        text-align: right;
      }

      .right.money-amount {
        font-size: 24px;
        color: #222;
        line-height: 1;
      }

      

    }
    .money {
         font-size: 28px;
        line-height: 40px;
        color: rgba($color: #000000, $alpha: 0.53);
        margin-right: 16px;   
        span {
          font-family: PingFangSC-Regular;
          font-size: 34px;
          color: #545454;
          letter-spacing: 0;
          line-height: 48px;
        }
    }
  }
</style>
