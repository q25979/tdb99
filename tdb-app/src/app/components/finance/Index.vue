<template>
  <main-container :hasHeader="false" :noHeader="true">
    <div class="finance">
      <div class="home-icon">
        <div class="user-icon">
          <img :src="memberProfile.avatar || defaultImage" alt="">
        </div>
        <p class="user-uid">UID: {{memberProfile.uid}}</p>
      </div>
      <div class="content-box">
        <div class="total-assets-box">
          <div class="total-assets">
            <div class="assets-count" @click="$router.push('/finance/generalasset')">
              <div class="count-left">
                <p class="count-title">
                  <img src="../../assets/img/icon/home_2x.png" alt="">
                  {{$t('common.total_asset_wallet')}}
                </p>
                <p class="count">{{assetData.total_balance}}</p>
              </div>
              <div class="count-right">
                <img src="../../assets/img/icon/home_icon_142x.png" alt="">
              </div>
            </div>
            <div class="count-bottom">
              <div class="bottom-item">
                <p class="title">{{$t('common.super_vip')}}</p>
                <p class="number">0</p>
              </div>
              <div class="bottom-item" @click="$router.push('/finance/node_profit')">
                 <p class="title">{{$t('common.node_profit')}}</p>
                <p class="number">{{memberProfile.node_profit}}</p>
              </div>
            </div>
          </div>
          <swiper :options='swiperOption' class="notice-swiper" ref="myswiper" v-if="noticeList.length > 0">
            <swiper-slide v-for="(item,index) in noticeList" :key="index">
              <div class="notice" @click="$router.push('/account/news_detail?id='+item.id)"><img src="../../assets/img/icon/notice.png" alt="">
                <span>公告：{{handleDetails(item.details)}}</span>
              </div>
            </swiper-slide>
          </swiper>
            
            <div class="wallet-box">
              <div class="wallet-item" @click="$router.push('/finance/communitywallet')">
                <p class="count-title">
                  <img src="../../assets/img/icon/home_2x.png" alt="">
                  {{$t('common.community_wallet')}}
                </p>
                <p class="count">{{assetData.total_community | currency(8)}}</p>
              </div>
              <div class="wallet-item" @click="$router.push('/finance/exchangeasset')">
                <p class="count-title">
                  <img src="../../assets/img/icon/home_2x.png" alt="">
                  {{$t('common.exchange_wallet')}}
                </p>
                <p class="count">{{assetData.transaction_balance}}</p>
              </div>
            </div>
        </div>
          <div class="devlop-line">
            <span class="line"></span> <span>{{$t('common.developing')}}</span> <span class="line"></span>
          </div>
          <div class="development">
            <div class="develop-item" v-for="(item,index) in developments" :key="index">
              <img :src="item.imgPath" alt="">
              <div class="develop-title">
                {{item.devTitle}}
              </div>
            </div>
          </div>
      </div>

      <div>

      </div>
    </div>
  </main-container>
