<template>
  <main-container :title="$t('common.community_wallet')" :hasTabbar="false" containerColor="#f7f7f7">
     <mt-button icon="back" slot="left" @click.native="$router.go(-1)"></mt-button>
    <div class="asset-community">
      <div class="asset-total">
        <div class="total">
        <header>
          {{$t('common.current_amount')}}
        </header>
        <div class="amount">
          {{validData | currency(8)}}
        </div>
        <div class="total-bottom">
          <div class="total-content">
            <p class="total-title">{{$t('common.valid_amount')}}</p>
            <p class="total-count">{{assetData | currency(8)}}</p>
          </div>
          <div class="total-content">
             <p class="total-title">{{$t('common.frozen')}}</p>
            <p class="total-count">{{frozenData | currency(8)}}</p>
          </div>
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
import {Decimal} from 'decimal.js';
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
      allLoaded: false,
      frozenData: '',
      validData: '',
    }
  },
  mounted() {
    this.$get('/member/assets/query').then(res => {
      this.assetData = res.data.community_balance;
      this.frozenData = res.data.community_frozen_balance;
      this.validData = new Decimal(this.assetData).plus(this.frozenData);
    });
    this.getList(true);
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
        assets_type: 2,
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
      }).catch(err => {
      });
    },
    loadMore() {
      this.page++;
      this.getList();
    }
  },
  components: {
    MainContainer,
    RecordItem,
    NoTips
  },
};
</script>
<style lang="scss" rel="stylesheet/scss">
  .asset-community {
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
        color:#FFF5D6;
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
        display: flex;
        margin-top: 35px;
        .total-content {
          width: 50%;
          &:nth-child(2) {
            padding-left: 32px;
            border-left: 1px solid rgba(255,255,255,0.20);
          }
          .total-title {
            font-size: 24px;
            color:#FFF5D6;
            text-align: left;
            line-height: 1;
          }
          .total-count {
            font-family: PingFangSC-Regular;
            font-size: 26px;
            color: #F2D479;
            text-align: left;
            line-height: 1;
            margin-top: 15px;
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
          color: #485EF0;
        }

        .mint-tab-item-label {
          height: 106px;
          line-height: 106px !important;
        }
      }
    }


    .listBox {
      height: calc(100% - 24px - 120px);
      overflow: scroll;
      position: absolute;
      width: 100%;
      top: 120px;
      left: 0;
    }
  }
    
  }
</style>
