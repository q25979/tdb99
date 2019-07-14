<template>
  <div class="payment-info">
    <header :class="hasPaied ? 'noborder' : ''">
      <!-- {{hasPaied ? $t('common.payment_way') : $t('common.select_payment')}} -->
      {{$t('common.select_payment')}}
    </header>
    <div class="group">
      <div class="item" v-for="(item, index) in paymentArr" :key="index">
        <header @click="payment = item.id">
          <div class="left">
            <input type="radio" name="payment" :value="item.id" v-model="payment">
            <label for="male"></label>
            <div class="text">
              <i :class="`icon ${item.key}`"></i>
              <span>
                {{item.label}}
              </span>
            </div>
          </div>
          <div class="right">
            <img src="../../../assets/img/icon/link_icon.png" alt="" :class="payment == item.id ? 'reverse' : ''">
          </div>
        </header>
        <div class="content" v-show="payment == item.id">
          <div v-if="item.type == 3">
            <span class="title">{{$t('common.usdt_address')}}</span> ：
            <span class="field">{{item.address}}</span>
            <mt-button
              class="copy-btn"
              v-clipboard:copy="item.address"
              v-clipboard:success="copySuccess"
              v-clipboard:error="copyError">
              {{$t('common.copy')}}
            </mt-button>
          </div>
          <div v-if="item.type == 2">
            <span class="title">{{$t('common.aplipay_name')}}</span> ：
            <span class="field">{{item.name}}</span>
          </div>
          <div v-if="item.type == 2">
            <span class="title">{{$t('common.alipay_account')}}</span> ：
            <span class="field">{{item.alipay}}</span>
            <mt-button
              class="copy-btn"
              v-clipboard:copy="item.alipay"
              v-clipboard:success="copySuccess"
              v-clipboard:error="copyError">
              {{$t('common.copy')}}
            </mt-button>
          </div>
          <div v-if="item.type == 2">
            <span class="title">{{$t('common.payment_qrcode')}}</span> ：
            <span class="field">
              <img v-gallery :src="item.alipay_image" alt="">
            </span>
          </div>
          <div v-if="item.type == 0">
            <span class="title">{{$t('common.open_bank')}}</span> ：
            <span class="field">{{item.bank}}</span>
          </div>
          <div v-if="item.type == 0">
            <span class="title">{{$t('common.bank_number')}}</span> ：
            <span class="field">{{item.card_number}}</span>
            <mt-button
              class="copy-btn"
              v-clipboard:copy="item.card_number"
              v-clipboard:success="copySuccess"
              v-clipboard:error="copyError">
              {{$t('common.copy')}}
            </mt-button>
          </div>
          <div v-if="item.type == 0">
            <span class="title">{{$t('common.name')}}</span> ：
            <span class="field">{{item.name}}</span>
          </div>
          <div v-if="item.type == 1">
            <span class="title">{{$t('common.wechat_name')}}</span> ：
            <span class="field">{{item.name}}</span>
          </div>
          <div v-if="item.type == 1">
            <span class="title">{{$t('common.wechat_account')}}</span> ：
            <span class="field">{{item.wechat}}</span>
            <mt-button
              class="copy-btn"
              v-clipboard:copy="item.wechat"
              v-clipboard:success="copySuccess"
              v-clipboard:error="copyError">
              {{$t('common.copy')}}
            </mt-button>
          </div>
          <div v-if="item.type == 1">
            <span class="title">{{$t('common.payment_qrcode')}}</span> ：
            <span class="field">
              <img v-gallery :src="item.wechat_image" alt="">
            </span>
          </div>
        </div>
      </div>
    </div>
    <div class="group-paied" v-if="false">
      <header>
        <i :class="`icon ${pay.key}`"></i>
        <span>
          {{pay.label}}
        </span>
      </header>
      <div class="content">
        <div v-if="pay.type == 3">
          <span class="title">{{$t('common.usdt_address')}}：</span>
          <span class="field">{{pay.address}}</span>
          <mt-button
            class="copy-btn"
            v-clipboard:copy="pay.address"
            v-clipboard:success="copySuccess"
            v-clipboard:error="copyError">
            {{$t('common.copy')}}
          </mt-button>
        </div>
        <div v-if="pay.type == 2">
          <span class="title">{{$t('common.aplipay_name')}}：</span>
          <span class="field">{{pay.name}}</span>
        </div>
        <div v-if="pay.type == 2">
          <span class="title">{{$t('common.alipay_account')}}：</span>
          <span class="field">{{pay.alipay}}</span>
          <mt-button
            class="copy-btn"
            v-clipboard:copy="pay.alipay"
            v-clipboard:success="copySuccess"
            v-clipboard:error="copyError">
            {{$t('common.copy')}}
          </mt-button>
        </div>
        <div v-if="pay.type == 2">
          <span class="title">{{$t('common.payment_qrcode')}}：</span>
          <span class="field">
            <img v-gallery :src="pay.alipay_image" alt="">
          </span>
        </div>
        <div v-if="pay.type == 0">
          <span class="title">{{$t('common.open_bank')}}：</span>
          <span class="field">{{pay.bank}}</span>
        </div>
        <div v-if="pay.type == 0">
          <span class="title">{{$t('common.bank_number')}}：</span>
          <span class="field">{{pay.card_number}}</span>
          <mt-button
            class="copy-btn"
            v-clipboard:copy="pay.card_number"
            v-clipboard:success="copySuccess"
            v-clipboard:error="copyError">
            {{$t('common.copy')}}
          </mt-button>
        </div>
        <div v-if="pay.type == 0">
          <span class="title">{{$t('common.name')}}：</span>
          <span class="field">{{pay.name}}</span>
        </div>
        <div v-if="pay.type == 1">
          <span class="title">{{$t('common.wechat_name')}}：</span>
          <span class="field">{{item.name}}</span>
        </div>
        <div v-if="pay.type == 1">
          <span class="title">{{$t('common.wechat_account')}}：</span>
          <span class="field">{{pay.wechat}}</span>
          <mt-button
            class="copy-btn"
            v-clipboard:copy="pay.wechat"
            v-clipboard:success="copySuccess"
            v-clipboard:error="copyError">
            {{$t('common.copy')}}
          </mt-button>
        </div>
        <div v-if="pay.type == 1">
          <span class="title">{{$t('common.payment_qrcode')}}：</span>
          <span class="field">
            <img v-gallery :src="pay.wechat_image" alt="">
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  export default {
    props: ['allPayment', 'paymentArr', 'value', 'hasPaied', 'pay'],
    data() {
      return {
      };
    },
    model: {
      prop: 'value',
      event: 'update'
    },
    computed: {
      payment: {
        get() {
          return this.value;
        },
        set(val) {
          this.$emit("update", val);
        }
      }
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
      }
    }
  }