</template>
<script>
  import store from 'app/store';
  import MainContainer from 'app/components/elements/MainContainer';
  import i18n from 'app/i18n';
  import {Decimal} from 'decimal.js';
  import 'swiper/dist/css/swiper.css';
  import { swiper, swiperSlide } from 'vue-awesome-swiper';

  const localeList = i18n.localeList;
  export default {
    data() {
      return {
        defaultImage: require('../../assets/img/default_avatar.png'),
        state: store.state,
        assetData: {},
        swiperOption: {
          loop : true,
          autoplay: {
            delay:3000,
            disableOnInteraction: false,
          },
          observer:true,
          direction: 'vertical',
          observeParents:false 
         },
        noticeList:{},
        developments: [
          {
            imgPath: require('../../assets/img/icon/home_icon_1.png'),
            devTitle: this.$t('index.app_1')
          },{
            imgPath: require('../../assets/img/icon/home_icon_2.png'),
            devTitle: this.$t('index.app_2')
          },{
            imgPath: require('../../assets/img/icon/home_icon_3.png'),
            devTitle: this.$t('index.app_3')
          },{
            imgPath: require('../../assets/img/icon/home_icon_4.png'),
            devTitle: this.$t('index.app_4')
          },{
            imgPath: require('../../assets/img/icon/home_icon_5.png'),
            devTitle: this.$t('index.app_5')
          },{
            imgPath: require('../../assets/img/icon/home_icon_6.png'),
            devTitle: this.$t('index.app_6')
          },{
            imgPath: require('../../assets/img/icon/home_icon_7.png'),
            devTitle: this.$t('index.app_7')
          },{
            imgPath: require('../../assets/img/icon/home_icon_8.png'),
            devTitle: this.$t('index.app_8')
          },{
            imgPath: require('../../assets/img/icon/home_icon_9.png'),
            devTitle: this.$t('index.app_9')
          },{
            imgPath: require('../../assets/img/icon/home_icon_10.png'),
            devTitle: this.$t('index.app_10')
          },{
            imgPath: require('../../assets/img/icon/home_icon_11.png'),
            devTitle: this.$t('index.app_11')
          },{
            imgPath: require('../../assets/img/icon/home_icon_12.png'),
            devTitle: this.$t('index.app_12')
          }
        ]
      };
    },
    computed: {
      memberProfile() {
        return this.state.memberProfile;
      }
    },
    mounted() {
      this.$get('/member/assets/query').then(res => {
        this.assetData = res.data;
        this.assetData.total_community = new Decimal(this.assetData.community_balance).plus(this.assetData.community_frozen_balance);
      });
      this.getList();
    },

    methods: {
      handleDetails(str) {
        if(str) {
          let temp = str.replace(/<[^>]+>/g, "");
          return temp.replace(/&nbsp;/ig, "");
        } else {
          return '';
        }
      },
      getList() {
      this.$get('/member/news', {
        params: {
          per_page: 5,
          page: 1
        }
      }).then(r => {
        this.noticeList = r.data.objects
      }).catch(err => {
      });
    },
    },
    components: {
      MainContainer,
      swiper,
      swiperSlide
    },
  };

