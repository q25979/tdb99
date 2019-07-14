const express = require('express');
const cookieParser = require('cookie-parser');
const app = express();

app.use(cookieParser());

// handle fallback for HTML5 history API
app.use(require('connect-history-api-fallback')());

app.config = require('./config');

module.exports = app;
