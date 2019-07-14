<template>
  <main-container :title="$t('common.transfer')" :hasTabbar="false" containerColor="#fff">
    <mt-button icon="back" slot="left" @click.native="$router.go(-1)"></mt-button>
    <div class="finance-transfer">
      <mt-field class="common-input" :label="$t('common.mobile')" v-model="mobile" :placeholder="$t('tips.enter_other_mobile')">
      </mt-field>
      <mt-field class="common-input" :label="$t('common.fee')" v-model="fee" disabled>
      </mt-field>
      <mt-field class="common-input" :label="$t('common.count')" type="number" v-model.number="amount" :placeholder="$t('tips.enter_transfer_count')">
      </mt-field>
      <mt-field class="common-input" :label="$t('common.actual_count')" v-model="totalAmount">
      </mt-field>
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
import {Decimal} from 'decimal.js';
export default {
  data() {
    return {
      mobile: '',
      amount: '',
      securityPsd: '',
      fee: '',
      totalAmount: '0'
    };
  },
  mounted() {
    this.$get('/member/setting').then(r => {
      this.fee = r.data.value.community_transaction_fee_rate;
    });
  },
  computed: {
    canSubmit() {
      return this.mobile && this.amount && (this.amount > 0) && this.securityPsd;
    }
  },
  methods: {
    handleClick() {
      this.$post('/member/assets/transaction', {
        mobile: this.mobile,
        amount: this.amount,
        security_password: this.securityPsd
      }).then(r => {
        this.messagebox({
          message: this.$t('success.transfer'),
          confirmButtonText: this.$t('common.sure')
        }).then(res => {
          this.mobile = '';
          this.amount = '';
          this.securityPsd = '';
        });
      }).catch(err => {
        let text = '';
        switch(err.code) {
        case 1001:
          if(err.message.mobile) {
            text = this.$t('errors.mobile_not_exist');
          } else if(err.message.current_user) {
            text = this.$t('errors.not_community_node');
          } else if(err.message.user) {
            text = this.$t('errors.other_not_primary_node');
          }
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
  watch: {
    'amount': {
      handler(v) {
        this.totalAmount = this.amount ? (new Decimal(v)).times(new Decimal(this.fee)).plus(new Decimal(v)) : '0';
      }
    }
  },
  components: {
    MainContainer,
    PasswordInput
  }
};
</script>
<style lang="scss">
  .finance-transfer {
    &>.mint-button {
      display: block;
      width: calc(100% - 64px) ;
      margin-top: 96px;
      height: 104px;
      margin-left: 32px;
      font-size: 36px;
      border-radius: 10px;
    }
  }
</style>

