<template>
  <main-container :title="$t('account.password_title')" :hasTabbar="false" containerColor="#fff">
    <mt-button icon="back" slot="left" @click.native="$router.push('/account/setting')"></mt-button>
    <mt-button slot="right" :disabled="!canSubmit" @click.native="handleSave">
      {{$t('common.save')}}
    </mt-button>
    <div class="account-setting-security">
      <password-input :label="$t('common.old_psd')" :placeholder="$t('tips.enter_old_psd')" v-model="oldPsd"></password-input>
      <password-input :label="$t('common.new_psd')" :placeholder="$t('tips.enter_new_psd')" v-model="newPsd"></password-input>
      <password-input :label="$t('common.confirm_psd')" v-model="rePsd" :placeholder="$t('tips.enter_new_psd_again')"></password-input>
      <div class="tips">
        {{$t('rule.login_psd')}}
      </div>
    </div>
  </main-container>
</template>
<script>
import PasswordInput from 'app/components/elements/PasswordInput';
import MainContainer from 'app/components/elements/MainContainer';
export default {
  data() {
    const numReg = /^[a-zA-Z\w]{6,20}$/;
    return {
      oldPsd: '',
      newPsd: '',
      rePsd: '',
      numReg
    };
  },
  computed: {
    canSubmit() {
      return this.oldPsd && this.newPsd && this.rePsd;
    }
  },
  mounted() {
  },
  methods: {
    handleSave() {
      window.scroll(0, 0);
      if(!(this.numReg.test(this.oldPsd) && this.numReg.test(this.newPsd) && this.numReg.test(this.rePsd))) {
        this.messagebox({
          message: this.$t('rule.login_psd'),
          confirmButtonText: this.$t('common.sure')
        });
        return false;
      } else if(this.newPsd !== this.rePsd) {
        this.messagebox({
          message: this.$t('errors.password_twice_not_same'),
          confirmButtonText: this.$t('common.sure')
        });
        return false;
      }

      this.$put('/member/user/current_user', {
        new_password: this.newPsd,
        old_password: this.oldPsd,
      })
      .then(resp => {
        this.newPsd = '';
        this.oldPsd = '';
        this.rePsd = '';
        let index = this.toast({
          iconClass: 'icon icon-success-check'
        });
        setTimeout(v => {
          index.close();
        }, 2000);
      })
      .catch(err => {
        if(err.code == 1002) {
          this.messagebox({
            message: this.$t('errors.old_psd_not_match'),
            confirmButtonText: this.$t('common.sure')
          });
        }
      });
    }
  },
  components: {
    PasswordInput,
    MainContainer
  }
};
</script>
<style lang="scss">
  .account-setting-security {
    // padding-top: 8px;
    .tips {
      font-family: PingFangSC-Regular;
      font-size: 24px;
      color: #818181;
      margin-top: 21px;
      padding: 0 32px;
    }
  }
</style>

