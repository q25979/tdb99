<template>
  <div class='record-item'>
    <div class="content">
      <div class='left'>
        <p >{{getType(item.record_type)}}</p>
        <span>{{item.created_at | time}}</span>
      </div>
      <div class='right'>
        <p>
          {{getNumber(item.delta_amount) >= 0 ? `+${item.delta_amount}` : item.delta_amount}}
        </p>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  props: ['item'],
  data() {
    return {};
  },
  methods: {
    formatAddress(address) {
      return address.replace(/([0-9a-zA-Z\w]{4})[0-9a-zA-Z\w]*([0-9a-zA-Z\w]{5})/, "$1....$2");
    },
    getNumber(val) {
      return parseFloat(val);
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
  }
};
</script>
<style lang="scss">
  .record-item {
    display: flex;
    justify-content: space-between;
    padding-top: 32px;  
    padding-left: 32px;
    background: #fff;
    .content {
      display: flex;
      justify-content: space-between;
      flex: 1;
      padding-right: 32px;
      border-bottom: 2px solid #E6E6E6;
      width: calc(100% + 64px);
      padding-bottom: 20px;
      align-items: center;
      .left {
        display: flex;
        flex-direction: column;

        p {
          font-size: 30px;
          color: #222;
        }

        span {
          margin-top: 20px;
          font-size: 24px;
          color: #818181;;
        }
      }
    }

    .right {
      display: flex;
      flex-direction: column;
      text-align: right;

      p {
        font-size: 30px;
        color: #CD941B;
        text-align: right;
        font-weight: 500;
      }

      span {
        font-size: 28px;
        line-height: 44px;
        color: rgba(255, 255, 255, .3);
      }
    }
  }
</style>


