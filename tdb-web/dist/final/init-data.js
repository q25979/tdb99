const currency = require('./currency');
const fs = require('fs');

function generateScript(exrate) {
  return `window.initData=${JSON.stringify({
    exrate
  })}`;
}

module.exports = {
  compose(req) {
    return currency.get('USD')
      .then(exrate => {
        fs.writeFile('./src/server/exrate.config.json', JSON.stringify(exrate, null, 2), 'utf8', error => { });
        return generateScript(exrate);
      }).catch(() => {
        const exrate = require('./exrate.config.json');
        return generateScript(exrate);
      });
  }
};
