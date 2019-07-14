<template>
  <div class="common-no-tips">
    <div class="tips-content">
      <div class="img">
        <i class="icon icon-no-tips"></i>
      </div>
      <div class="tips-text">
        {{text}}
      </div>
    </div>
  </div>
</template>
<script>
export default {
  props: ['text'],
  data() {
    return {};
  }
};
</script>
<style lang="scss">
  .common-no-tips {
    height: 100%;
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    .img {
      text-align: center;
      i {
        width: 229px;
        height: 150px;
        background-image: url('../../assets/img/icon_no.png');
        margin-bottom: 40.7px;
      }
    }
    .tips-text {
      text-align: center;
      font-family: PingFangSC-Regular;
      font-size: 30px;
      color: #000;
    }
  }
</style>


