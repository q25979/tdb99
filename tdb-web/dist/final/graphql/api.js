const fetch = require('node-fetch');
const url = require('url');
const config = require('../config');

class ApiError extends Error {
  constructor(response, body) {
    super('Api Error');
    this._response = response;
    const {status} = response;
    if (status === 401) {
      this.authRequired = true;
    }
    this.apiStatus = status;
    this.cause = body;
  }
}

function makeUrl(method, ctx) {
  while (method.startsWith('/')) {
    method = method.substr(1);
  }
  let apiUrl = url.resolve(config.apiEndPoint, method);
  if (ctx) {
    const args = Object.entries(ctx).map((k) =>
      `${encodeURIComponent(k[0])}=${encodeURIComponent(k[1])}`);
    apiUrl = [apiUrl, args.join('&')].join(apiUrl.indexOf('?') >= 0 ? '&' : '?');
  }
  return apiUrl;
}

function handleResponse(fetchPromise) {
  return fetchPromise.then(res => {
    if (res.status == 401) {
      return res.json().then(body => {
        return Promise.reject(new ApiError(res, body));
      });
    } else {
      return res;
    }
  });
}

function get(method, ctx) {
  return handleResponse(fetch(makeUrl(method, ctx)));
}

function post(method, ctx, data) {
  if (typeof data === 'object') {
    data = JSON.stringify(data);
  }
  return handleResponse(fetch(makeUrl(method, ctx), {
    method: 'POST',
    body: data,
    headers: {'Content-Type': 'application/json'}
  }));
}

function put(method, ctx, data) {
  if (typeof data === 'object') {
    data = JSON.stringify(data);
  }
  return handleResponse(fetch(makeUrl(method, ctx), {
    method: 'PUT',
    body: data,
    headers: {'Content-Type': 'application/json'}
  }));
}

function deleteMethod(method, ctx) {
  return handleResponse(fetch(makeUrl(method, ctx), {method: 'DELETE'}));
}

module.exports = {
  get,
  post,
  put,
  deleteMethod,
  ApiError
};
