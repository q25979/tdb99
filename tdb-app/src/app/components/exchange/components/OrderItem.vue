<template>
  <div class="sell-item" @click="$router.push(isSell() ? `/exchange/details/sell/${item.number}` : `/exchange/details/buy/${item.number}`)">
    <div class="title">
      <div class="title-left">
        <span :class="['sell-icon',{'is-sell': isSell()}]"></span> {{isSell() ? $t('order.sell_order') : $t('order.buy_order')}}
        <!-- <div v-if="item.side == 2 || item.status != 1 && item.status != 16">
          <img
            v-for="(item, index) in imgArr"
            :key="index"
            :src="item"
            alt="">
        </div> -->
      </div>
      <div class="title-right">
       {{getStatus(item.status)}} <img src="../../../assets/img/back_icon_12x.png" alt="">
      </div>
    </div>
    <div class="sell-content">
      <div class="count">
        {{$t('common.count')}}: <span>{{item.amount}}</span>
      </div>
      <div class="count">
        {{$t('common.current_price')}}: <span>${{item.current_price | currency}}</span>
      </div>
    </div>
    <div class="money">
      {{$t('common.amount')}}: <span>￥{{item.payment_amount}}</span>
    </div>
  </div>
</template>

<script>
import {Decimal} from 'decimal.js';
import store from 'app/store';
export default {
  props: ['item', 'imgArr'],
  data() {
    return {
      state: store.state,
      allImg: [],
      img: '',
    };
  },
  mounted() {
  },
  computed: {
    memberProfile() {
      return this.state.memberProfile;
    },
    rate() {
      return this.state.rate;
    }
  },
  methods: {
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
    isSell() {
      return this.item.side == 2;
    }
  }
}
</script>

<style lang="scss">
  .sell-item {
     padding: 38px 32px 32px;
     background-color: #fff;
    .title {
      display: flex;
      justify-content: space-between;
      margin-bottom: 40px;
      .title-left { 
        font-family: PingFangSC-Regular;
        font-size: 30px;
        color: #222;
        line-height: 1;
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
          background-color: #CD941B;
          margin-right: 24px; 
        }
        .sell-icon.is-sell {
          background-color: #CD941B;
        }
        img {
            width: 36px;
            height: 36px;
            margin-right: 24px;
            &:first-of-type {
              margin-left: 48px;
            }
            
          }
      }

      .title-right {
        display: flex;
        align-items: center;
        font-size: 30px;
        line-height: 1;
        color: #818181;
        img {
          width: 44px;
          height: 44px;
        }
      }
    }
    .sell-content {
      display: flex;
      justify-content: space-between;
      margin-bottom: 8px;
      .count {
        font-size: 24px;
        line-height: 1;
        color: #818181;
        margin-right: 16px;
        span {
          font-family: PingFangSC-Regular;
          font-size: 30px;
          color: #222;
          line-height: 1;
        }
        &:last-child {
          span {
            color: #CD941B;
          }
        }
      }
    }
    .money {
        font-size: 24px;
        line-height: 1;
        color: #818181;
        margin-right: 16px; 
        margin-top: 30px;  
        span {
          font-family: PingFangSC-Regular;
          font-size: 30px;
          color: #222;
          font-weight: bold;
          line-height: 1;
        }
    }
  }
</style>
