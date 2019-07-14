// see http://vuejs-templates.github.io/webpack for documentation.
var path = require('path');
var appConfig = require('../src/server/config');
module.exports = {
  app: appConfig,
  lokalise: {
    apiToken: '28018eacf590c54a9babeba3cf42fc6a4df703b3',
    projectId: '16138072598194c986fac4.95738592',
    localeRoot: path.resolve(__dirname, '../src/app/i18n/locale'),
  },
  build: {
    env: require('./prod.env'),
    index: path.resolve(__dirname, '../dist/final/public/index.html'),
    distRoot: path.resolve(__dirname, '../dist'),
    serverRoot: path.resolve(__dirname, '../dist/final'),
    assetsRoot: path.resolve(__dirname, '../dist/final/public'),
    assetsSubDirectory: 'static',
    assetsPublicPath: '',
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
    apiEndPoint: require('./prod.env')['API_END_POINT'][process.env.API_URL]
  },
  dev: {
    env: require('./dev.env'),
    port: 5050,
    autoOpenBrowser: false,
    assetsSubDirectory: 'static',
    assetsPublicPath: '/',
    proxyTable: {
      '/api/**': {
        target: 'http://127.0.0.1:5000',
        // target: 'http://api.tdb99.com',
        changeOrigin: true,
        pathRewrite: {
          '^/api': '/'
        },
      },
    },
    // CSS Sourcemaps off by default because relative paths are "buggy"
    // with this option, according to the CSS-Loader README
    // (https://github.com/webpack/css-loader#sourcemaps)
    // In our experience, they generally work as expected,
    // just be aware of this issue when enabling this option.
    cssSourceMap: false,
    apiEndPoint: require('./prod.env')['API_END_POINT']['staging'],
  },
};
