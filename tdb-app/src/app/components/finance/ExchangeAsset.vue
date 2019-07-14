<template>
  <main-container :title="$t('common.exchange_wallet')" :hasTabbar="false" containerColor="#f7f7f7">
     <mt-button icon="back" slot="left" @click.native="$router.go(-1)"></mt-button>
    <div class="asset-exchange">
      <div class="asset-total">
        <div class="total">
        <header>
          {{$t('common.current_amount')}}
        </header>
        <div class="amount">
          {{assetData}}
        </div>
        <div class="total-bottom">
            <mt-button @click.native="$router.push('/finance/transfer')">
              {{this.$t('common.transfer')}}
            </mt-button>
            <mt-button @click.native="$router.push('/finance/exchange')">
              {{this.$t('common.huazhuan')}}
            </mt-button>
        </div>
      </div>
      </div>
     <div class='operation'>
        <mt-navbar class="wallet-nav-item">
          <mt-tab-item :id="item" v-for="(item, index) in navItem" :key="index" :class="{'is-selected': isSelect== item}"
            @click.native="changeNav(item)">
            {{getType(item)}}
          </mt-tab-item>
        </mt-navbar>
        <div class="listBox">
          <no-tips v-if="!dataList.length" :text="$t('common.no_record')"></no-tips>
          <div
            v-infinite-scroll="loadMore"
            infinite-scroll-disabled="allLoaded"
            infinite-scroll-distance="10"
            v-else>
            <record-item v-for="(item, index) in dataList" :key="index" :item="item">
            </record-item>
          </div>
        </div>
      </div>
    </div>
  </main-container>
</template>
<script>
import MainContainer from 'app/components/elements/MainContainer';
import RecordItem from 'app/components/finance/elements/RecordItem';
import NoTips from 'app/components/elements/NoTips';
export default {
  data() {
    return {
      assetData: '',
      navItem: [
        0,
        1,
        2,
        4,
        8,
        16,
        32,
        64,
        128,
        256,
        512
      ],
      isSelect: 0,
      details: {},
      dataList: [],
      page: 1,
      allLoaded: false
    }
  },
  computed: {
  },
  methods: {
    changeNav(index) {
      this.isSelect = index;
      this.getList(true);
    },
    getType(v) {
      let typeObj = {
        0: this.$t('common.all'),
        1: this.$t('record.type_1'),
        2: this.$t('record.type_2'),
        4: this.$t('record.type_4'),
        8: this.$t('record.type_8'),
        16: this.$t('record.type_16'),
        32: this.$t('record.type_32'),
        64: this.$t('record.type_64'),
        128: this.$t('record.type_128'),
        256: this.$t('record.type_256'),
        512: this.$t('record.type_512'),
      };
      return typeObj[v]
    },
    getList(isInit) {
      if (isInit) {
        this.dataList = [];
        this.page = 1;
        this.allLoaded = false;
      }
      let params = {
        page: this.page,
        per_page: 10,
        assets_type: 4,
        record_type: this.isSelect
      };
      this.$get('/member/assets/list', {
        params: params
      }).then(r => {
        this.dataList = this.dataList.concat(r.data.objects);
        if (r.data.total_pages > this.page) {
          this.allLoaded = false;
        } else {
          this.allLoaded = true;
        }
      }).catch(err => {});
    },
    loadMore() {
      this.page++;
      this.getList();
    }
  },
  mounted() {
    this.$get('/member/assets/query').then(res => {
      this.assetData = res.data.transaction_balance;
    });
    this.getList(true);
  },
  components: {
    MainContainer,
    RecordItem,
    NoTips
  },

};
</script>
<style lang="scss" rel="stylesheet/scss">
  .asset-exchange {
   .asset-total {
     background: #fff;
     padding-bottom: 41px;
     margin-bottom: 24px;
      .total {
      background-image: url('../../assets/img/wallet_bg_balance2x.png');
      background-size: 100% 100%;
      height: 336px;
      margin: 40px 24px 0;
      padding: 45px 48px 0px 48px;
      header {
        font-family: PingFangSC-Regular;
        font-size: 28px;
        color: #FFF5D6;
        line-height: 1;
      }
      .amount {
        margin-top: 39px;
        font-family: PingFangSC-Medium;
        font-size: 60px;
        color: #F2D479;
        line-height: 1;
      }
      .total-bottom {
        .mint-button {
          background-clip: padding-box;
          background-image: linear-gradient(-90deg, #614911 0%, #AA8835 100%);
          border-radius: 30.5px;
          color: #fff;
          font-size: 28px;
          padding: 0 43px;
          height: 56px;
          line-height: 56px;
          border: 0;
          &:first-child {
            margin-right: 24px;
          }
        }
      }
    }
   }
   .operation {
    height: calc(100% - 336px - 41px - 24px - 40px);
    display: block;
    background: #fff;
    position: relative;
    .mint-navbar {
      height: 106px;
      padding: 0 !important;
      

      .mint-tab-item {
        padding: 0 40px;
        width: auto !important;
        font-family: PingFangSC-Regular;
        font-size: 30px;
        color: #878787;
        letter-spacing: -0.72px;
        text-align: left;

        &.is-selected {
          margin: 0 !important;
        }

        .mint-tab-item-label {
          height: 106px;
          line-height: 106px !important;
        }
      }
    }


    .listBox {
      height: calc(100% - 24px - 120px - 57px);
      overflow: scroll;
      position: absolute;
      width: 100%;
      top: 120px;
      left: 0;
    }
  }
    
  }
</style>
