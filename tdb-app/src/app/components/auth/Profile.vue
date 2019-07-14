<template>
  <main-container :hasHeader='false' containerColor='#fff' :noHeader='true' :hasTabbar='false'>
    <div class="auth-profile">
      <header>
        {{$t('auth.profile_title')}}
      </header>
      <mt-field class="common-input" v-model="name" :label="$t('common.name')" :placeholder="$t('tips.set_name')"></mt-field>
      <div class="radio-fields">
        <header>
          {{$t('common.gender')}}
        </header>
        <div class="content">
          <div>
            <input type="radio" id="male" value="1" v-model="gender">
            <label for="male"></label>
            <span @click="gender = '1'">
              {{$t('common.male')}}
            </span>
          </div>
          <div>
            <input type="radio" id="female" value="2" v-model="gender">
            <label for="female"></label>
            <span @click="gender = '2'">
              {{$t('common.female')}}
            </span>
          </div>
        </div>
      </div>
      <mt-field class="common-input" v-model="nickname" :label="$t('common.nickname')" :placeholder="$t('tips.set_nickname')"></mt-field>
      <mt-field class="common-input" v-model="wechat" :label="$t('common.wechat_account')" :placeholder="$t('tips.set_wechat')"></mt-field>
      <mt-button type="primary" :disabled="!canSubmit" @click="handleClick">
       {{$t('common.sure')}}
      </mt-button>
    </div>
  </main-container>
</template>
<script>
import MainContainer from 'app/components/elements/MainContainer';
import store from 'app/store';
export default {
  data() {
    return {
      name: '',
      nickname: '',
      gender: '',
      wechat: '',
      state: store.state,
    };
  },
  computed: {
    canSubmit() {
      return this.name && this.nickname && this.gender && this.wechat;
    }
  },
  mounted() {
  },
  methods: {
    handleClick() {
      this.$put('/member/user/current_user', {
        name: this.name,
        gender: this.gender,
        nickname: this.nickname,
        wechat: this.wechat
      }).then(res => {
        store.updateMemberProfile(res.data);
        this.$router.push('/answer');
      });
    }
  },
  components: {
    MainContainer,
  }
};
</script>
<style lang="scss" rel="stylesheet/scss">
  .auth-profile {
    .mint-cell {
      .mint-cell-wrapper {
        background: transparent !important;
      }
    }
    &>header {
      margin-top: 58px;
      font-family: PingFangSC-Regular;
      font-size: 64px;
      color: #222;
      padding-left: 32px;
      margin-bottom: 37px;
      line-height: 1;
    }
    .radio-fields {
      header {
        font-size: 32px;
        color: #545454;
        padding: 0 32px;
        margin-top: 32px;
      }
      .content {
        display: flex;
        align-items: center;
        padding: 0 32px;
        height: 50px;
        margin-top: 16px;
        justify-content: space-around;
        &>div {
          display: flex;
          align-items: center;
          position: relative;
          height: 50px;
          &:last-child {
            margin-right: 0;
          }
          input {
            opacity: 0;
            width: 40px;
            height: 40px;
            margin: 0;
          }
          label {
            width: 32px;
            height: 32px;
            position: absolute;
            left: 0;
            border-radius: 50%;
            background-image: url('../../assets/img/icon/radio.png');
            background-size: 100% 100%;
          }
          input:checked+label {
            background-image: url('../../assets/img/icon/radio_selected.png');
          }

          input:checked+label::after {
          }
          span {
            font-size: 30px;
            color: #000000;
            margin-left: 19px;
          }
        }
      }
    }
    &>.mint-button {
      margin: 0 32px;
      display: block;
      width: calc(100% - 64px);
      box-shadow: none;
      border: 0;
      font-family: PingFangSC-Regular;
      font-size: 36px;
      margin-top: 81px;
      opacity: 1 !important;
      height: 104px;
    }
  }
</style>
