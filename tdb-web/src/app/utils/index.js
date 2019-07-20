const setTitleHack = function(t) {
  document.title = t;
  let iframe = document.createElement('iframe');
  iframe.style.visibility = 'hidden';
  iframe.style.width = '1px';
  iframe.style.height = '1px';
  iframe.src = '../../../favicon.ico';
  iframe.onload = function() {
    setTimeout(function() {
      iframe.remove();
    }, 10);
  };
  document.body.appendChild(iframe);
};

const setWechatTitle = function(title) {
  document.title = title;
  let mobile = navigator.userAgent.toLowerCase();
  if (/iphone|ipad|ipod/.test(mobile)) {
    let iframe = document.createElement('iframe');
    iframe.style.visibility = 'hidden';
    // 替换成站标favicon路径或者任意存在的较小的图片即可
    iframe.setAttribute('src', '../../../favicon.ico');
    let iframeCallback = function() {
      setTimeout(function() {
        iframe.removeEventListener('load', iframeCallback);
        document.body.removeChild(iframe);
      }, 10);
    };
    iframe.addEventListener('load', iframeCallback);
    document.body.appendChild(iframe);
  }
};

module.exports = {
  setTitleHack,
  setWechatTitle
};
