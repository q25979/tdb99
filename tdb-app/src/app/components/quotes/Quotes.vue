<template>
  <main-container :hasHeader="true" class="quotes" :title="$t('common.quote')" containerColor="#fff">
    <!-- <header slot="header" class="nav-header">
      <mt-navbar v-model="selected">
        <mt-tab-item id="quotes" @click.native="$router.push('/quotes/list')">
          {{$t('quotes.market')}}
        </mt-tab-item>
        <mt-tab-item id="news" @click.native="$router.push('/quotes/news')">
          {{$t('quotes.notice')}}
        </mt-tab-item>
      </mt-navbar>
    </header> -->
    <div class="quotes-container">
      <ul>
        <li class="header">
          <div>
            {{$t('common.asset')}}
          </div>
          <div>
           {{$t('common.lastest_price')}}
          </div>
          <div>
            {{$t('common.asset_change')}}
          </div>
        </li>
        <li
          class="crypto"
          v-for="(item, index) of dataList"
          :key="index">
          <div>
            <i :class="['icon', item.currency_code]"></i>
            <span>{{item.currency_code}}</span>
          </div>
          <div>
            ${{item.usd_price}}
          </div>
          <div :class="getNumber(item.percent_change) >=0 ? 'up' : 'down'">
            {{getNumber(item.percent_change) >= 0 ? `+${getNumber(item.percent_change, 2)}` : getNumber(item.percent_change, 2)}}%
          </div>
        </li>
      </ul>
    </div>
  </main-container>
</template>
<script>
import MainContainer from 'app/components/elements/MainContainer';
export default {
  data() {
    return {
      selected: 'quotes',
      dataList: [],
      canAjax: true,
      interval: ''
    };
  },
  computed: {
  },
  mounted() {
    this.getList();
    if(!this.interval) {
      this.interval = setInterval(() => {
        this.getList();
      }, 5000);
    }
  },
  methods: {
    getList() {
      if(this.canAjax) {
        this.canAjax = false;
      }
      this.$get('/member/currency/cryptocurrency').then(res => {
        this.dataList = res.data.objects;
        this.canAjax = true;
      }).catch(err => {
        this.canAjax = true;
      });
    },
    getNumber(val, v) {
      if(v) {
        return parseFloat(val).toFixed(2);
      } else {
        return parseFloat(val);
      }
    }
  },
  watch: {
  },
  components: {
    MainContainer,
  },
  beforeRouteLeave(to, from, next) {
    clearInterval(this.interval);
    next();
  }
};
</script>
<style lang="scss" rel="stylesheet/scss">
  .quotes {
    position: relative;
  }
  
  .quotes-container {
    ul {
      li {
        display: flex;
        align-items: center;
        padding: 40px 32px;
        width: 100%;
        position: relative;
        &.header {
          font-family: PingFangSC-Regular;
          font-size: 22px;
          color: #878787;
          padding: 26px 32px;
          background: #fff;
          border-bottom: 2px solid #E6E6E6;
          &:after {
            display: none;
          }
          &>div {
            font-size: 26px;
            color: #878787;
            letter-spacing: 0;
            text-align: left;
          }
        }
        &:after {
          position: absolute;
          content: '';
          width: calc(100% - 32px);
          height: 2px;
          background: #E6E6E6;
          bottom: 0;
          right: 0;
        }
        div {
          &:first-child {
            width: calc(32% - 15px);
            margin-right: 15px;
          }
          &:nth-child(2) {
            width: calc(48% - 15px);
            margin-right: 15px;
          }
          &:last-child {
            width: 20%;
          }
        }
        &.crypto {
          background: #fff;
          i {
            width: 64px;
            height: 64px;
            &.BTC {
              background-image: url('../../assets/img/crypto/BTC.png');
            }
            &.ETH {
              background-image: url('../../assets/img/crypto/ETH.png');
            }
            &.DASH {
              background-image: url('../../assets/img/crypto/DASH.png');
            }
            &.LTC {
              background-image: url('../../assets/img/crypto/LTC.png');
            }
            &.USDT {
              background-image: url('../../assets/img/crypto/USDT.png');
            }
            &.BSV {
              background-image: url('../../assets/img/crypto/BSV.png');
            }
            &.ETC {
              background-image: url('../../assets/img/crypto/ETC.png');
            }
            &.EOS {
              background-image: url('../../assets/img/crypto/EOS.png');
            }
            &.XRP {
              background-image: url('../../assets/img/crypto/XRP.png');
            }
            &.DOGE {
              background-image: url('../../assets/img/crypto/DOGE.png');
            }
          }
          div {
            &:first-child {
              display: flex;
              align-items: center;
              span {
                font-family: PingFangSC-Regular;
                font-size: 30px;
                color: #222;
                margin-left: 16px;
              }
            }
            &:nth-child(2) {
              font-size: 30px;
              color: #222;
              letter-spacing: 0;
              text-align: left;
              font-family:SFCompactDisplay-Regular;
            }
            &:last-child {
              height: 48px;
              line-height: 48px;
              text-align: center;
              border-radius: 8px;
              font-family: PingFangSC-Regular;
              font-size: 24px;
              font-weight:bold;
              color: #FFFFFF;
              &.up {
                background: #4AC76E;
              }
              &.down {
                background: #EA2524;
              }
            }
          }
        }
      }
    }
  }
</style>
