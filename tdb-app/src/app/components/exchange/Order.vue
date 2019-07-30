<template>
  <main-container :hasHeader='false' class="exchange-order" containerColor='#fff' :noHeader='true' :hasTabbar='false'>
    <div class='order-operation'>
      <header>
        <mt-navbar class="buy-nav">
          <mt-tab-item
            v-for="(item,index) in navItem"
            :key="index"
            :id="item.value"
            :class="{'is-selected': activeType == item.value}"
            @click.native="changeNav(item)">
            {{item.label}}
          </mt-tab-item>
        </mt-navbar>
        <mt-button icon="back" @click.native="$router.go(-1)"></mt-button>
      </header>
      <div class="buy-content" v-if="'buy' === activeType">
        <mt-field class="common-input" :label="$t('common.price')" v-model="price" disabled></mt-field>
        <mt-field class="common-input" :label="$t('common.count')" v-model="sell_amount" disabled></mt-field>
      </div>
      <div class="sell-content" v-if="'sell' === activeType">
        <mt-field class="common-input" :label="$t('common.price')" v-model="price" disabled></mt-field>
        <mt-field class="common-input" :label="$t('common.count')" v-model="sell_amount" disabled></mt-field>
        <password-input :label="$t('common.security_psd')" :placeholder="$t('tips.enter_security_psd')" v-model="securityPsd" :showForget='true'></password-input>
      </div>
      <mt-button class="sure" type="primary" :disabled="!canSubmit" @click="handleClick">
        {{$t('common.sure')}}
      </mt-button>
    </div>
  </main-container>
</template>

