<template>
  <main-container :hasHeader='false' containerColor='#fff' :noHeader='true' :hasTabbar='false'>
    <div class="auth-answer">
      <div class="question-fields" v-if="!isResult">
        <header>
          {{$t('common.question')}} {{activeIndex + 1}}/10
        </header>
        <div class="radio-container" v-for="(item, index) in questionArr" :key="index">
          <mt-radio
            :title="item.title"
            v-model="activeValue"
            v-if="index == activeIndex"
            :options="item.options">
          </mt-radio>
        </div>
        <mt-button type="primary" :disabled="!activeValue" @click="handleClick">
        {{$t('common.submit')}}
        </mt-button>
      </div>
      <div class="answer-result" v-else>
        <header>
          <i class="icon icon-evaluation-success"></i>
        </header>
        <div>
          {{$t('tips.answer_success')}}
        </div>
        <div>
          {{$t('answer.tips')}}
        </div>
        <mt-button type="primary" @click="$router.push('/')">
          {{$t('common.receive')}}
        </mt-button>
      </div>
    </div>
  </main-container>
</template>
<script>
import MainContainer from 'app/components/elements/MainContainer';
import store from 'app/store';
export default {
  data() {
    return {
      isResult: false,
      activeValue: '',
      activeIndex: 0,
      questionArr: [{
        title: `${this.$t('question.ul1')}：--`,
        options: [{
          label: this.$t('question.li1_1'),
          value: '0'
        }, {
          label: this.$t('question.li1_2'),
          value: '1'
        }, {
          label: this.$t('question.li1_3'),
          value: '2'
        }, {
          label: this.$t('question.li1_4'),
          value: '3'
        }],
        correct: '3'
      }, {
        title: `${this.$t('question.ul2')}：--`,
        options: [{
          label: this.$t('question.li2_1'),
          value: '0'
        }, {
          label: this.$t('question.li2_2'),
          value: '1'
        }, {
          label: this.$t('question.li2_3'),
          value: '2'
        }, {
          label: this.$t('question.li2_4'),
          value: '3'
        }],
        correct: '3'
      }, {
        title: `${this.$t('question.ul3')}：--`,
        options: [{
          label: this.$t('question.li3_1'),
          value: '0'
        }, {
          label: this.$t('question.li3_2'),
          value: '1'
        }, {
          label: this.$t('question.li3_3'),
          value: '2'
        }, {
          label: this.$t('question.li3_4'),
          value: '3'
        }],
        correct: '3'
      }, {
        title: `${this.$t('question.ul4')}：--`,
        options: [{
          label: this.$t('question.li4_1'),
          value: '0'
        }, {
          label: this.$t('question.li4_2'),
          value: '1'
        }, {
          label: this.$t('question.li4_3'),
          value: '2'
        }, {
          label: this.$t('question.li4_4'),
          value: '3'
        }],
        correct: '0'
      }, {
        title: `${this.$t('question.ul5')}：--`,
        options: [{
          label: this.$t('question.li5_1'),
          value: '0'
        }, {
          label: this.$t('question.li5_2'),
          value: '1'
        }, {
          label: this.$t('question.li5_3'),
          value: '2'
        }, {
          label: this.$t('question.li5_4'),
          value: '3'
        }],
        correct: '2'
      }, {
        title: `${this.$t('question.ul6')}：--`,
        options: [{
          label: this.$t('question.li6_1'),
          value: '0'
        }, {
          label: this.$t('question.li6_2'),
          value: '1'
        }, {
          label: this.$t('question.li6_3'),
          value: '2'
        }, {
          label: this.$t('question.li6_4'),
          value: '3'
        }],
        correct: '1'
      }, {
        title: `${this.$t('question.ul7')}：--`,
        options: [{
          label: this.$t('question.li7_1'),
          value: '0'
        }, {
          label: this.$t('question.li7_2'),
          value: '1'
        }, {
          label: this.$t('question.li7_3'),
          value: '2'
        }, {
          label: this.$t('question.li7_4'),
          value: '3'
        }],
        correct: '0'
      }, {
        title: `${this.$t('question.ul8')}：--`,
        options: [{
          label: `${this.$t('question.li8_1')} 20%`,
          value: '0'
        }, {
          label: `${this.$t('question.li8_2')} 20%`,
          value: '1'
        }, {
          label: `${this.$t('question.li8_3')} 15%`,
          value: '2'
        }, {
          label: `${this.$t('question.li8_4')} 10%`,
          value: '3'
        }],
        correct: '2'
      }, {
        title: `${this.$t('question.ul9')}：--`,
        options: [{
          label: this.$t('question.li9_1'),
          value: '0'
        }, {
          label: this.$t('question.li9_2'),
          value: '1'
        }, {
          label: this.$t('question.li9_3'),
          value: '2'
        }, {
          label: this.$t('question.li9_4'),
          value: '3'
        }],
        correct: '3'
      }, {
        title: `${this.$t('question.ul10')}：--`,
        options: [{
          label: this.$t('question.li10_1'),
          value: '0'
        }, {
          label: this.$t('question.li10_2'),
          value: '1'
        }, {
          label: this.$t('question.li10_3'),
          value: '2'
        }, {
          label: this.$t('question.li10_4'),
          value: '3'
        }],
        correct: '0'
      }]
    };
  },
  computed: {
  },
  mounted() {
  },
  methods: {
    handleClick() {
      if(this.activeValue === this.questionArr[this.activeIndex].correct) {
        if(this.activeIndex == this.questionArr.length - 1) {
          this.$post('/member/user/evaluation', {}).then(res => {
            store.updateMemberProfile(res.data);
            this.isResult = true;
          }).catch(err => {
          });
          return false;
        }
        this.activeValue = '';
        this.activeIndex++;
      } else {
        this.messagebox({
          message: this.$t('errors.answer_error'),
          confirmButtonText: this.$t('common.sure')
        });
      }
    }
  },
  components: {
    MainContainer,
  }
};
</script>
<style lang="scss" rel="stylesheet/scss">
  .auth-answer {
    .question-fields {
      &>header {
        margin-top: 58px;
        font-family: PingFangSC-Regular;
        font-size: 64px;
        color: #222;
        padding-left: 32px;
        margin-bottom: 37px;
        line-height: 1;
      }
      .mint-radiolist {
        .mint-radiolist-title {
          margin: 0;
          margin-bottom: 32px;
          padding: 0 34px;
          font-size: 34px;
          color: #545454;
        }
        .mint-cell {
          margin: 0 32px 24px;
          .mint-cell-wrapper {
            padding-left: 0px !important;
            padding-right: 0px !important;
            background-color: #f1f1f1 !important;
            border-radius: 4px;
            .mint-cell-title {
              .mint-radiolist-label {
                display: flex;
                align-items: center;
                .mint-radio {
                  .mint-radio-input {

                  }
                  .mint-radio-core {
                    background-size: 100%;
                    background-image: url('../../assets/img/icon/radio.png');
                    border: 0;
                    &:after {
                      display: none !important;
                    }
                  }
                  .mint-radio-input:checked + .mint-radio-core {
                    background-image: url('../../assets/img/icon/radio_selected.png');
                  }
                }
                .mint-radio-label {
                  line-height: 40px;
                }
              }
            }
          }
        }
      }
      .mint-button {
        margin: 200px 32px 0px;
        display: block;
        width: calc(100% - 64px);
        box-shadow: none;
        border: 0;
        font-family: PingFangSC-Regular;
        font-size: 36px;
        opacity: 1 !important;
        height: 98px;
      }
    }
    .answer-result {
      header {
        text-align: center;
        margin-top: 80px;
        i {
          width: 130px;
          height: 130px;
          background-image: url('../../assets/img/icon/evaluation_success.png');
        }
      }
      &>div {
        padding: 0 135px;
        text-align: center;
        &:nth-child(2) {
          font-size: 40px;
          color: #333333;
          margin-top: 64px;
        }
        &:nth-child(3) {
          font-size: 30px;
          color: #545454;
          margin-top: 24px;
        }
      }
      .mint-button {
        height: 104px;
        border-radius: 48px;
        width: 320px;
        margin: 81px auto 0;
        display: block;
      }
    }
  }
</style>
