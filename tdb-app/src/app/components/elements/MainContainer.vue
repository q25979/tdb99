<template>
  <div class="main-container">
    <mt-header :title="title" v-if="hasHeader">
      <slot name="left" slot="left"></slot>
      <slot name="right" slot="right"></slot>
    </mt-header>
    <slot name="header"></slot>
    <div :class="['container', {'no-tabbar': !hasTabbar},{'no-header': noHeader}]" :style="{backgroundColor: containerColor}">
      <slot></slot>
    </div>
    <mt-tabbar v-model="selected"  v-if="hasTabbar">
      <mt-tab-item
        v-for="(item, index) in tabbarArr"
        :key="index"
        :id="item.id"
        @click.native="$router.push(item.link)">
        <img slot="icon" :src="selected == item.id ? item.icon_selected : item.icon">
        {{item.label}}
      </mt-tab-item>
    </mt-tabbar>
  </div>
</template>
<script>
export default {
  props: {
    title: String,
    hasHeader: {
      type: Boolean,
      default: true,
    },
    hasTabbar: {
      type: Boolean,
      default: true,
    },
    containerColor: {
      type: String,
      default: '#EDEFF3',
    },
    noHeader: {
      type:Boolean,
      default: false
    }
  },
  data() {
    return {
      selected: 'finance',
      tabbarArr: [{
        icon: require('../../assets/img/icon/global_icon_assets2x.png'),
        label: this.$t('common.home'),
        icon_selected: require('../../assets/img/icon/global_icon_assets_select2x.png'),
        id: 'finance',
        link: '/'
      }, {
        icon: require('../../assets/img/icon/global_icon_exchange2x.png'),
        label: this.$t('common.exchange'),
        icon_selected: require('../../assets/img/icon/global_icon_exchange_select2x.png'),
        id: 'exchange',
        link: '/exchange'
      },  {
        icon: require('../../assets/img/icon/global_icon_quotes2x.png'),
        label: this.$t('common.quote'),
        icon_selected: require('../../assets/img/icon/global_icon_quotes_select2x.png'),
        id: 'quotes',
        link: '/quotes/list'
      }, {
        icon: require('../../assets/img/icon/global_icon_me2x.png'),
        label: this.$t('account.title'),
        icon_selected: require('../../assets/img/icon/global_icon_me_select2x.png'),
        id: 'account',
        link: '/account'
      }]
    };
  },
  mounted() {
    let tab = this.$route.meta.tab;
    if(!tab) tab = 'finance';
    this.selected = tab;
  },
  watch: {
  },
  components: {
  },
};
</script>
<style lang="scss">
  .main-container {
    height: 100%;
    position: relative;
    .mint-header {
      height: 90px;
      padding: 0 32px;
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      background: linear-gradient(75deg,rgba(19,25,43,1),rgba(43,39,28,1),rgba(13,14,14,1));
      .mint-header-button.is-left {
        .mintui {
          color:rgba(242,212,121,1);
        }
        .mint-button-text {
          font-family: PingFangSC-Regular;
          font-size: 32px;
          color:rgba(242,212,121,1);
        }
        .mint-button {
          display: flex;
          align-items: center;
        }
      }
      .mint-header-title {
        font-family: PingFangSC-Medium;
        font-size: 36px;
        color:rgba(242,212,121,1);
        font-weight: 500;
        height: 90px;
        line-height: 90px;
      }
      .mint-header-button.is-right {
        .mint-button {
          .mint-button-text {
            font-family: PingFangSC-Regular;
            font-size: 30px;
            color: rgba(242,212,121,1);
          }
          &.is-disabled {
            .mint-button-text {
              color: #ccc;
            }
          }
        }
      }
    }
    .container {
      padding-top: 88px;
      height: 100%;
      padding-bottom: 100px;
      background-color: #fff;
      &.no-header {
        padding-top: 0;
      }
      &.no-tabbar {
        padding-bottom: 0;
      }
      &>div {
        height: 100%;
        overflow: auto;
      }
    }
    .mint-tabbar {
      height: 100px;
      position: absolute;
      bottom: 0;
      left: 0;
      background:rgba(255,255,255,1);
      box-shadow:3px -3px 29px 0px rgba(191,191,214,0.3);
      .mint-tab-item {
        padding: 0;
        .mint-tab-item-icon {
          width: 36px;
          height: 40px;
          margin-top: 14px;
        }
        .mint-tab-item-label {
          font-size: 22px;
          color: #BABABA ;
        }
        &.is-selected {
          background: #fff;
          .mint-tab-item-label {
            color: #CD941B;
          }
        }
      }
    }
  }
</style>


