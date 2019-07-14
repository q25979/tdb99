<template>
  <main-container :title="$t('account.receive_title')" class="addressBox" :containerColor="dataList.length ? '#f7f7f7' : '#fff'" :hasTabbar="false">
    <mt-button icon="back" slot="left" @click.native="$router.push('/account')"></mt-button>
    <mt-button slot="right" @click.native="handleRouter">
      <img class="more" src="../../assets/img/address_icon_add2x.png" height="22" width="22" slot="icon">
    </mt-button>
    <div class='addresss'>
      <div class="content-box">
        <div class="noAddress" v-if="!dataList.length">
          <img src="../../assets/img/generic_icon_no2x.png" alt>
          <p class="gathering">{{$t('receive.no_tips')}}</p>
          <mt-button @click.native="$router.push('/account/receiveway')" class="add-btn" type="primary">
            {{$t('common.add')}}
          </mt-button>
        </div>
        <mt-loadmore
        :bottom-method="loadBottom"
        :bottom-all-loaded="allLoaded"
        ref="loadmore"
        :auto-fill="false"
        :bottomLoadingText="$t('common.loading')"
        :bottomDropText="$t('common.release_update')">
          <div v-if='dataList.length'>
            <div class="reice-item" v-for='(item, index) in dataList' :key="index">
              <div class="userId">
                <i :class="`icon ${getType(item.type).value}`"></i> {{getType(item.type).label}}
              </div>
              <div class="content">
                <div>
                  <p class="user-name">{{item.type == 3 ? item.remark : item.name}}</p>
                  <p class="user-address">
                    {{getAddress(item)}}
                  </p>
                </div>
                <div>
                  <img v-gallery :src="getImage(item)" alt="" v-if="getImage(item)">
                </div>
              </div>
            </div>
          </div>
        </mt-loadmore>
      </div>
    </div>
  </main-container>
</template>

<script>
  import MainContainer from "app/components/elements/MainContainer.vue";
  import store from 'app/store';
  export default {
    data() {
      return {
        navItem: [{
          label: this.$t('common.all'),
          value: ''
        }],
        isSelect: '',
        dataList: [],
        page: 1,
        allLoaded: false,
        fromPath:''
      };
    },
    mounted() {
      this.getAddressList();
      this.$get('/member/assets/query').then(r => {
        let currency_code = []
        r.data.objects.forEach(element => {
          this.navItem.push({
            label: element.currency_code,
            value: element.currency_code
          });
        });
      }).catch(err => {});
    },
    methods: {
      handleRouter() {
        if(this.dataList.length >= 4) {
          this.messagebox({
            message: this.$t('receive.tips1'),
            confirmButtonText: this.$t('common.sure')
          });
        } else {
          this.$router.push('/account/receiveway');
        }
      },
      getType(v) {
        let typeObj = {
          0: {
            value: 'bank',
            label: this.$t('common.bank_card')
          },
          1: {
            value: 'wechat',
            label: this.$t('common.wechat')
          },
          2: {
            value: 'alipay',
            label: this.$t('common.alipay')
          },
          3: {
            value: 'usdt',
            label: 'USDT'
          }
        };
        return typeObj[v]
      },
      getAddress(item) {
        if(item.type == 0) {
          return item.card_number;
        }
        if(item.type == 1) {
          return item.wechat;
        }
        if(item.type == 2) {
          return item.alipay;
        }
        if(item.type == 3) {
          return item.address;
        } 
      },
      getImage(item) {
        if(item.type == 1) {
          return item.wechat_image;
        } else if(item.type == 2) {
          return item.alipay_image;
        } else {
          return '';
        } 
      },
      getAddressList() {
        this.$get('/member/payment/list',{
          params: {
            per_page: 4,
            page: this.page,
          }
        }).then(resp => {
          if (resp.data.objects.length === 0) {
          } else {
            if(resp.data.total_pages > this.page ){
              this.allLoaded = false;
            }else {
              this.allLoaded = true;
            }
            this.dataList = this.dataList.concat(resp.data.objects);
          }
        })
        .catch(err=> {
        });
      },
      loadBottom() {
        this.$refs.loadmore.onBottomLoaded();
        this.page++;
        this.getAddressList();
      }
    },
    watch:{
  
  },
   components: {
      MainContainer
    }
}

</script>


<style lang="scss" rel="stylesheet/scss">
  .addressBox {
    .more {
      width: 40px;
      height: 40px;
    }
    .addresss {
      position: relative;
      height: 100%;
      .mint-navbar {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        z-index: 100;
        .mint-tab-item {
          padding: 0;
          height: 87px;
          line-height: 87px;
          .mint-tab-item-label {
            height: 87px !important;
            line-height: 87px !important;
          }
          &.is-selected {
            color: #21E3E7;
            border-bottom: 3px solid #21E3E7;
            .mint-tab-item-label {
              color: #21E3E7 !important;
            }
          }
        }
      }
      .content-box {
        padding: 24px  0;
        height: 100%;
        overflow: auto;
        .noAddress {
          text-align: center;
          margin-top: 160px;

          img {
            width: 165px;
            height: 160px;
          }

          p.gathering {
            font-size: 30px; 
            color: #545454;
            letter-spacing: 0;
            margin-top: 32px;
            margin-bottom: 88px;
            line-height: 42px;
          }

          .mint-button.add-btn {
            border-radius: 48px;
            width: 320px;
            height: 104px;
            color: #fff;
            font-size: 36px;
          }
        }

        .reice-item {
          background: #fff;
          width: 100%;
          padding: 24px 32px;
          border-radius: 8px;
          margin-bottom: 24px;

          .userId {
            font-size: 30px;
            height: 42px;
            margin-bottom: 31px;
            line-height: 1;
            display: flex;
            align-items: center;
            i {
              width: 44px;
              height: 44px;
              margin-right: 24px;
              &.usdt {
                background-image: url('../../assets/img/payment/usdt.png');
              }
              &.alipay {
                background-image: url('../../assets/img/payment/alipay.png');
              }
              &.wechat {
                background-image: url('../../assets/img/payment/wechat.png');
              }
              &.bank {
                background-image: url('../../assets/img/payment/bank.png');
              }
            }
          }

          .content {
            display: flex;
            align-items: center;
            &>div {
              &:first-child {
                width: 60%;
              }
              &:last-child {
                width: 40%;
                display: flex;
                align-items: center;
                justify-content: flex-end;
                img {
                  width: 100px;
                  height: 100px;
                }
              }
            }
            .user-name {
              color: #818181;
              font-size: 24px;
              line-height: 1;
              margin-bottom: 42px;
            }

            .user-address {
              font-size: 30px;
              color: #222;
              line-height: 1;
            }
          }
        }
      }
    }

  }

</style>
