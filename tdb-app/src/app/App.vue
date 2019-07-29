<template>
  <router-view></router-view>
</template>
<script>
export default {
  data() {
    return {
      extraPath: ['Home', 'Finance']
    };
  },
  mounted() {
    // if(this.extraPath.indexOf(this.$route.name) > -1) {
    //   StatusBar.backgroundColorByHexString("#1E1C14");
    // } else {
    //   StatusBar.backgroundColorByHexString("#1E1C14");
    // }
  },
  watch: {
    $route(val) {
      // if(this.extraPath.indexOf(val.name) > -1) {
      //   StatusBar.backgroundColorByHexString("#1E1C14");
      // } else {
      //   StatusBar.backgroundColorByHexString("#1E1C14");
      // }
    }
  }
};
</script>
<style lang="scss">
  @import './style/common';
  #app,
  html,
  body {
    width: 100%;
    height: 100%;
    .app {
      i {
        font-size: px2rem(24px);
        &.active {
          color: #26a2ff;
        }
      }
    }
  }
</style>
