<template>
  <main-container :title="$t('account.title')">
    <i class="icon icon-setting" slot="right" @click="$router.push('/account/setting')"></i>
    <div class="account">
      <mt-cell class="profile" is-link to="/account/profile">
        <img :src="memberProfile.avatar || defaultAvatar" class="avatar" alt="" slot="icon">
        <div class="details" slot="title">
          <header>
            <div class="name">{{memberProfile.nickname}}</div>
            <div class="uid">UID: {{memberProfile.uid}}</div>
            <div class="uid">{{getLevel(memberProfile.is_community_node)}}</div>
          </header>
        </div>
      </mt-cell>
      <div class="cell-group">
        <mt-cell is-link to="/account/invite">
          <i class="icon icon-invite" slot="icon"></i>
          <span slot="title">
          {{$t('account.invite_title')}}
          </span>
        </mt-cell>
        <div class="line"></div>
        <mt-cell is-link to="/account/friend">
          <i class="icon icon-friend" slot="icon"></i>
          <span slot="title">
           {{$t('account.friend_title')}}
          </span>
        </mt-cell>
      </div>
      <div class="cell-group">
        <mt-cell is-link to="/account/receivable">
          <i class="icon icon-address" slot="icon"></i>
          <span slot="title">
            {{$t('account.receive_title')}}
          </span>
        </mt-cell>
      </div>
      <div class="cell-group">
        <mt-cell is-link to="/account/news">
          <i class="icon icon-notice" slot="icon"></i>
          <span slot="title">
           {{$t('account.news_title')}}
          </span>
        </mt-cell>
        <div class="line"></div>
        <mt-cell is-link to="/account/contact">
          <i class="icon icon-contact" slot="icon"></i>
          <span slot="title">
            {{$t('account.contact_title')}}
          </span>
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
  mounted() {
    store.refreshMemberProfile();
  },
  methods: {
    getLevel(level) {
      if(level == 1) {
        return this.$t('level_1');
      } else {
        return this.$t('level_0');
      }
    }
  },
  components: {
    MainContainer
  }
};
</script>
<style lang="scss" rel="stylesheet/scss">
  .icon-setting {
    height: 40px;
    width: 40px;
    background-image: url('../../assets/img/icon/setting_gray.png');
  }
  .account {
    .profile {
      height: 205px;
      background:linear-gradient(75deg,rgba(19,25,43,1),rgba(43,39,28,1),rgba(13,14,14,1));
      .mint-cell-wrapper {
        height: 205px;
        background:linear-gradient(75deg,rgba(19,25,43,1),rgba(43,39,28,1),rgba(13,14,14,1)) !important;
      }
      .mint-cell-allow-right::after {
        border-color: rgba(242,212,121,1) !important;
      }
      .mint-cell-title {
        img.avatar {
          width: 120px;
          height: 120px;
          border-radius: 4px;
        }
        .details {
          margin-left: 32px;
          header {
            font-family: PingFangSC-Medium;
            font-size: 34px;
            color: rgba(242,212,121,1);
            .name {
              line-height: 48px;
              margin-bottom: 5px;
              color: rgba(242,212,121,1);
            }
            .uid {
              color: rgba(242,212,121,1);
              font-size: 28px;
              line-height: 40px;
            }
          }
          // div {
          //   margin-top: 15px;
          //   font-family: PingFangSC-Regular;
          //   font-size: 28px;
          //   color: rgba(255,255,255,0.70);
          // }
        }
      }
    }
    .cell-group {
      background-color: #fff;
      &.profit {
        .mint-cell-title {
          span {
            margin-left: 0 !important;
          }
        }
      }
      .icon {
        width: 40px;
        height: 40px;
        &.icon-notice {
          background-image: url('../../assets/img/icon/notice_blue.png');
        }
        &.icon-address {
          background-image: url('../../assets/img/icon/address_green.png');
        }
        &.icon-contact {
          background-image: url('../../assets/img/icon/contact_purple.png');
        }
        &.icon-invite {
          background-image: url('../../assets/img/icon/invite_orange.png');
        }
        &.icon-friend {
          background-image: url('../../assets/img/icon/friend_blue.png');
        }
      }
      margin-top: 29px;
      .mint-cell {
        .mint-cell-title {
          span {
            font-family: PingFangSC-Regular;
            font-size: 28px;
            color: #222;
            margin-left: 24px;
          }
        }
      }
    }
    .line {
      margin-left: 15px;
      border-bottom: 2px solid #eee;
    }
  }
</style>
