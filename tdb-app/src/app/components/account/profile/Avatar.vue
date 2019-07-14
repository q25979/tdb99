<template>
  <main-container :title="$t('account.avatar_title')" containerColor="#fff" :hasTabbar="false">
    <mt-button icon="back" slot="left" @click.native="$router.push('/account/profile')"></mt-button>
    <div class="account-profile-avatar">
      <header>
        <img :src="memberProfile.avatar || defaultAvatar" alt="">
      </header>
      <div class="btn-group">
        <mt-button @click.native="handleFromCam" type="primary">
          {{$t('account.avatar_from_album')}}
        </mt-button>
        <mt-button @click.native="handleTake" type="primary">
          {{$t('account.avatar_from_photo')}}
        </mt-button>
      </div>
    </div>
  </main-container>
</template>
<script>
import store from 'app/store';
import MainContainer from 'app/components/elements/MainContainer';
export default {
  data() {
    return {
      defaultAvatar: require('../../../assets/img/default_avatar.png'),
      state: store.state,
      token: localStorage.getItem('token'),
    }
  },
  computed: {
    memberProfile() {
      this.name = this.state.memberProfile.name;
      return this.state.memberProfile;
    }
  },
  methods: {
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
    handleFromCam() {
      this.cameraTakePicture(0);
    },
    handleTake() {
      this.cameraTakePicture(1);
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
    },
    onSuccess(imageData) {
      let imageUrl = "data:image/jpeg;base64," + imageData;
      let param = new FormData();
      param.append('attachment', this.dataURLtoFile(imageUrl));
      this.$upload('/member/upload/image', param).then(r => {
        let key = r.data.key;
        this.$put('/member/user/current_user', {
          avatar: key
        })
        .then(resp => {
          this.state.memberProfile.avatar = imageUrl;
          let index = this.toast({
            iconClass: 'icon icon-success-check'
          });
          setTimeout(v => {
            index.close();
          }, 2000);
        })
        .catch(err => {
          this.messagebox({
            message: this.$t('errors.server_busy'),
            confirmButtonText: this.$t('common.sure')
          });
        });
      }).catch(err => {
        alert(err);
      });
    },
  },
  components: {
    MainContainer
  }
};
</script>
<style lang="scss">
  .account-profile-avatar {
    header {
      margin-top: 27px;
      img {
        width: 750px;
        height: 750px;
      }
    }
    .btn-group {
      padding: 0 32px;
      margin-top: 75px;
      .mint-button {
        display: block;
        width: 100%;
        border-radius: 10px;
        font-family: PingFangSC-Regular;
        font-size: 36px;
        color: #FFFFFF;
        height: 104px;
        &:last-child {
          margin-top: 30px;
        }
      }
    }
  }
</style>

