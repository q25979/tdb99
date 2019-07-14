<template>
  <main-container :title="$t('account.gender_title')" containerColor="#fff" :hasTabbar="false">
    <mt-button icon="back" slot="left" @click.native="$router.push('/account/profile')"></mt-button>
    <mt-button slot="right" :disabled="cannotSave" @click.native="handleSave">
      {{$t('common.save')}}
    </mt-button>
    <div class="account-profile-nickname">
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
    </div>
  </main-container>
</template>
<script>
import store from 'app/store';
import MainContainer from 'app/components/elements/MainContainer';
export default {
  data() {
    return {
      gender: '',
      state: store.state
    };
  },
  computed: {
    cannotSave() {
      return !this.gender;
    },
  },
  mounted() {
    store.refreshMemberProfile(v => {
      this.gender = this.state.memberProfile.gender;
    });
  },
  methods: {
    handleSave() {
      this.$put('/member/user/current_user', {
        gender: this.gender
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
            background-image: url('../../../assets/img/icon/radio.png');
            background-size: 100% 100%;
          }
          input:checked+label {
            background-image: url('../../../assets/img/icon/radio_selected.png');
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
  }
</style>


