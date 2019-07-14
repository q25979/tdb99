<template>
  <main-container :title="$t('common.exchange')" containerColor="#fff" class="exchange-maket">
    <mt-button slot="left" @click.native="handleFilter">
      <img src="../../assets/img/filter.png" alt class="filter">
    </mt-button>
    <mt-button slot="right" @click.native="$router.push('/exchange/order')">
      <img src="../../assets/img/transaction.png" alt class="transaction">
    </mt-button>
    <transition name="filter-fade">
      <div v-show="showFilter" class="filter-board">
        <span v-for="(item, index) in screen" :key="index">
          <span
            @click="chooseGeneration(item)"
            class="generation-btn"
            :class="{'active': generation == item.value}"
          >{{item.label}}</span>
        </span>
      </div>
    </transition>
    <div @click="showFilter = false" v-show="showFilter" class="filter-modal"></div>
    <div class="exchange">
      <div class="chart">
        <highcharts :options="options" ref="highcharts" class="charts"></highcharts>
      </div>
      <p class="chart-title">{{$t('exchange.chart_title')}}</p>
      <div class="content">
        <div class="sell-box" v-if="dataList.length">
          <div
            v-infinite-scroll="loadMore"
            infinite-scroll-disabled="allLoaded"
            infinite-scroll-distance="10"
          >
            <order-item
              class="order-item"
              v-for="(item, index) in dataList"
              :item="item"
              :key="index"
              :imgArr="imgArr"
            ></order-item>
          </div>
        </div>
        <div class="no-order" v-else>
          <img src="../../assets/img/icon_no.png" alt>
          <p>{{$t('common.no_exchange_order')}}</p>
        </div>
      </div>
    </div>
  </main-container>
