module.exports = {
  getCommonTime(time) {
    const oDate = new Date(time*1000);
    const oYear = oDate.getFullYear();
    const oMonth = oDate.getMonth()+1;
    const oDay = oDate.getDate();
    const oHour = oDate.getHours();
    const oMin = oDate.getMinutes();
    return `${oYear}-${getNum(oMonth)}-${getNum(oDay)} 
     ${getNum(oHour)}:${getNum(oMin)}`;
    function getNum(num) {
      return parseInt(num) < 10 ? `0${num}` : num;
    }
  },
  uuid() {
    const s = [];
    const hexDigits = '0123456789abcdef';
    for (let i = 0; i < 36; i++) {
      s[i] = hexDigits.substr(Math.floor(Math.random() * 0x10), 1);
    }
    s[14] = '4';  // bits 12-15 of the time_hi_and_version field to 0010
    s[19] = hexDigits.substr((s[19] & 0x3) | 0x8, 1);  // bits 6-7 of the clock_seq_hi_and_reserved to 01
    s[8] = s[13] = s[18] = s[23] = '-';

    const uuid = s.join('');
    return uuid;
  },
  getChartsTime(time) {
    const oDate = new Date(time*1000);
    const oYear = oDate.getFullYear();
    const oMonth = oDate.getMonth()+1;
    const oDay = oDate.getDate();
    return `${getNum(oMonth)}-${getNum(oDay)}`;
    function getNum(num) {
      return parseInt(num) < 10 ? `0${num}` : num;
    }
  }
};

  