<script>
import MainContainer from 'app/components/elements/MainContainer';
import PasswordInput from 'app/components/elements/PasswordInput';
export default {
  data() {
    return {
      activeType: 'buy',
      title: this.$t('order.buy_order'),
      navItem: [{
        label: this.$t('order.buy_order'),
        value: 'buy'
      }, {
        label: this.$t('order.sell_order'),
        value: 'sell'
      }],
      price: '',
      sell_amount: '',
      securityPsd: '',
      count: ''
    }
  },
  mounted() {
    this.$get('/member/setting').then(res => {
      let data = res.data.value;
      this.sell_amount = data['sell_amount'];
    });
    this.$get('/member/currency/usd_price').then(res => {
      this.price = `$ ${res.data.usd_price}`;
    });
  },
  computed: {
    canSubmit() {
      return (this.activeType == 'buy') || (this.activeType == 'sell' && this.securityPsd);
    }
  },
  methods:{
    getPayment(val) {
      let text = '';
      if(val == 0) {
        text = this.$t('common.bank_card');
      } else if(val == 1) {
        text = this.$t('common.wechat');
      } else if(val == 2) {
        text = this.$t('common.alipay');
      } else if(val == 3) {
        text = 'USDT';
      }
      return {
        label: text,
        value: val
      };
    },
    initForm() {
      this.securityPsd = '';
    },
    changeNav(val) {
      this.activeType = val.value;
      this.title = val.label;
      this.initForm();
    },
    handlePending(id) {
      this.messagebox({
        message: this.$t('tips.queue'),
        confirmButtonText: this.$t('common.query'),
        closeOnClickModal: false
      }).then(res => {
        this.load.open();
        setTimeout(() => {
          this.$get(`/member/order/pending/${id}?side=${this.activeType == 'buy' ? '1' : '2'}`).then(resp => {
            if(resp.data.status == 0) {
              this.handlePending(id);
            } else if(resp.data.status == 1) {
              this.messagebox({
                message: this.$t('success.operation'),
                confirmButtonText: this.$t('common.sure')
              }).then(res => {
                this.$router.push('/exchange');
              });
            } else {
              let text = '';
              if(resp.data.details.code == 1003) {
                text = this.$t('errors.in_side_full');
              } else if(resp.data.details.code == 1008) {
                text = this.$t('errors.community_wallet_not_enough');
              } else if(resp.data.details.code == 1001) {
                text = this.$t('errors.never_buy_order');
              } else if(resp.data.details.code == 1006 && this.activeType == 'buy'){
                text = this.$t('errors.today_buy_fill');
              } else if(resp.data.details.code == 1007) {
                text = this.$t('errors.tomorrow_try');
              } else {
                text = this.$t('errors.today_sell_fill');
              }
              this.messagebox({
                message: text,
                confirmButtonText: this.$t('common.sure')
              });
            }
          });
        }, 2000);
      });
    },
    handleSubmit() {
      window.scroll(0, 0);
      let params = {};
      if(this.activeType == 'buy') {
      } else {
        params.security_password = this.securityPsd;
      }
      this.load.open();
      setTimeout(() => {
        this.$post(`/member/order/${this.activeType}`, params).then(r => {
          // if(this.activeType == 'buy') {
          //   this.messagebox({
          //     message: this.$t('success.operation'),
          //     confirmButtonText: this.$t('common.sure')
          //   }).then(res => {
          //     this.$router.push('/exchange');
          //   });
          // } else {
          //   this.handleSell(r.data.id);
          // }
          this.handlePending(r.data.id);
        }).catch(err => {
          let text = '';
          if(err.code == 1006) {
            if(err.message.user) {
              if(err.message.user.indexOf('allow') >= 0) {
                text = this.$t('errors.not_allow_exchange');
              } else if(err.message.user.indexOf('finish') >= 0) {
                text = this.$t('errors.order_not_finish');
              } else if(err.message.user.indexOf('today') >= 0) {
                text = this.$t('errors.buy_order_limit');
              }
            } else if(err.message.time) {
              text = this.$t('errors.now_not_allow_exchange');
            }
          } else if(err.code == 1001) {
            if(err.message.order) {
              text = this.$t('errors.not_match_sell_order');
            } else if(err.message.user) {
              text = this.$t('errors.buy_first');
            }
          } else if(err.code == 1002) {
            text = this.$t('errors.security_psd_not_match');
          } else if(err.code == 1003) {
            if(err.message.failed) {
              text = this.$t('errors.order_failed');
            } else {
              text = this.$t('errors.people_limit');
            }
          } else if(err.code == 1008) {
            text = this.$t('errors.community_wallet_not_enough');
          }
          this.messagebox({
            message: text,
            confirmButtonText: this.$t('common.sure')
          });
        });
      }, 2000);
    },
    handleClick() {
      if(this.activeType == 'sell') {
        this.$get('/member/payment/list').then(res => {
          if(!res.data.total_count) {
            this.messagebox({
              message: this.$t('errors.no_payment'),
              confirmButtonText: this.$t('common.sure')
            }).then(r => {
              this.$router.push('/account/receivable');
            });
            return false;
          } else {
            this.handleSubmit();
          }
        });
      } else {
        this.handleSubmit();
      }
    }
  },
  components:{
    MainContainer,
    PasswordInput
  }
}
</script>

<style lang="scss">
  .order-operation {
    height: 88px;
    &>header {
      position: relative;
      background:linear-gradient(75deg,rgba(19,25,43,1),rgba(43,39,28,1),rgba(13,14,14,1));
      &>.mint-button {
        position: absolute;
        left: 0;
        top: 0;
        background: transparent;
        box-shadow: none;
        border: 0;
        &:active, &:after {
          background: transparent;
        }
        .mint-button-icon {
          i {
            color: #F2D479;
          }
        }
      }
    }
    .mint-navbar {
      height: 88px;
      background: transparent !important;
      a {
        padding: 0;
        .mint-tab-item-label {
          line-height: 88px !important;
          color: #F2D479 !important;
        }
      }
      .mint-tab-item {
        &::before {
          background: #F2D479 !important;
          height: 9px !important;
          width: 70px !important;
        }
      }
    }
    .buy-content {
      margin-top: 7;
    }
    .sell-content {
      margin-top: 7px;
    }

    .sure {
      display: block;
      width: calc(100% - 64px) ;
      height: 104px;
      margin-top: 102px;
      margin-left: 32px;
      font-size: 36px;
      border-radius: 10px;
    }
  }
</style>
