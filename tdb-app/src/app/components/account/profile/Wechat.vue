<template>
  <main-container :title="$t('account.wechat_title')" :hasTabbar="false">
    <mt-button icon="back" slot="left" @click.native="$router.push('/account/profile')"></mt-button>
    <mt-button slot="right" :disabled="cannotSave" @click.native="handleSave">
      {{$t('common.save')}}
    </mt-button>
    <div class="account-profile-nickname">
      <mt-field class="common-input" :label="$t('common.wechat')" :placeholder="$t('tips.set_wechat')" v-model="wechat"></mt-field>
    </div>
  </main-container>
</template>
<script>
import store from 'app/store';
import MainContainer from 'app/components/elements/MainContainer';
export default {
  data() {
    return {
      wechat: '',
      state: store.state
    };
  },
  computed: {
    cannotSave() {
      return !this.wechat;
    },
  },
  mounted() {
    store.refreshMemberProfile(v => {
      this.wechat = this.state.memberProfile.wechat;
    });
  },
  methods: {
    handleSave() {
      window.scroll(0, 0);
      this.$put('/member/user/current_user', {
        wechat: this.wechat
      })
      .then(resp => {
        store.updateMemberProfile(resp.data);
        let index = this.toast({
          iconClass: 'icon icon-success-check'
        });
        setTimeout(v => {
          index.close();
        }, 2000);
      })
      .catch(err => {
      });
    }
  },
  components: {
    MainContainer
  }
};
</script>
<style lang="scss">
  .account-profile-nickname {
    .tips {
      padding: 0 32px;
      font-family: PingFangSC-Regular;
      font-size: 28px;
      color: #545454;
      margin-top: 24px;
    }
    .common-input {
      .mint-cell-wrapper {
        padding-bottom: 32px !important;
      }
    }
  }
</style>


