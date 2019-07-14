<template>
  <div class="proof-img">
    <div class="order-title">{{$t('payment_info.proof_img')}}</div>
    <div class="img-content">
      <div class="img-field" v-for="(item, index) in details.match_order.proof_img" :key="index">
        <img :src="item" alt="" v-gallery:proofImg>
      </div>
    </div>
  </div>
</template>
<script>
  export default {
    props: ['details'],
    data() {
      return {
      };
    }
  }
</script>
<style lang="scss">
  .proof-img {
    background: #fff;
    padding: 32px 0 24px 0;
    margin-top: 18px;
    .order-title {
      font-family: PingFangSC-Regular;
      font-size: 28px;
      color: #222;
      line-height: 1;
      margin-bottom: 33px;
      padding: 0 32px;
    }
    .img-content {
      display: flex;
      align-items: center;
      flex-wrap: wrap;
      padding: 0 16px;
      .img-field {
        display: flex;
        align-items: center;
        width: calc(25% - 32px);
        height: calc(81.42px * 2 - 16px);
        margin: 16px 16px 0 16px;
        img {
          width: 100%;
          height: 100%;
        }
      }
    }
  }
</style>

