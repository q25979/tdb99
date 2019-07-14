<template>
  <main-container :title="$t('receive.bank_title')" containerColor="#fff" :hasTabbar="false">
    <mt-button icon="back" slot="left" @click.native="$router.go(-1)"></mt-button>
    <div class="bank-form-bank">
      <mt-field :label="$t('common.name')" :placeholder="$t('tips.enter_real_name')" class="common-input" v-model="name"></mt-field>
      <mt-field :label="$t('common.bank_number')" :placeholder="$t('tips.enter_bank_number')"  class="common-input" v-model="card_number"></mt-field>
      <mt-field :label="$t('common.open_bank')" :placeholder="$t('tips.enter_open_bank')"  class="common-input" v-model="bank"></mt-field>
      <password-input :placeholder="$t('tips.enter_security_psd')" :label="$t('common.security_psd')" :showForget='true' v-model="security_password"></password-input>
      <mt-button type="primary" :disabled="!canSubmit" class="sure-btn" @click.native="handleClick">
        {{$t('common.sure')}}
      </mt-button>
    </div>
  </main-container>
</template>

<script>
import MainContainer from 'app/components/elements/MainContainer';
import PasswordInput from 'app/components/elements/PasswordInput'
export default {
  data() {
    return {
      name: '',
      bank: '',
      card_number: '',
      security_password: ''
    }
  },
  computed: {
    canSubmit() {
      return this.name && this.security_password && this.bank && this.card_number;
    }
  },
  methods: {
    handleClick() {
      window.scroll(0, 0);
      this.$post('/member/payment/list', {
        type: 0,
        name: this.name,
        security_password: this.security_password,
        bank: this.bank,
        card_number: this.card_number
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
  .bank-form-bank {
    width: 100%;
    .add-qr {
      overflow: hidden;
      padding-top: 32px;
      margin-left: 32px;
      .qr-title {
        font-size: 32px;
        line-height: 45px;
        color: #545454 ;
        margin-bottom: 32px;
      }
      .add-icon {
        border: 2px solid #BABABA;
        border-radius: 8px;
        width: 144px;
        height: 144px;
        img {
          &.normal {
            width: 100%;
            height: 100%;
          }
          &.add-icon {
            width: 80px;
            height: 80px;
            display: block;
            margin: 32px auto 32px;
          }
        }
      }
    }
    .sure-btn {
      display: block;
      width: calc(100% - 64px) ;
      margin: 176px auto 0;
      height: 104px;
    }
  }
</style>

