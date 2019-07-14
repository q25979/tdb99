<template>
  <main-container class="quotes" :title="$t('account.news_title')" containerColor="#fff" :hasTabbar="false">
    <mt-button slot="left" icon="back" @click.native="$router.push('/account')"></mt-button>
    <div class="news-container">
      <no-tips :text="$t('common.no_content')" v-if="!dataList.length"></no-tips>
      <mt-loadmore
      :bottom-method="loadBottom"
      :bottom-all-loaded="allLoaded"
      ref="loadmore"
      :auto-fill="false"
      :bottomLoadingText="$t('common.loading')"
      :bottomDropText="$t('common.release_update')">
        <ul>
          <li v-for="(item, index) in dataList" :key="index" @click="$router.push('/account/news_detail?id='+item.id)">
            <div class="header">
              <header>{{item.title}}</header>
              <div class="time">{{item.created_at | time}}</div>
            </div>
            <div class="summary">
              {{handleDetails(item.details)}}
            </div>
            <div class="detail-btn" >
              {{$t('news.look_details')}} 
              <img src="../../assets/img/icon/icon_right.png" alt="">
            </div>
          </li>
        </ul>
      </mt-loadmore>
    </div>
  </main-container>
</template>
<script>
import NoTips from 'app/components/elements/NoTips';
import MainContainer from 'app/components/elements/MainContainer';
export default {
  data() {
    return {
      selected: 'news',
      dataList: [],
      page: 1,
      allLoaded: false
    };
  },
  computed: {
  },
  mounted() {
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
          per_page: 10,
          page: this.page
        }
      }).then(r => {
        if(r.data.total_pages > this.page) {
          this.allLoaded = false;
        } else {
          this.allLoaded = true;
        }
        this.dataList = this.dataList.concat(r.data.objects);
      }).catch(err => {
      });
    },
    loadBottom() {
      this.$refs.loadmore.onBottomLoaded();
      this.page++;
      this.getList();
    }
  },
  watch: {
  },
  components: {
    MainContainer,
    NoTips
  },
};
</script>
<style lang="scss" rel="stylesheet/scss">
  .news-container {
    ul {
      li {
        padding: 24px 32px;
        position: relative;
        border-bottom: 1px solid #EDEFF3;
        .header {
          font-family: PingFangSC-Regular;
          display: flex;
          align-items: center;
          header {
            font-size: 34px;
            width: 58%;
            color: #222222;
          }
          .time {
            font-family: PingFangSC-Regular;
            font-size: 26px;
            width: 40%;
            color: #474747;
            text-align: right;
          }
        }
        .summary {
          font-family: PingFangSC-Regular;
          font-size: 32px;
          color: #878787;
          margin-top: 22px;
          margin-bottom: 30px;
          width: 80%;
          white-space: nowrap;
          text-overflow:ellipsis;
          overflow:hidden;
        }
        .detail-btn {
          font-size: 26px;
          line-height: 28px;
          color: #EBCE75;
          display: flex;
          justify-content: flex-end;
          img {
            width: 24px;
            height: 28px;
            margin-left: 6px;
          }
        }
      }
    }
  }
</style>
