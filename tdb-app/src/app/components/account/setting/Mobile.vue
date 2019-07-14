<template>
  <main-container :title="$t('mobile.set_phone_number')" :hasTabbar="false">
    <mt-button icon="back" slot="left" @click.native="$router.push('/account/setting')"></mt-button>
    <mt-button slot="right" :disabled="cannotSave" @click.native="handleSave">
      {{$t('common.save')}}
    </mt-button>
    <div class="setting-mobile">
      <div class="fields-content">
        <mobile-input v-model="mobile" :label="$t('mobile.deal_phone')" :placeholder="$t('mobile.input_deal_phone')"></mobile-input>
      </div>
    </div>
  </main-container>
</template>
<script>
import store from 'app/store';
import MainContainer from 'app/components/elements/MainContainer';
import MobileInput from 'app/components/elements/MobileInput';
export default {
  data() {
    return {
      mobile: '',
      state: store.state
    };
  },
  computed: {
    cannotSave() {
      return !this.mobile;
    },
    countryCode: {
      get() {
        return this.state.countryCode;
      },
      set(val) {
        this.state.countryCode = val;
      }
    },
  },
  mounted() {
    store.refreshMemberProfile(v => {
      this.mobile = this.state.memberProfile.order_mobile;
      if(this.mobile == null) {
      } else {
        let arr = this.mobile.split(' ');
        this.countryCode = arr[0];
        this.mobile = arr[1];
      }
    });
  },
  methods: {
    handleSave() {
      window.scroll(0, 0);
      this.$put('/member/user/current_user', {
        order_mobile: `${this.countryCode} ${this.mobile}`
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
    MainContainer,
    MobileInput
  }
};
</script>
<style lang="scss">
  .setting-mobile {
    .fields-content {
      padding-bottom: 32px;
      background: #fff;
    }
  }
</style>


