<template>
  <main-container class="quotes" :title="$t('common.node_profit')" containerColor="#fff" :hasTabbar="false">
    <mt-button slot="left" icon="back" @click.native="$router.go(-1)"></mt-button>
    <div class="node-profit">
      <no-tips :text="$t('common.no_record')" v-if="!dataList.length"></no-tips>
      <mt-loadmore
      :bottom-method="loadBottom"
      :bottom-all-loaded="allLoaded"
      ref="loadmore"
      :auto-fill="false"
      :bottomLoadingText="$t('common.loading')">
        <record-item v-for="(item, index) in dataList" :key="index" :item="item">
        </record-item>
      </mt-loadmore>
    </div>
  </main-container>
</template>
<script>
import NoTips from 'app/components/elements/NoTips';
import MainContainer from 'app/components/elements/MainContainer';
import RecordItem from 'app/components/finance/elements/RecordItem';
export default {
  data() {
    return {
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
    getList() {
      let params = {
        page: this.page,
        per_page: 10,
        record_type: 512
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
    NoTips,
    RecordItem
  },
};
</script>
<style lang="scss" rel="stylesheet/scss">
  .node-profit {
  }
</style>
