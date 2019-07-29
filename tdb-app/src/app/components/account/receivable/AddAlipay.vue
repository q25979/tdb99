<template>
  <main-container :title="$t('receive.alipay_title')" containerColor="#fff" :hasTabbar="false">
    <mt-button icon="back" slot="left" @click.native="$router.go(-1)"></mt-button>
    <div class="bank-form-alipay">
      <mt-field :label="$t('common.aplipay_name')" :placeholder="$t('tips.enter_aplipay_name')" class="common-input" v-model="name"></mt-field>
      <mt-field :label="$t('common.alipay_account')" :placeholder="$t('tips.enter_alipay_account')"  class="common-input" v-model="alipay"></mt-field>
      <password-input :placeholder="$t('tips.enter_security_psd')" :label="$t('common.security_psd')" :showForget='true' v-model="security_password"></password-input>
      <div class="add-qr">
        <p class="qr-title">{{$t('common.add_receive_qrcode')}}</p>
        <div class="add-icon">
          <img :src="alipay_image || addIcon" alt="" @click="handleTake">
        </div>
      </div>
      <mt-button type="primary" :disabled="!canSubmit" class="sure-btn" @click.native="handleClick">
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
      addIcon: require('../../../assets/img/add_icon_placeholder.png'),
      alipay_image: '',
      name: '',
      security_password: '',
      alipay: '',
      token: localStorage.getItem('token')
    }
  },
  computed: {
    canSubmit() {
      return this.name && this.security_password && this.alipay;
    }
  },
  methods: {
    handleTake() {
      this.cameraTakePicture(0);
    },
    cameraTakePicture (sourceType) {
      if(navigator.camera) {
        navigator.camera.getPicture(this.onSuccess, this.onFail, {
          quality: 50,
          destinationType: 0,
          encodingType: Camera.EncodingType.JPEG,
          allowEdit: true,
          sourceType: sourceType
        });
      }
    },
    onFail(message) {
      console.log("Failed");
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
      console.log("Success");
      let imageUrl = "data:image/jpeg;base64," + imageData;
      let param = new FormData();
      param.append('attachment', this.dataURLtoFile(imageUrl));
      this.$upload('/member/upload/image', param).then(r => {
        let key = r.data.key;
        this.alipay_image = key;
      }).catch(err => {
        alert(err);
      });
    },
    handleClick() {
      window.scroll(0, 0);
      this.$post('/member/payment/list', {
        type: 2,
        name: this.name,
        security_password: this.security_password,
        alipay: this.alipay,
        alipay_image: this.alipay_image
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
  .bank-form-alipay {
    width: 100%;
    .add-qr {
      overflow: hidden;
      padding-top: 32px;
      margin-left: 32px;
      .qr-title {
        font-size: 32px;
        line-height: 1;
        color: #222;
        margin-bottom: 19px;
      }
      .add-icon {
        border-radius: 8px;
        width: 120px;
        height: 120px;
        img {
          width: 100%;
          height: 100%;
        }
      }
    }
    .sure-btn {
      display: block;
      width: calc(100% - 64px) ;
      margin: 145px auto 0;
      height: 104px;
    }
  }
</style>

