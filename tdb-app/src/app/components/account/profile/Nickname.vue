<template>
  <main-container :title="$t('account.nickname_title')" :hasTabbar="false">
    <mt-button icon="back" slot="left" @click.native="$router.push('/account/profile')"></mt-button>
    <mt-button slot="right" :disabled="cannotSave" @click.native="handleSave">
      {{$t('common.save')}}
    </mt-button>
    <div class="account-profile-nickname">
      <mt-field class="common-input" :label="$t('common.nickname')" :placeholder="$t('tips.set_nickname')" v-model="nickname"></mt-field>
    </div>
  </main-container>
</template>
<script>
import store from 'app/store';
import MainContainer from 'app/components/elements/MainContainer';
export default {
  data() {
    return {
      nickname: '',
      state: store.state
    };
  },
  computed: {
    cannotSave() {
      return !this.nickname;
    },
  },
  mounted() {
    store.refreshMemberProfile(v => {
      this.nickname = this.state.memberProfile.nickname;
    });
  },
  methods: {
    handleSave() {
      window.scroll(0, 0);
      this.$put('/member/user/current_user', {
        nickname: this.nickname
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


