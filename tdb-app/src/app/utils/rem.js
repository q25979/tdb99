(function(doc, win) {
  const docEl = doc.documentElement || doc.body;
  const resizeEvt = 'orientationchange' in window ? 'orientationchange' : 'resize';
  const recalc = function() {
    const clientWidth = docEl.clientWidth || win.innerWidth || win.screen.width;
    if (!clientWidth) return;
    docEl.style.fontSize = (clientWidth / 10) + 'px';
  };
  if (!doc.addEventListener) return;
  win.addEventListener(resizeEvt, recalc, false);
  doc.addEventListener('DOMContentLoaded', recalc, false);


  doc.addEventListener("deviceready", onDeviceReady, false);
  function onDeviceReady() {
    if (navigator.userAgent.match(/(iPhone)/)) {
      if ((screen.availHeight == 647) && (screen.availWidth == 375) && (window.devicePixelRatio == 3)) {
          StatusBar.hide()
      }
    }
  }
})(document, window);
