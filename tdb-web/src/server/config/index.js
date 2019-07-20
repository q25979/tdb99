const mode = process.env.NODE_ENV || 'development';
const base = require('./base');
const config = Object.assign(base, require('./' + mode));
if (config.apiEndPoint && !config.apiEndPoint.endsWith('/')) {
  config.apiEndPoint += '/';
}
module.exports = config;
