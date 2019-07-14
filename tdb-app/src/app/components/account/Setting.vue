<template>
  <main-container :title="$t('common.setting')" :hasTabbar="false">
    <mt-button slot="left" icon="back" @click.native="$router.push('/account')"></mt-button>
    <div class="account-setting">
      <div class="cell-group mobile">
        <mt-cell :title="$t('common.mobile')" :value="memberProfile.mobile"></mt-cell>
      </div>
      <div class="cell-group">
        <mt-cell
          :title="$t('setting.add_deal_phone')"
          is-link to="/account/setting/mobile">
        </mt-cell>
        <div class="line"></div>
        <mt-cell
          :title="$t('account.password_title')"
          is-link to="/account/setting/password">
        </mt-cell>
        <div class="line"></div>
        <mt-cell
          :title="$t('account.security_psd_title')"
          is-link :to="`/account/setting/security`">
        </mt-cell>
      </div>
      <div class="cell-group">
        <mt-cell :title="$t('account.lang')" is-link to="/account/setting/lang"></mt-cell>
      </div>
      <!-- <div class="cell-group">
        <mt-cell :title="$t('setting.aboutwe')" is-link to="/account/setting/about"></mt-cell>
      </div> -->
      <mt-button @click.native="handleLogout" type="primary">
        {{$t('common.logout')}}
      </mt-button>
    </div>
  </main-container>
</template>
<script>
import store from 'app/store';
import MainContainer from 'app/components/elements/MainContainer';
export default {
  data() {
    return {
      state: store.state,
    };
  },
  computed: {
    memberProfile() {
      return this.state.memberProfile;
    }
  },
  mounted() {
  },
  methods: {
    handleLogout() {
      this.$post('/member/user/logout')
      .then(res => {
        window.localStorage.removeItem('token');
        this.$router.push('/home');
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
  .account-setting {
    .cell-group {
      background-color: #fff;
      margin-bottom: 41px;
      .mint-cell {
        .mint-cell-value {
          span {
            opacity: 0.8;
            font-family: PingFangSC-Regular;
            font-size: 30px;
            color: #545454;
          }
        }
      }
      &.mobile {
        .mint-cell-value {
          span {
            font-weight:500;
            color:rgba(71,71,71,1);
          }
        }
      }
    }
    &>.mint-button {
      display: block;
      // margin-top: 65px;
      margin-top: 328px;
      width: calc(100% - 64px);
      margin-left: 32px;
      opacity: 0.8;
      font-family: PingFangSC-Regular;
      font-size: 34px;
      color: #FFFFFF;
      font-weight: 500;
      border: 0;
      box-shadow: none;
      height: 104px;
      line-height: 104px;
    }
    .line {
      margin-left: 15px;
      border-bottom: 2px solid #eee;
    }
  }
</style>
