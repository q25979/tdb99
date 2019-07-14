<template>
  <main-container :title="$t('exchange.details_title')" class="buy-box" containerColor='#EDEFF3' :hasTabbar='false'>
    <mt-button icon="back" slot="left" @click.native="$router.go(-1)"></mt-button>
    <mt-button slot="right" :disabled="!canUpload" @click.native="handleBuyConfirm" v-if="!isSell && details.status == 2">
      {{$t('common.save')}}
    </mt-button>
    <mt-button slot="right" :disabled="!canConfirm" @click.native="handleSellConfirm" v-if="isSell && details.status == 4">
      {{$t('common.config')}}
    </mt-button>
    <mt-button slot="right" @click.native="handleCancel(0)" v-if="isSell && details.status == 1">
      {{$t('common.cancel')}}
    </mt-button>
    <div class="buy-detail">
      <details-header :details="details" :isSell="isSell" :imgArr="imgArr"></details-header>
      <div class="buy-info">
        <order-info :details="details"></order-info>
        <payment-info
          :details="details"
          :paymentArr="imgArr"
          v-model="payment"
          :hasPaied="hasPaied"
          :pay="pay"
          v-if="details.side == 2 || (details.match_order && details.match_order.created_timestamp)"></payment-info>
        <proof-img v-if="details.status == 4 || details.status == 8" :details="details"></proof-img>
        <div class="upload" v-if="!isSell && details.status == 2">
          <div class="order-title">{{$t('exchange.details_upload_proof')}}</div>
          <p class="tips">{{$t('exchange.details_proof_tips')}}</p>
          <div class="upload-fields">
            <div
              class="img-field"
              v-for="(item, index) in proof_img"
              :key="index"
              @click="handleTake('modify', index)">
              <img :src="item" alt="">
            </div>
            <div class="img-field" @click="handleTake('add')">
              <img :src="addIcon" alt="" class="add-icon">
            </div>
          </div>
          <!-- <mt-button class="upload-btn" type="primary" :disabled="!canUpload" @click="handleBuyConfirm">
            {{$t('exchange.details_buy_confirm')}}
          </mt-button> -->
          <!-- <mt-button type="danger" class="upload-btn" @click="handleCancel(1)">取消买单</mt-button> -->
        </div>
        <div class="sell-confirm" v-if="isSell && details.status == 4">
          <password-input :placeholder="$t('tips.enter_security_psd')" :label="$t('common.security_psd')" :showForget='true' v-model="security_password"></password-input>
          <!-- <mt-button type="primary" class="confirm-btn" :disabled="!canConfirm" @click="handleSellConfirm">
            {{$t('common.sure')}}
          </mt-button> -->
        </div>
        <!-- <div class="sell-cancel" v-if="isSell && details.status == 1">
          <mt-button type="danger" class="upload-btn" @click="handleCancel(0)">
            {{$t('exchange.details_cancel_sell')}}
          </mt-button> -->
        <!-- </div> -->
      </div>
    </div>

  </main-container>
