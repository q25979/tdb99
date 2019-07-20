const express = require('express');

const app = require('./app');

const port = process.env.PORT || '7001';

app.use(express.static('public'));

module.exports = app.listen(port, (err) => {
  if (err) {
    console.log(err);
  } else {
    console.log(`listening on port ${port}`);
  }
});
