const fetch = require('node-fetch');
const config = require('../config');
const url = require('url');

function formatCdnUrl(resource, schema) {
  resource = url.resolve(config.cdn, resource);
  if (resource && resource.startsWith('//') && schema) {
    resource = schema + ':' + resource;
  }
  return resource;
}

function fetchDetailHtml(url) {
  return fetch(formatCdnUrl(url, 'http')).then(resp => resp.text());
}

function formatPrice(price) {
  return Number(price).toFixed(2);
}

module.exports = {
  formatCdnUrl,
  fetchDetailHtml,
  formatPrice
};
