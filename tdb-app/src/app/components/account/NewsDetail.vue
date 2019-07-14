<template>
  <main-container class="news-detail" :title="$t('news.details')" containerColor="#fff" :hasTabbar="false">
    <mt-button slot="left" icon="back" @click.native="$router.go(-1)"></mt-button>
    <div class="news-content">
      <div v-html="news.details"></div>
    </div>
  </main-container>
</template>

<script>
import MainContainer from 'app/components/elements/MainContainer';
export default {
  data() {
    return {
      news:{}
    }
  },
  mounted(){
    this.getNews();
  },
  methods:{
    getNews(){
      let id = this.$route.query.id;
      this.$get(`/member/news/detail/${id}`).then(res => {
        this.news = res.data
      })
    }
  },
  components:{MainContainer}
}
</script>

<style lang="scss" rel="stylesheet/scss">
  .news-detail {
    .news-content {
      color: #222;
      padding: 32px 32px;
      line-height: 1.8;
      * {
        font-size: 30px;
      }
    }

  }
</style>

