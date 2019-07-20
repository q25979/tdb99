<template>
  <div class="app"> 
    <transition :name="transitionName"> 
    <router-view class="child-view"></router-view> 
    </transition>
  </div>
</template>
<script>
  export default {
    data() {
      return {
        transitionName: 'slide-left',
      };
    },
    watch: {
      '$route': {
        handler(to, from) {
          if(to.name == 'Register') {
            this.transitionName = 'slide-right';
          } else {
            this.transitionName = 'slide-left';
          }
        }
      }
    }
  };
</script>
<style lang="scss">
  @import "./style/common";
  @import "./style/mixin";
  #app,.app{
    width: 100%;
    min-height: 100%;
  }
  .child-view { 
    position: absolute;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    transition: all .5s cubic-bezier(.55,0,.1,1);
  }
  .slide-left-enter, .slide-right-leave-active {
    opacity: .5;
    -webkit-transform: translate(100%, 0);
    transform: translate(100%, 0);
  }
  .slide-left-leave-active, .slide-right-enter {
    opacity: .5;
    -webkit-transform: translate(-100%, 0);
    transform: translate(-100%, 0);
  } 
</style>
