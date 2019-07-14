<template>
  <main-container class="cust-container" :title="$t('account.friend_title')" :hasTabbar="false" containerColor="#fff">
    <mt-button slot="left" icon="back" @click.native="$router.push('/account')"></mt-button>
    <span slot="right" class="filter-btn" @click="handleFilter">{{showFilter ? $t('common.cancel') : $t('common.filter')}}</span>
    <transition name="filter-fade">
      <div v-show="showFilter" class="filter-board">
        <span v-for="n in 10" :key="n">
          <span @click="chooseGeneration(n)" class="generation-btn" :class="{'active': generation == n}">{{$t('account.friend_generation', {n: n})}}</span>
        </span>
      </div>
    </transition>
    <div @click="showFilter = false" v-show="showFilter" class="filter-modal"></div>
    <div class="account-friend">
      <header>
        <div>
          <span>
            {{$t('account.friend_generation_count', {n: generation})}}：{{dataList.length}}
          </span>
          <span>
            {{$t('account.friend_total')}}：{{memberProfile.cal_team_count}}
          </span>
        </div>
      </header>
      <no-tips :text="$t('common.no_record')" v-if="!dataList.length"></no-tips>
      <div v-for="(item, index) in dataList" :key="index" v-show="dataList.length">
        <mt-cell>
          <i class="icon icon-person-blue" slot="icon"></i>
          <div class="phone_time" slot="title">
            <div>{{item.mobile}}</div>
            <div>{{item.created_at | time}}</div>
          </div>
        </mt-cell>
        <div class="line"></div>
      </div>
    </div>
  </main-container>
</template>
<script>
import MainContainer from 'app/components/elements/MainContainer';
import NoTips from 'app/components/elements/NoTips';
import store from 'app/store';
export default {
  data() {
    return {
      dataList: [],
      generation: 1,
      showFilter: false,
      state: store.state
    };
  },
  computed: {
    memberProfile() {
      return this.state.memberProfile;
    }
  },
  mounted() {
    this.getData();
  },
  methods: {
    handleFilter() {
      this.showFilter = !this.showFilter;
    },
    chooseGeneration(n) {
      this.generation = n;
      this.showFilter = false;
      this.getData();
    },
    getData() {
      this.$get('/member/team/sponsor_downline', {
        params: {
          depth: this.generation
        }
      }).then(res => {
        this.dataList = res.data.objects;
      }).catch(err => {});
    }
  },
  components: {
    MainContainer,
    NoTips
  },
  watch: {
  },
};
</script>
<style lang="scss">
  .cust-container {
    >header {
      z-index: 10001;
    }
  }
  .filter-btn {
    font-size: 28px;
    color: #F2D479;
  }
  .filter-board {
    position: absolute;
    width: 100%;
    height: auto !important;
    z-index: 10000;
    display: flex;
    flex-wrap: wrap;
    background: #fff;
    padding-bottom: 26px;
    >span {
      width: 33.3%;
      text-align: center;
      .generation-btn {
        &.active {
          background:linear-gradient(75deg,rgba(176,133,30,1),rgba(242,201,97,1));
          color: #fff;
        }
        background:rgba(241,241,241,1);
        color: #696969;
        display: inline-block;
        width: 210px;
        height: 80px;
        font-size: 30px;
        line-height: 80px;
        border-radius: 8px;
      }
    }
  }
  .filter-modal {
    background: #000;
    opacity: 0.5;
    position: fixed;
    width: 100%;
    z-index: 1;
  }
  .account-friend {
    padding: 90px 0 65px 0;
    &>header {
      position: fixed;
      top: 90px;
      width: 100%;
      padding: 10px 32px;
      left: 0;
      height: 90px;
      font-family: PingFangSC-Regular;
      font-size: 30px;
      background: #F6F7F7;
      z-index: 9999;
      display: flex;
      align-items: center;
      &>div {
        color: #222;
        height: 40px;
        line-height: 40px;
        margin-bottom: 10px;
        width: 100%;
        display: flex;
        align-items: center;
        font-size: 28px;
        justify-content: space-between;
        &:last-child {
          margin-bottom: 0;
        }
      }
    }
    .mint-cell {
      .mint-cell-wrapper {
        padding: 32px !important;
        align-items: start !important;
        .mint-cell-title {
          color: #000;
          align-items: center !important;
        }
        .mint-cell-value {
          color: #545454 !important;
          >span {
            line-height: 44px;
          }
        }
      }
    }
    .line {
      border-bottom: 2px solid #E6E6E6;
      margin-left: 32px;
    }
    
    .icon {
      width: 44px;
      height: 44px;
      &.icon-person-blue {
        background-image: url('../../assets/img/icon_person_blue.png');      
      }
    }
    .phone_time {
      padding-left: 18px;
      >div {
        &:first-child {
          color: #222;
          font-size: 30px;
        }
        &:last-child {
          margin-top: 30px;
          color: #696969;
          font-size: 26px;
        }
      }
    }
  }
  .filter-fade-enter-active, .filter-fade-leave-active {
    transition: all 0.5s;
    transform: translateY(0%);
  }
  .filter-fade-enter, .filter-fade-leave-to /* .fade-leave-active below version 2.1.8 */ {
    transform: translateY(-100%);
  }
</style>

