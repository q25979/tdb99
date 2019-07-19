<template>
  <main-container :hasHeader="false" :noHeader="true">
    <div class="finance">
      <div class="home-icon">
        <div class="user-icon">
          <img :src="memberProfile.avatar || defaultImage" alt="">
        </div>
        <p class="user-uid">
          <span>UID: {{memberProfile.uid}}</span>
        </p>
      </div>
      <div class="content-box">
        <div class="total-assets-box">
          <div class="total-assets">
            <div class="assets-count" @click="$router.push('/finance/generalasset')">
              <div class="count-left">
                <p class="count-title">
                  {{$t('common.total_asset_wallet')}}
                </p>
                <p class="count">{{parseFloat(assetData.total_balance).toFixed(2)}}</p>
              </div>
              <div class="count-right">
                <img src="../../assets/img/icon/home_icon_142x.png" alt="">
              </div>
            </div>
            <div class="count-bottom">
              <div class="bottom-item">
                <p class="number">0.00</p>
                <p class="title"><span class="icon vip"></span>{{$t('common.super_vip')}}</p>
              </div>
              <div class="bottom-item" @click="$router.push('/finance/node_profit')">
                <p class="number">{{parseFloat(memberProfile.node_profit).toFixed(2)}}</p>
                <p class="title"><span class="icon icon-profit"></span>{{$t('common.node_profit')}}</p>
              </div>
            </div>
          </div>

          <swiper :options='swiperOption' class="notice-swiper" ref="myswiper" v-if="noticeList.length > 0">
            <swiper-slide v-for="(item,index) in noticeList" :key="index">
              <div class="notice" @click="$router.push('/account/news_detail?id='+item.id)"><img src="../../assets/img/icon/gonggao.png" alt="">
                <span class="notice-title">公告</span>
                <span>{{handleDetails(item.details)}}</span>
              </div>
            </swiper-slide>
          </swiper>
          <div class="wallet-box">
            <div class="wallet-item" @click="$router.push('/finance/communitywallet')">
              <p class="count-title">
                {{$t('common.community_wallet')}}
              </p>
              <p class="count">{{assetData.total_community | currency(2)}}</p>
            </div>
            <div class="wallet-item" @click="$router.push('/finance/exchangeasset')">
              <p class="count-title">
                {{$t('common.exchange_wallet')}}
              </p>
              <p class="count">{{parseFloat(assetData.transaction_balance).toFixed(2)}}</p>
            </div>
            <div class="wallet-item" @click="$router.push('/finance/exchangeasset')">
              <p class="count-title">
                {{$t('common.consumption_wallet')}}
              </p>
              <p class="count">{{parseFloat(assetData.transaction_balance).toFixed(2)}}</p>
            </div>
          </div>
        </div>

        <div class="devlop-box">
          <div class="devlop-ing">
            <span class="devlop-icon devlop-left"></span>
            <span class="devlop-text">{{$t('common.developing')}}</span>
            <span class="devlop-icon devlop-right"></span>
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
      height: 580px;
      background: url('../../assets/img/icon/index_bg.png') no-repeat;
      background-size: contain;
      font-family: PingFangSC-Medium;
      text-align: center;
      padding-top: 120px;
     
      .user-icon {
        width: 160px;
        height: 160px;
        border: 5px solid white;
        border-radius: 50%;
        overflow: hidden;
        margin: 0 auto;
        display: flex;
        margin-bottom: 18px;
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
        font-size: 22px;
        color: #555555;
        text-align: center;
        &>span {
          display: inline-block;
          background: #E9E9E9;
          height: 45px;
          line-height: 45px;
          border-radius: 45px;
          padding: 0 30px;
        }
      }
    }

    .content-box {
       padding: 0 32px;
      .total-assets-box {
        width: 100%;
        margin-top: -145px;
        border-radius: 20px;
        .total-assets {
          width: 100%;
          height: 310px;
          padding: 30px 24px 0px;
          background:white;
          box-shadow:0px 0px 20px 0px rgba(160, 118, 148, 0.35);
          border-radius: 20px;
          margin-bottom: 20px;
          .assets-count {
            display: flex;
            .count-left {
              flex: 1;

              .count-title {
                font-family: PingFangSC-Regular;
                font-size: 25px;
                color: #66707E;
                margin-bottom: 5px;
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
                color: #0D0D0D;
                letter-spacing: 0;
                line-height: 70px;
                font-weight: bold;
              }
            }

            .count-right {
              width: 230px;
              margin-right: 0;
              position: relative;
              top: -24px;
              left: 48px;

              img {
                width: 100%;
                height: 100%;
              }
            }
             
          }
          .count-bottom {
               display: flex;
               padding: 20px 0;
               background: #F0F2F4;
               position: relative;
               top: -30px;
               border-radius: 20px;
              
               .bottom-item {
                 width: 50%;
                 height: 100%;
                 text-align: center;
                 &:first-child {
                   border-right: 1px solid #DFE0E4;
                 }
                 .title {
                    font-family: PingFangSC-Regular;
                    font-size: 18px;
                    color: #00002C;
                    .icon {
                      height: 24px;
                      width: 24px;
                      background: url("../../assets/img/icon/VIP.png") no-repeat;
                      background-size: contain;
                      display: inline-block;
                      margin-right: 8px;
                      position: relative;
                      top: 1px;
                    }
                    .icon-profit {
                      background-image: url("../../assets/img/icon/shouyi.png");
                    }
                 }
                 .number {
                    font-family: PingFangSC-Regular;
                    font-size: 34px;
                    font-weight: bold;
                    color: #5B636D;
                 }
               }
         }
        }
        .notice-swiper {
          height: 80px;
          border-radius: 80px;
          background: white;
          box-shadow:0px 0px 20px 0px rgba(160, 118, 148, 0.35);
          swiperSlide {
             height: 100%;
         }
           .notice {
              font-size: 28px;
              padding: 20px;
              line-height: 40px;
              overflow: hidden;
              display: flex;
              span {
                word-break:keep-all;           /* 不换行 */
                white-space:nowrap;          /* 不换行 */
                overflow:hidden;               /* 内容超出宽度时隐藏超出部分的内容 */
                text-overflow:ellipsis;
                color: #A7ABB8;
             }
              img {
                width: 40px;
                height: 40px;
                margin-right: 10px;
            }
            .notice-title {
              color: #D4A55D;
              font-size: 35px;
              display: inline-block;
              width: 120px;
              padding-right: 10px;
              font-weight: bold;
              font-style: italic;
              border-right: 1px solid #A7ABB8;
              margin-right: 15px;
            }
          }
        }
       
        .wallet-box {
          display: flex;
          width: 100%;
          justify-content: space-between;
          margin-top: 40px;
          .wallet-item {
            width: calc(33% - 16px);
            height: 100%;
            box-shadow:0px 0px 20px 0px rgba(160, 118, 148, 0.35);
            border-radius: 20px;
            padding: 20px;
            color: white;
            background: url("../../assets/img/icon/money_bg1.png") no-repeat center center;
            .count-title {
              font-family: PingFangSC-Regular;
              font-size: 18px;
              color: #FEFFFF;
            }

            .count {
              font-family: PingFangSC-Regular;
              font-size: 32px;
              font-weight: bold;
              line-height: 60px;
              color: #FEFFFF;
            }
            &:nth-child(2) {
              background-image: url("../../assets/img/icon/money_bg2.png");
            }
            &:nth-child(3) {
              background-image: url("../../assets/img/icon/money_bg3.png");
            }
          }
        }
      }
      .devlop-box {
        font-family: PingFangSC-Regular;
        font-size: 32px;
        line-height: 45px;
        color: #878787;
        align-items: center;
        margin-top: 40px;
        margin-bottom: 33px;
        background: white;
        border-radius: 50px;
        padding: 30px;
        box-shadow:0px 0px 20px 0px rgba(160, 118, 148, 0.35);
        .devlop-ing {
          text-align: center;
          width: 100%;
          font-weight: bold;
          .devlop-icon {
            display: inline-block;
            background: url("../../assets/img/icon/devlop_left.png") no-repeat;
            width: 20px;
            height: 30px;
            background-size: contain;
          }
          .devlop-left {
            display: inline-block;
          }
          .devlop-right {
            background-image: url("../../assets/img/icon/devlop_right.png");
          }
          .devlop-text {
            position: relative;
            top: -3px;
          }
        }
        .development {
          clear: both;
          content: " ";
          display: block;
          overflow: hidden;
          text-align: center;
          .develop-item {
            float: left;
            border-radius: 10px;
            font-size: 22px;
            width: calc(34.3999% - 20px);
            height: 200px;
            line-height: 105px;
            background: #FFF7ED;
            img {
              width: 70px;
              position: relative;
              top: 25px;
            }
            &:nth-child(2),&:nth-child(5),&:nth-child(8),&:nth-child(11) {
              margin: 20px 20px 0;
            }
            &:nth-child(2),&:nth-child(5),&:nth-child(6) {
              img {
                width: 80px;
              }
            }
            &:nth-child(7) {
              img {
                width: 90px;
              }
            }
            &:nth-child(3), &:nth-child(11) {
              img {
                width: 60px;
              }
            }
            & {
              margin-top: 20px;
            }
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
