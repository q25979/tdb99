import axios from 'axios';
import {Toast, Indicator} from 'mint-ui';
import store from 'app/store';
import router from 'app/router';

const toast = Toast;

axios.interceptors.request.use((config) => {
  Indicator.open();
  return config;
}, (err) => {
  return Promise.reject(err);
});

axios.interceptors.response.use(
  response => {
    Indicator.close();
    return response;
  },
  error => {
    Indicator.close();
    if (error.response) {
      switch (error.response.status) {
      case 401:
        store.unauth();
        break;
      case 500:
        toast({message: '服务器错误，请稍后重试'});
      }
    }
    return Promise.reject(error.response.data);
  }
);

const makeUrl = (url, param={}) => {
  url = BASE_URL + url;
  if(localStorage.getItem('token')) {
    let obj = Object.assign({}, {token: localStorage.getItem('token')}, param);
    const args = Object.entries(obj).map((k) =>
    `${encodeURIComponent(k[0])}=${encodeURIComponent(k[1])}`);
    url = [url, args.join('&')].join(url.indexOf('?') >= 0 ? '&' : '?');
  }
  return url;
};


export function get(url, param) {
  if(param) {
    param = param.params;
  }
  return new Promise((resolve, reject) => {
    axios.get(makeUrl(url, param)).then(res => {
      resolve(res);
    }).catch(err => {
      reject(err);
    });
  });
};

export function post(url, param={}) {
  return new Promise((resolve, reject) => {
    axios.post(makeUrl(url), param).then(res => {
      resolve(res);
    }).catch(err => {
      reject(err);
    });
  });
};

export function put(url, param={}) {
  return new Promise((resolve, reject) => {
    axios.put(makeUrl(url), param).then(res => {
      resolve(res);
    }).catch(err => {
      reject(err);
    });
  });
};

export function deletes(url, param={}) {
  if(param) {
    param = param.params;
  }
  return new Promise((resolve, reject) => {
    axios.delete(makeUrl(url)).then(res => {
      resolve(res);
    }).catch(err => {
      reject(err);
    });
  });
};

export function upload(url, param={}) {
  return new Promise((resolve, reject) => {
    axios.post(makeUrl(url), param, {
      headers: {'Content-Type': 'multipart/form-data'}
    }).then(res => {
      resolve(res);
    }).catch(err => {
      reject(err);
    });
  });
};
