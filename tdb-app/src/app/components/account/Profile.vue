<template>
  <main-container :title="$t('account.profile_title')" :hasTabbar="false">
    <mt-button icon="back" slot="left" @click.native="$router.push('/account')"></mt-button>
    <div class="account-profile">
      <div class="group">
        <mt-cell :title="$t('common.avatar')" is-link to="/account/profile/avatar">
          <img :src="memberProfile.avatar || defaultAvatar" alt="" class="avatar">
        </mt-cell>
        <div class="line"></div>
        <mt-cell :title="$t('common.name')" is-link to="/account/profile/name">
          {{memberProfile.name}}
        </mt-cell>
        <div class="line"></div>
        <mt-cell :title="$t('common.gender')" is-link to="/account/profile/gender">
          {{memberProfile.gender == 2 ? $t('common.female') : $t('common.male')}}
        </mt-cell>
        <div class="line"></div>
        <mt-cell :title="$t('common.nickname')" is-link to="/account/profile/nickname">
          {{memberProfile.nickname}}
        </mt-cell>
        <div class="line"></div>
        <mt-cell :title="$t('common.wechat_account')" is-link to="/account/profile/wechat">
          {{memberProfile.wechat}}
        </mt-cell>
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
      defaultAvatar: require('../../assets/img/default_avatar.png'),
      state: store.state
    };
  },
  computed: {
    memberProfile() {
      return this.state.memberProfile;
    }
  },
  components: {
    MainContainer
  }
};
</script>
<style lang="scss">
  .account-profile {
    .group {
      background-color: #fff;
    }
    .mint-cell {
      .avatar {
        width: 120px;
        height: 120px;
        border-radius: 4px;
      }
    }
    .line {
      margin-left: 15px;
      border-bottom: 2px solid #eee;
    }
  }
</style>