</script>
<style lang="scss" rel="stylesheet/scss">
  .finance {
    .home-icon {
      width: 100%;
      height: 800px;
      background: url('../../assets/img/icon/Logo.gif');
      background-size: 100% 100%;
      font-family: PingFangSC-Medium;
      text-align: center;
      padding-top: 284px;
     
      .user-icon {
        width: 130px;
        height: 130px;
        border: 8px solid rgba(255,255,255,0.30);
        border-radius: 50%;
        overflow: hidden;
        margin: 0 auto;
        display: flex;
        margin-bottom: 14px;
        img {
          width: 100%;
          height: 100%;
          border-radius: 50%;
        }
      }
      .user-nick {
        font-size: 34px;
        color: #fff;
        margin-bottom: 6px;
      }
      .user-uid {
        font-size: 26px;
        color: #DFC370;
      }
    }

    .content-box {
       padding: 0 32px;
      .total-assets-box {
        width: 100%;
        margin-top: -145px;
        border-radius: 10px;
        .total-assets {
          width: 100%;
          height: 401px;
          padding: 40px 24px 0px;
          background:rgba(255,255,255,1);
          box-shadow:0px 0px 20px 0px rgba(160, 118, 148, 0.35);
          border-radius: 10px;
          margin-bottom: 45px;
          .assets-count {
            display: flex;
            border-bottom: 1px solid #E6E6E6 ;
            padding-bottom: 32px;
            .count-left {
              flex: 1;

              .count-title {
                font-family: PingFangSC-Regular;
                font-size: 30px;
                color: #878787;
                margin-bottom: 16px;
                margin-top: 8px;

                img {
                  width: 38px;
                  height: 38px;
                  margin-right: 10px;
                }
              }

              .count {
                font-family: PingFangSC-Regular;
                font-size: 40px;
                color: #212121;
                letter-spacing: 0;
                line-height: 100px;
              }
            }

            .count-right {
              width: 188px;
              height: 176px;
              margin-right: 24px;

              img {
                width: 100%;
                height: 100%;
              }
            }
             
          }
          .count-bottom {
               display: flex;
              
               .bottom-item {
                 padding: 24px 0 24px 52px;
                 width: 50%;
                 height: 100%;
                 &:first-child {
                   border-right: 1px solid #E6E6E6;
                 }
                 .title {
                    font-family: PingFangSC-Regular;
                    font-size: 28px;
                    color: #878787;
                    line-height: 40px;
                    margin-bottom: 8px;
                 }
                 .number {
                    font-family: PingFangSC-Regular;
                    font-size: 28px;
                    color: #545454;
                    line-height: 56px;
                 }
               }
         }
        }
        .notice-swiper {
          height: 40px;
          swiperSlide {
             height: 100%;
         }
           .notice {
              font-size: 28px;
              line-height: 40px;
              display: flex;
              span {
                word-break:keep-all;           /* 不换行 */
                white-space:nowrap;          /* 不换行 */
                overflow:hidden;               /* 内容超出宽度时隐藏超出部分的内容 */
                text-overflow:ellipsis;
             }
              img {
                width: 40px;
                height: 40px;
                margin-right: 20px;
            }
          }
        }
       
        .wallet-box {
          display: flex;
          width: 100%;
          height: 181px;
          justify-content: space-between;
          margin-top: 40px;
          .wallet-item {
            width: calc(50% - 16px);
            height: 100%;
            background: #fff;
            padding: 32px 0 0 24px;
            box-shadow:0px 0px 20px 0px rgba(160, 118, 148, 0.35);
            border-radius: 10px;
              .count-title {
                font-family: PingFangSC-Regular;
                font-size: 30px;
                color: #878787;
                margin-bottom: 16px;
                margin-top: 8px;

                img {
                  width: 36px;
                  height: 36px;
                  margin-right: 10px;
                }
              }

              .count {
                font-family: PingFangSC-Regular;
                font-size: 30px;
                line-height: 67px;
                color: #212121;
              }
          }
        }
      }
      .devlop-line {
        font-family: PingFangSC-Regular;
        font-size: 32px;
        line-height: 45px;
        color: #878787;
        display: flex;
        align-items: center;
        margin-top: 53px;
        margin-bottom: 33px;
        span {
          width: calc(100% - 464px - 98px);
          display: inline-block;
          overflow: hidden;
          text-overflow:ellipsis;
          white-space: nowrap;
          text-align: center;
          &.line {
            width: 232px;
            height: 2px;
            background-color: #ccc;
            &:first-child {
              margin-right: 49px;
            }

            &:last-child {
              margin-left: 49px;
            }

          }
        }
        
  
      }
      .development {
        width: 100%;
        display: flex;
        flex-wrap: wrap;
        margin-bottom: 10px;
        .develop-item {
          width: 220px;
          height: 186px;
          background: #fff;
          margin-right: 12px;
          margin-bottom: 13px;
          box-shadow:0px 0px 20px 0px rgba(160, 118, 148, 0.35);
          border-radius:10px;
          &:nth-child(3n) {
            margin-right: 0;
          }
          img {
            display: block;
            margin: 34px auto 19px;
            width: 74px;
            height: 74px;
          }
          .develop-title {
            font-size:30px;
            font-family:PingFang-SC-Regular;
            color:rgba(34,34,34,1);
            text-align: center;
            overflow: hidden;
            text-overflow:ellipsis;
            white-space: nowrap;
          }
        } 
      }
    }

    .investTip {
      margin-bottom: 32px;
    }

    .profit {
      margin-top: 32px;
      margin-bottom: 32px;
    }

  }

</style>