</script>

<style lang="scss">
  .payment-info {
    margin-top: 18px;
    background-color: #fff;
    &>header {
      font-size: 28px;
      color: #222;
      line-height: 1;
      padding: 24px 32px;
      border-bottom: 5px solid #f1f1f1;
      &.noborder {
        border: 0;
      }
    }
    &>.group {
      .item {
        border-bottom: 2px solid #f1f1f1;
        &:last-child {
          border: 0;
        }
        &>header {
          height: 73px;
          display: flex;
          align-items: center;
          justify-content: space-between;
          padding: 0 32px;
          .left {
            display: flex;
            align-items: center;
            position: relative;
            .text {
              display: flex;
              align-items: center;
              i {
                width: 36px;
                height: 36px;
              }
              span {
                color: #222;
                font-size: 30px;
                margin-left: 25px;
              }
            }
            input {
              opacity: 0;
              width: 27px;
              height: 27px;
              margin: 0 25px 0 0;
            }
            label {
              width: 27px;
              height: 27px;
              position: absolute;
              left: 0;
              border-radius: 50%;
              background-image: url('../../../assets/img/icon/radio.png');
              background-size: 100% 100%;
            }
            input:checked+label {
              background-image: url('../../../assets/img/icon/radio_select_green.png');
            }

            input:checked+label::after {
            }
          }
          .right {
            display: flex;
            align-items: center;
            img {
              width: 24px;
              transform: rotate(-90deg);
              &.reverse {
                transform: rotate(0deg);
              }
            }
          }
        }
        .content {
          padding: 20px 32px 42px;
          &>div {
            display: flex;
            align-items: center;
            margin-bottom: 26px;
            font-size: 24px;
            color: #9B9B9B;
            &:last-child {
              margin-bottom: 0;
            }
            span {
              &.title {
                width: 220px;
                text-align: right;
              }
              &.field {
                width: calc(100% - 220px);
                img {
                  width: 48px;
                  height: 48px;
                }
                &:nth-child(2) {
                  width: auto;
                  max-width: calc(100% - 240px - 135px);
                  word-wrap: break-word; 
                  overflow: hidden;
                }
              }
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
    }
    &>.group-paied {
      padding: 0 32px;
      &>header {
        display: flex;
        align-items: center;
        margin-bottom: 26px;
        i {
          width: 36px;
          height: 36px;
        }
        span {
          color: #222;
          font-size: 30px;
          margin-left: 25px;
        }
      }
      &>.content {
        padding-bottom: 32px;
        .copy-btn {
          width: 96px;
          font-size: 24px;
          padding: 0;
          height: 40px;
          line-height: 40px;
          background-color: #fff;
          border-radius: 20px;
          margin-left: 15px;
        }
        &>div {
          display: flex;
          align-items: center;
          margin-bottom: 26px;
          font-size: 24px;
          &:last-child {
            margin-bottom: 0;
          }
          span {
            &.title {
              color: #9b9b9b;
              text-align: left;
              width: 40%;
            }
            &.field {
              color: #9b9b9b;
              text-align: right;
              img {
                width: 48px;
                height: 48px;
              }
              &:nth-child(2) {
                width: calc(60% - 111px);
                word-wrap: break-word;
              }
              &:last-child {
                width: 60%;
              }
            }
          }
        }
      }
    }
  }
</style>
