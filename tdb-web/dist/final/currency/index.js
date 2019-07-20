const fetch = require('node-fetch');

class CurrencyManager {
  constructor(options) {
    options = options || {};
    this._refreshTime = options.refreshTime || 1000 * 3600 * 24;
    this._allowedCurrency = options.allowedCurrency;
    this._fetching = null;
    this._cache = {
      time: 0,
      value: null
    };
  }

  update() {
    if (this._fetching) {
      return this._fetching;
    }
    this._fetching = fetch('http://api.fixer.io/latest')
      .then(resp => resp.json()).then(result => {
        return fetch('https://api.bitfinex.com/v1/pubticker/BTCUSD')
          .then(resp => resp.json()).then(btcResult => {
            result.rates.BTC = result.rates.USD / btcResult.mid;
            return result;
          });
      }).then(resp => {
        this._cache.time = Date.now();
        this._cache.value = resp;
        this._fetching = null;
        return resp;
      }).catch((err) => {
        this._fetching = null;
        throw err;
      });
    return this._fetching;
  }

  get(base) {
    const now = Date.now();
    let fetchPromise;
    if (this._cache.time === 0 || !this._cache.value) {
      fetchPromise = this.update();
    } else {
      fetchPromise = Promise.resolve(this._cache.value);
    }
    if (now - this._cache.time > 1000 * 3600 * 24) {
      this.update();
    }
    return fetchPromise.then(body => {
      body.rates[body.base] = 1;
      const baseRate = body.rates[base];
      if (this._allowedCurrency) {
        body.rates = this._allowedCurrency.reduce((value, key) => {
          value[key] = body.rates[key];
          return value;
        }, {});
      }
      return {
        base,
        rates: Object.keys(body.rates).reduce((value, key) => {
          value[key] = body.rates[key] / baseRate;
          return value;
        }, {})
      };
    });
  }
}

module.exports = new CurrencyManager({
  allowedCurrency: ['CNY', 'USD', 'EUR', 'GBP', 'CAD', 'BTC', 'JPY', 'AUD', 'HKD']
});