</template>
<script>
  import PasswordInput from 'app/components/elements/PasswordInput';
  import MainContainer from 'app/components/elements/MainContainer';
  import DetailsHeader from './components/DetailsHeader.vue';
  import PaymentInfo from './components/PaymentInfo.vue';
  import ProofImg from './components/ProofImg.vue';
  import OrderInfo from './components/OrderInfo.vue';
  import store from 'app/store';

  // type 0 银行卡 1 微信 2 支付宝 3 USDT
  export default {
    data() {
      return {
        details: {},
        type: '',
        state: store.state,
        imgArr: [],
        proof_img: [],
        addIcon: require('../../assets/img/add_icon_placeholder.png'),
        activeIndex: 0,
        activeType: 'add',
        security_password: '',
        payment: '',
        hasPaied: false,
        pay: ''
      };
    },
    mounted() {
      store.getRate();
      this.type = this.$route.params.type;
      this.getDetails(() => {
        if(this.details.side == 2) {
          this.$get('/member/payment/list').then(res => {
            for(let item of res.data.objects) {
              item = Object.assign(item, this.getPayment(item.type));
            }
            this.imgArr = res.data.objects;
          });
        } else {
          if(this.details.match_order.created_timestamp) {
            for(let item of this.details.match_order.all_payment) {
              item = Object.assign(item, this.getPayment(item.type));
            }
            this.imgArr = this.details.match_order.all_payment;
          }
        }
        if(this.details.match_order.payment.id) {
          this.hasPaied = true;
          this.pay = Object.assign(this.details.match_order.payment, this.getPayment(this.details.match_order.payment.type));
          this.payment = this.details.match_order.payment.id;
        }
      });
    },
    computed: {
      memberProfile() {
        return this.state.memberProfile;
      },
      isSell() {
        return this.details.side == 2;
      },
      canUpload() {
        return this.proof_img.length && this.payment;
      },
      canConfirm() {
        return this.security_password;
      },
    },
    methods: {
      handleSellConfirm() {
        this.$post(`/member/order/${this.type}/detail/${this.$route.params.number}`, {
          security_password: this.security_password
        }).then(res => {
          this.messagebox({
            message: this.$t('success.finish_exchange'),
            confirmButtonText: this.$t('common.sure')
          }).then(r => {
            this.getDetails();
          });
        });
      },
      handleBuyConfirm() {
        this.$put(`/member/order/${this.type}/detail/${this.$route.params.number}`, {
          proof_img: this.proof_img,
          payment_id: this.payment
        }).then(res => {
          this.messagebox({
            message: this.$t('success.upload'),
            confirmButtonText: this.$t('common.sure')
          }).then(r => {
            this.getDetails();
          });
        });
      },
      handleTake(type, index) {
        this.activeIndex = index;
        this.activeType = type;
        // if(this.activeType == 'add') {
        //   this.$set(this.proof_img, this.proof_img.length, 'http://www.baidu.com/img/bd_logo1.png?qua=high')
        // } else {
        //   this.$set(this.proof_img, this.activeIndex, 'https://ss3.bdstatic.com/70cFv8Sh_Q1YnxGkpoWK1HF6hhy/it/u=85690711,3884201894&fm=27&gp=0.jpg')
        // }
        this.cameraTakePicture(0);
      },
      cameraTakePicture (sourceType) {
        if(navigator.camera) {
          navigator.camera.getPicture(this.onSuccess, this.onFail, {
            quality: 50,
            destinationType: 0,
            encodingType: Camera.EncodingType.JPEG,
            allowEdit: false,
            sourceType: sourceType
          });
        }
      },
      onFail(message) {
        alert(message);
      },
      dataURLtoFile(dataurl) {
        const arr = dataurl.split(',');
        const mime = arr[0].match(/:(.*?);/)[1];
        const bstr = atob(arr[1]);
        let n = bstr.length;
        const u8arr = new Uint8Array(n);
        while (n--) {
          u8arr[n] = bstr.charCodeAt(n);
        }
        return new Blob([u8arr], { type: mime });
      },
      onSuccess(imageData) {
        let imageUrl = "data:image/jpeg;base64," + imageData;
        let param = new FormData();
        param.append('attachment', this.dataURLtoFile(imageUrl));
        this.$upload('/member/upload/image', param).then(r => {
          let key = r.data.key;
          if(this.activeType == 'add') {
            this.$set(this.proof_img, this.proof_img.length, key);
          } else {
            this.$set(this.proof_img, this.activeIndex, key);
          }
        }).catch(err => {
          alert(err);
        });
      },
      getDetails(cb) {
        this.$get(`/member/order/${this.type}/detail/${this.$route.params.number}`).then(res => {
          this.details = res.data;
          // this.details.payment = Object.assign(this.details.payment, this.getPayment(this.details.payment.type));
          if(typeof cb == 'function') {
            cb();
          }
        });
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
          key: key
        };
      },
      handleCancel(type) {
        // type 0 sell_cancel 1 buy_cancel
        this.messagebox({
          message: type ? this.$t('exchange.question_cancel_buy') : this.$t('exchange.question_cancel_sell'),
          showConfirmButton: true,
          showCancelButton: true,
          confirmButtonText: this.$t('common.sure'),
          cancelButtonText: this.$t('common.cancel')
        }).then(r => {
          if(r == 'confirm') {
            this.$delete(`/member/order/${this.type}/detail/${this.$route.params.number}`).then(res => {
              this.messagebox({
                message: type ? this.$t('success.cancel_buy') : this.$t('success.cancel_sell'),
                confirmButtonText: this.$t('common.sure')
              }).then(r => {
                this.getDetails();
              });
            });
          }
        });
      }
    },
    components: {
      MainContainer,
      DetailsHeader,
      PaymentInfo,
      ProofImg,
      PasswordInput,
      OrderInfo,
    },
  };

</script>
<style lang="scss" rel="stylesheet/scss">
  .buy-detail {
    .space-line {
      height: 24px;
      width: 100%;
      background: #F6F7F7;
    }
    .buy-info {
      padding-bottom: 50px;
      margin-top: 18px;

      .upload {
        padding: 32px 0 24px 0;
        background-color: #fff;
        margin-top: 18px;
        .order-title {
          font-family: PingFangSC-Regular;
          font-size: 28px;
          color: #222;
          line-height: 1;
          margin-bottom: 33px;
          padding: 0 32px;
        }

        .tips {
          font-family: PingFangSC-Regular;
          font-size: 24px;
          color: #878787;
          letter-spacing: 0;
          line-height: 33px;
          margin-bottom: 36px;
          padding: 0 32px;
        }
        .upload-fields {
          display: flex;
          align-items: center;
          flex-wrap: wrap;
          margin-bottom: 72px;
          padding: 0 16px;
          .img-field {
            display: flex;
            align-items: center;
            width: calc(25% - 32px);
            height: calc(81.42px * 2 - 16px);
            margin: 16px 16px 0 16px;
            border-radius: 10px;
            overflow: hidden;
            img {
              width: 100%;
              height: 100%;
            }
          }
        }
      }

      .upload-btn {
        display: block;
        width: calc(100% - 64px);
        margin: 30px 32px 0 32px;
      }

      .sell-cancel {
        margin-top: 30px;
      }
    }
    .sell-confirm {
      margin-top: 20px;
      padding-bottom: 32px;
      background-color: #fff;
      .confirm-btn {
        display: block;
        width: calc(100% - 64px);
        margin: 96px 32px 0 32px;
      }
    }
  }

</style>
