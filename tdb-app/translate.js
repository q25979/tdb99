const jsonfile = require('jsonfile');
const lang = 'vi';
const file = './src/app/i18n/locale/cn.json';
const esFile = `./src/app/i18n/locale/${lang}.json`;
const request = require('request');
const traditionalize = require("hanzi-tools").traditionalize;
const key1 = 'trnsl.1.1.20171101T112134Z.c3788eb249fee851.ea02e687d8898e053b842b34400df9aac14dcddc';
const key2 = 'trnsl.1.1.20170915T040921Z.44c071ab10c84598.0ea459723b55a70a5a6a2c05cd66c5080179bfa5';
const key3 = 'trnsl.1.1.20170920T123957Z.7537863a1f564d60.25c2b433420eea0a996f6c7d88689a6185bd16a5';
const key4 = 'trnsl.1.1.20170626T113046Z.3600f26f4639e211.58298c04b023e83062fd474386be66af75b58848';

jsonfile.readFile(file, function(err, obj) {
  let length = 0;
  let keyArr = [];
  let valueArr = [];
  for(let k in obj) {
    length++;
    keyArr.push(k);
    valueArr.push(obj[k]);
  }
  let temp = 0;
  function translateFun() {
    request.post({
      url: `https://translate.yandex.net/api/v1.5/tr.json/translate?key=${key3}&lang=${lang}`,
      form: {text: valueArr[temp]}
    }, function(err, res, body) {
      if(err) {
        valueArr[temp] = false;
      } else {
        console.log(body.text, err, res);
        body = JSON.parse(body);
        valueArr[temp] = body.text[0];
      }
      temp++;
      if(temp >= length) {
        let obj = {};
        for(let i = 0; i <= length; i++) {
          if(i < length) {
            obj[keyArr[i]] = valueArr[i];
          }
          if(i == length) {
            jsonfile.writeFile(esFile, obj, {spaces: 2, EOL: '\r\n'}, function(err) {
              if(!err) {
                console.log('transfer success!');
                return false;
              }
            });
          }
        }
      } else {
        console.log(`finish ${temp}/${length}`);
        translateFun();
      }
    });
  }
  if(lang == 'hk') {
    for(let item of valueArr) {
      valueArr[temp] = traditionalize(item);
      temp++;
      if(temp >= length) {
        let obj = {};
        for(let i = 0; i <= length; i++) {
          if(i < length) {
            obj[keyArr[i]] = valueArr[i];
          }
          if(i == length) {
            jsonfile.writeFile(esFile, obj, {spaces: 2, EOL: '\r\n'}, function(err) {
              if(!err) {
                console.log('transfer success!');
                return false;
              }
            });
          }
        }
      } else {
        console.log(`finish ${temp}/${length}`);
      }
    }
  } else {
    translateFun();
  }
});


