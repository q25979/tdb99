<template>
  <main-container :title="$t('common.huazhuan')" :hasTabbar="false" containerColor="#fff">
    <mt-button icon="back" slot="left" @click.native="$router.go(-1)"></mt-button>
    <div class="finance-exchange">
      <mt-field class="common-input" :label="$t('common.min_value')" :value="minVal" disabled></mt-field>
      <mt-field class="common-input" :label="$t('common.max_value')" :value="maxVal" disabled></mt-field>
      <mt-field class="common-input" :label="$t('common.count')" :placeholder="$t('tips.enter_huazhuan_count')" type="number" v-model.number="amount">
      </mt-field>
      <div class="tips">{{$t('huazhuan.tips1')}}</div>
      <password-input :placeholder="$t('tips.enter_security_psd')" :label="$t('common.security_psd')" v-model="securityPsd" :showForget="true"></password-input>
      <mt-button type="primary" :disabled="!canSubmit" @click.native="handleClick">
        {{$t('common.sure')}}
      </mt-button>
    </div>
  </main-container>
</template>
<script>
import MainContainer from 'app/components/elements/MainContainer';
import PasswordInput from 'app/components/elements/PasswordInput';
export default {
  data() {
    return {
      maxVal: '',
      minVal: '',
      amount: '',
      securityPsd: ''
    };
  },
  mounted() {
    this.$get('/member/setting').then(res => {
      this.maxVal = res.data.value.exchange_amount_max.toFixed(8),
      this.minVal = res.data.value.exchange_amount_min.toFixed(8)
    });
  },
  computed: {
    canSubmit() {
      return (this.amount % 500 == 0) && (this.amount > 0) && this.securityPsd;
    }
  },
  methods: {
    handleClick() {
      this.$post('/member/assets/exchange', {
        amount: this.amount,
        security_password: this.securityPsd
      }).then(r => {
        this.messagebox({
          message: this.$t('success.huazhuan'),
          confirmButtonText: this.$t('common.sure')
        }).then(res => {
          this.amount = '';
          this.securityPsd = '';
        });
      }).catch(err => {
        let text = '';
        switch(err.code) {
        case 1006:
          text = this.$t('errors.huanzhuan_count_error');
          break;
        case 1008:
          text = this.$t('errors.exchange_wallet_not_enough');
          break;
        case 1002:
          text = this.$t('errors.security_psd_not_match');
          break;
        }
        this.messagebox({
          message: text,
          confirmButtonText: this.$t('common.sure')
        });
      });
    }
  },
  components: {
    MainContainer,
    PasswordInput
  }
};
</script>
<style lang="scss">
  .finance-exchange {
    &>.mint-button {
      display: block;
      width: calc(100% - 64px);
      height: 104px;
      margin-top: 96px;
      margin-left: 32px;
      font-size: 36px;
      border-radius: 10px;
    }
    &>.tips {
      padding: 32px 32px 0;
      font-size: 28px;
      color: #222;
    }
  }
</style>
