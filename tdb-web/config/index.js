// see http://vuejs-templates.github.io/webpack for documentation.
var path = require('path');
var url = require('url');
var appConfig = require('../src/server/config');
var ossBasePath = 'lebo/qrcode/';
var cdnBasePath = url.resolve(appConfig.cdn, ossBasePath);
module.exports = {
  app: appConfig,
  lokalise: {
    apiToken: '28018eacf590c54a9babeba3cf42fc6a4df703b3',
    projectId: '16138072598194c986fac4.95738592',
    localeRoot: path.resolve(__dirname, '../src/app/i18n/locale'),
  },
  oss: {
    accessKeyId: 'LTAId5JGkZzEFYSw',
    accessKeySecret: 'y9DCNzafnatLMxE1s7IxqvI5NlQe0M',
    bucket: 'xiaoyu168',
    region: 'oss-ap-southeast-1',
  },
  build: {
    env: require('./prod.env'),
    ossBasePath: ossBasePath,
    cdnBasePath: cdnBasePath,
    index: path.resolve(__dirname, '../dist/final/public/index.html'),
    distRoot: path.resolve(__dirname, '../dist'),
    serverRoot: path.resolve(__dirname, '../dist/final'),
    assetsRoot: path.resolve(__dirname, '../dist/final/public'),
    assetsSubDirectory: 'static',
    assetsPublicPath: cdnBasePath,
    productionSourceMap: true,
    // Gzip off by default as many popular static hosts such as
    // Surge or Netlify already gzip all static assets for you.
    // Before setting to `true`, make sure to:
    // npm install --save-dev compression-webpack-plugin
    productionGzip: false,
    productionGzipExtensions: ['js', 'css'],
    // Run the build command with an extra argument to
    // View the bundle analyzer report after build finishes:
    // `npm run build --report`
    // Set to `true` or `false` to always turn it on or off
    bundleAnalyzerReport: process.env.npm_config_report,
    downloadUrl: require('./prod.env')['DOWNLOAD_URL'][process.env.URL_ENV]
  },
  dev: {
    env: require('./dev.env'),
    port: 8088,
    autoOpenBrowser: true,
    assetsSubDirectory: 'static',
    assetsPublicPath: '/',
    proxyTable: {
    },
    // CSS Sourcemaps off by default because relative paths are "buggy"
    // with this option, according to the CSS-Loader README
    // (https://github.com/webpack/css-loader#sourcemaps)
    // In our experience, they generally work as expected,
    // just be aware of this issue when enabling this option.
    cssSourceMap: false
  }
};
