// http://eslint.org/docs/user-guide/configuring

module.exports = {
  root: true,
  parser: 'babel-eslint',
  parserOptions: {
    sourceType: 'module'
  },
  env: {
    browser: true
  },
  // https://github.com/feross/standard/blob/master/RULES.md#javascript-standard-style
  extends: 'google',
  // required to lint *.vue files
  plugins: [
    'html'
  ],
  // add your custom rules here
  'rules': {
    'indent': ['error', 2],
    'max-len': [1, 120, 2, {
      ignoreUrls: true,
      ignoreRegExpLiterals: true
    }],
    'require-jsdoc': 0,
    'no-invalid-this': 1,
    'comma-dangle': 0,
    // allow paren-less arrow functions
    'arrow-parens': 0,
    // allow async-await
    'generator-star-spacing': 0,
    // allow debugger during development
    'no-debugger': process.env.NODE_ENV === 'production' ? 2 : 0,
    'new-cap': 0,
    'no-invalid-this': 0,
  }
};
