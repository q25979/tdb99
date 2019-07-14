<template>
  <main-container :title="$t('receive.usdt_title')" containerColor="#fff" :hasTabbar="false">
    <mt-button icon="back" slot="left" @click.native="$router.go(-1)"></mt-button>
    <mt-button slot="right" @click.native="handleScan">
      <img class="more" src="../../../assets/img/receipt_icon_22x.png" height="22" width="22" slot="icon">
    </mt-button>
    <div class="bank-form-usdt">
      <mt-field :label="$t('common.usdt_address')" :placeholder="$t('tips.enter_usdt_address')"  class="common-input" v-model="address"></mt-field>
      <mt-field :label="$t('common.remark')" :placeholder="$t('tips.enter_remark')"  class="common-input" v-model="remark"></mt-field>
      <password-input :placeholder="$t('tips.enter_security_psd')" :label="$t('common.security_psd')" :showForget='true' v-model="security_password"></password-input>
      <mt-button type="primary" :disabled="!canSubmit" class="sure-btn" @click.native="handleClick">
        {{$t('common.sure')}}
      </mt-button>
    </div>
  </main-container>
</template>

<script>
import MainContainer from 'app/components/elements/MainContainer';
import PasswordInput from 'app/components/elements/PasswordInput'
export default {
  data() {
    return {
      address: '',
      remark: '',
      security_password: ''
    }
  },
  computed: {
    canSubmit() {
      return this.address && this.security_password && this.remark;
    }
  },
  methods: {
    handleScan() {
      cordova.plugins.barcodeScanner.scan(
        result=> {
          this.address = result.text;
        },
        error=> {
          this.messagebox({
            message: this.$t('errors.server_busy'),
            confirmButtonText: this.$t('common.sure')
          });
        },
        {
          preferFrontCamera: false, // iOS and Android
          showFlipCameraButton: false, // iOS and Android
          showTorchButton: true, // iOS and Android
          torchOn: false, // Android, launch with the torch switched on (if available)
          //saveHistory: true, // Android, save scan history (default false)
          prompt: this.$t('tips.qrcode_center'), // Android
          resultDisplayDuration: 500, // Android, display scanned text for X ms. 0 suppresses it entirely, default 1500
          //formats: "QR_CODE,PDF_417", // default: all but PDF_417 and RSS_EXPANDED
          //orientation: "landscape", // Android only (portrait|landscape), default unset so it rotates with the device
          disableAnimations: true, // iOS
          disableSuccessBeep: false // iOS and Android
        }
      );
    },
    handleClick() {
      window.scroll(0, 0);
      this.$post('/member/payment/list', {
        type: 3,
        security_password: this.security_password,
        address: this.address,
        remark: this.remark
      }).then(res => {
        this.$router.push('/account/receivable');
      }).catch(err => {
        if(err.code == 1002) {
          this.messagebox({
            message: this.$t('errors.security_psd_not_match'),
            confirmButtonText: this.$t('common.sure')
          });
        }
      });
    }
  },
  components:{
    MainContainer,
    PasswordInput
  }
}
</script>

<style lang="scss" >
  .more {
    width: 40px;
    height: 40px;
  }
  .bank-form-usdt {
    width: 100%;
  
    .add-qr {
      overflow: hidden;
      padding-top: 32px;
      margin-left: 32px;
      .qr-title {
        font-size: 32px;
        line-height: 45px;
        color: #545454 ;
        margin-bottom: 32px;
      }
      .add-icon {
        border: 2px solid #BABABA;
        border-radius: 8px;
        width: 144px;
        height: 144px;
        img {
          &.normal {
            width: 100%;
            height: 100%;
          }
          &.add-icon {
            width: 80px;
            height: 80px;
            display: block;
            margin: 32px auto 32px;
          }
        }
      }
    }
    .sure-btn {
      display: block;
      width: calc(100% - 64px) ;
      margin: 348px auto 0;
      height: 104px;
    }
  }
</style>