</template>
<script>
import MainContainer from "app/components/elements/MainContainer";
import OrderItem from "./components/OrderItem";
import store from "app/store";
import {getChartsTime} from '../../utils/index.js';
export default {
  data() {
    return {
      screen: [
        {
          label: this.$t('common.all'),
          value: "31"
        },
        {
          label: this.$t('order.status_1'),
          value: "1"
        },
        {
          label: this.$t('order.status_2'),
          value: "2"
        },
        {
          label: this.$t('order.status_4'),
          value: "4"
        },
        {
          label: this.$t('order.status_8'),
          value: "8"
        },
        {
          label: this.$t('order.status_16'),
          value: "16"
        }
      ],
      showFilter: false,
      generation: "31",
      orgOptions: {},
      dataList: [],
      imgArr: [],
      options: {
        chart: {
          type: "line"
        },
        credits: {
          enabled: false
        },
        title: {
          text: null
        },
        subtitle: {
          text: null
        },
        xAxis: {
          reversed: true,
          title: {
            enabled: true,
            text: null
          },
          categories: [],
          maxPadding: 0.05
          // showLastLabel: true
        },
        yAxis: {
          title: {
            text: null
          },
          lineWidth: 2,
          visible: false
        },
        legend: {
          enabled: false
        },
        plotOptions: {
          spline: {
            marker: {
              enable: false
            }
          },
          series: {
            shadow: {
              color: "#485EF0",
              offsetX: "0px",
              offsetY: "10PX",
              opacity: ".6"
            }
          },
          line: {
            dataLabels: {
              // 开启数据标签
              enabled: true
            },
            // 关闭鼠标跟踪，对应的提示框、点击事件会失效
            enableMouseTracking: false
          }
        },
        series: [
          {
            name: this.$t('common.price'),
            color: "#485EF0",
            data: []
          }
        ]
      }
    };
  },
  mounted() {
    store.getRate();
    let symbolSize = 10;
    let data = [];
    let times = []
    this.$get("/member/currency/price_record", {
      params: {
        per_page: 7
      }
    }).then(res => {
      for(let i = 0; i < res.data.objects.length; i++) {
        let item = res.data.objects[i];
        data.push([Number(item.current_price)]);
        times.push(getChartsTime(item.created_timestamp));
        if(i == res.data.objects.length - 1) {
          this.options = {
            chart: {
              type: "line"
            },
            credits: {
              enabled: false
            },
            title: {
              text: null
            },
            subtitle: {
              text: null
            },
            xAxis: {
              reversed: true,
              title: {
                enabled: true,
                text: null
              },
              categories: times,
              maxPadding: 0.05
              // showLastLabel: true
            },
            yAxis: {
              title: {
                text: null
              },
              lineWidth: 2,
              visible: false
            },
            legend: {
              enabled: false
            },
            plotOptions: {
              spline: {
                marker: {
                  enable: false
                }
              },
              series: {
                shadow: {
                  color: "#CD941B",
                  offsetX: "0px",
                  offsetY: "10PX",
                  opacity: ".6"
                }
              },
              line: {
                dataLabels: {
                  // 开启数据标签
                  enabled: true
                },
                // 关闭鼠标跟踪，对应的提示框、点击事件会失效
                enableMouseTracking: false
              }
            },
            series: [
              {
                name: this.$t('common.price'),
                color: "#CD941B",
                data
              }
            ]
          };
        }
      }
    });
    let temp = [];
    this.$get("/member/payment/list").then(res => {
      for (let item of res.data.objects) {
        if (item.type == 0) {
          temp.push(require("../../assets/img/payment/bank.png"));
        }
        if (item.type == 1) {
          temp.push(require("../../assets/img/payment/wechat.png"));
        }
        if (item.type == 2) {
          temp.push(require("../../assets/img/payment/alipay.png"));
        }
        if (item.type == 3) {
          temp.push(require("../../assets/img/payment/usdt.png"));
        }
      }
      this.imgArr = temp;
    });
    this.getList(true);
  },
  methods: {
    handleFilter() {
      this.showFilter = !this.showFilter;
    },
    chooseGeneration(item) {
      this.generation = item.value;
      this.showFilter = false;
      this.getList(true);
    },
    getList(isInit) {
      if (isInit) {
        this.dataList = [];
        this.page = 1;
        this.allLoaded = false;
      }
      let params = {
        page: this.page,
        per_page: 5,
        status: this.generation
      };
      this.$get("/member/order", {
        params: params
      })
        .then(r => {
          this.dataList = this.dataList.concat(r.data.objects);
          if (r.data.total_pages > this.page) {
            this.allLoaded = false;
          } else {
            this.allLoaded = true;
          }
        })
        .catch(err => {});
    },
    loadMore() {
      this.page++;
      this.getList();
    }
  },
  computed: {},
  components: {
    MainContainer,
    OrderItem
  }
};
</script>
<style lang="scss" rel="stylesheet/scss">
.exchange-maket {
  & > header {
    z-index: 10001;
  }
  .filter,
  .transaction {
    width: 40px;
    height: 40px;
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
    > span {
      width: 33.3%;
      text-align: center;
      .generation-btn {
        &.active {
          background-image: linear-gradient(-90deg, #B0851E 0%, #F2C961 100%);
          color: #fff;
        }
        background: #f5f5f5;
        color: #616161;
        display: inline-block;
        width: 210px;
        height: 80px;
        font-size: 30px;
        line-height: 80px;
        border-radius: 4px;
        font-weight: 500;
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
  .exchange {
    position: relative;
    .chart {
      width: 100%;
      height: 287px;
      margin-top: 24px;
      margin-bottom: 24px;
      .charts {
        width: 100%;
        height: 287px;
        .highcharts-container {
          width: 100%;
          height: 287px;
          .highcharts-xaxis-grid .highcharts-grid-line {
            stroke-width: 2px;
            stroke: #d8d8d8;
          }
        }
      }
    }
    .chart-title {
      font-family: PingFangSC-Regular;
      font-size: 30px;
      color: #878787;
      letter-spacing: 0;
      line-height: 42px;
      text-align: center;
      margin-bottom: 16px;
    }
    .content {
      width: 100%;
      height: calc(100% - 287px - 48px - 58px);
      left: 0;
      position: relative;
      .sell-box {
        background: #f6f7f7;
        position: absolute;
        overflow: scroll;
        top: 0;
        width: 100%;
        height: 100%;
        left: 0;
        .order-item {
          margin-bottom: 24px;
        }
      }
      .no-order {
        width: 100%;
        height: 100%;
        text-align: center;
        img {
          width: 229px;
          height: 150px;
          margin-bottom: 24px;
          margin-top: 25%;
        }
        p {
          font-family: PingFangSC-Regular;
          font-size: 30px;
          color: #545454;
          letter-spacing: 0;
          line-height: 42px;
        }
      }
    }
  }
}
</style>
