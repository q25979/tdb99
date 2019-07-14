import Vue from 'vue';

Vue.filter('time', (v, format='yyyy-MM-dd hh:mm:ss') => {
  if(!v) return '';
  const _date = new Date(v*1000);
  const date = {
    'M+': _date.getMonth() + 1,
    'd+': _date.getDate(),
    'h+': _date.getHours(),
    'm+': _date.getMinutes(),
    's+': _date.getSeconds(),
    'q+': Math.floor((_date.getMonth() + 3) / 3),
    'S+': _date.getMilliseconds()
  };
  if (/(y+)/i.test(format)) {
    format = format.replace(RegExp.$1, (_date.getFullYear() + '').substr(4 - RegExp.$1.length));
  }
  for (let k in date) {
    if (new RegExp('(' + k + ')').test(format)) {
      format = format.replace(RegExp.$1, RegExp.$1.length == 1
      ? date[k] : ('00' + date[k]).substr(('' + date[k]).length));
    }
  }
  return format;
});

Vue.filter('currency', (v, num) => {
  if(num) {
    return parseFloat(v).toFixed(num);
  } else {
    return parseFloat(v);
  }
});

Vue.filter('type', v => {
  let typeObj = {
    0: '全部',
    0x0001: '充值',
    0x0002: '提现',
    0x0004: '转账',
    0x0008: '闪兑',
    0x0010: '空投',
    0x0020: '释放',
    0x0040: '直推奖励',
    0x0080: '团队奖励',
    0x0100: '管理员充值'
  };
  return typeObj[v]
});