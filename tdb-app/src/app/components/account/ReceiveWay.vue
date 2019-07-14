<template>
  <main-container :title="$t('account.receive_way_title')" class='addressBox' containerColor="#fff" :hasTabbar="false">
    <mt-button icon="back" slot="left" @click.native="$router.go(-1)"></mt-button>
    <div class="pay-way-list">
      <div class="cell-item" v-for="(item,index) in payWayList" :key="index" @click="$router.push(`/account/receiveway/${item.formpath}`)">
        <div class="cell-left">
          <img slot="icon" :src="item.icon" >{{item.type}}
        </div>
        <div class="cell-right">
          <img src="../../assets/img/back_icon_12x.png" alt="">
        </div>
      </div>
    </div>
  </main-container>
</template>

<script>
import MainContainer from 'app/components/elements/MainContainer';
export default {
  data() {
    return {
      payWayList : []
    }
  },
  mounted() {
    this.$get('/member/payment/list', {
      params: {
        per_page: 4,
        page: 1
      }
    }).then(res => {
      let alipay = {
        icon: require('../../assets/img/payment/alipay.png'),
        type: this.$t('common.alipay'),
        formpath:'addalipay',
      };
      let bank = { 
        icon: require('../../assets/img/payment/bank.png'),
        type: this.$t('common.bank_card'),
        formpath:'addbank'
      };
      let wechat = { 
        icon: require('../../assets/img/payment/wechat.png'),
        type: this.$t('common.wechat'),
        formpath:'addweixin'
      };
      let usdt = { 
        icon: require('../../assets/img/payment/usdt.png'),
        type: 'USDT',
        formpath:'addusdt'
      };
      let temp = [];
      for(let item of res.data.objects) {
        temp.push(item.type);
      }
      if(temp.indexOf(0) == -1) {
        this.payWayList.push(bank);
      }
      if(temp.indexOf(1) == -1) {
        this.payWayList.push(wechat);
      }
      if(temp.indexOf(2) == -1) {
        this.payWayList.push(alipay);
      }
      if(temp.indexOf(3) == -1) {
        this.payWayList.push(usdt);
      }
    }).catch(err=> {
    });
  },
  components:{
    MainContainer
  }
}
</script>

<style lang="scss" >
  .pay-way-list {
    width: 100%;
    padding: 32px;
    .cell-item {
      width: 100%;
      height: 100px;
      background: #f1f1f1;
      border-radius: 8px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 0 32px;
      margin-bottom: 32px;
      .cell-left {
        display: flex;
         font-size: 32px;
         line-height: 45px;
         img {
           width: 48px;
           height: 48px;
           margin-right: 24px;
         }
      }
      .cell-right {
        display: flex;
        img {
        width: 44px;
        height: 44px;
        }
      }

    }
  }
</style>

