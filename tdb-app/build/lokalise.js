const ora = require('ora');
const rm = require('rimraf');
const chalk = require('chalk');
const config = require('../config');
const fetch = require('node-fetch');
const FormData = require('form-data');
const unzip = require('unzip');

const urlPrefix = 'https://s3-eu-west-1.amazonaws.com/lokalise-assets/';

const form = new FormData();
form.append('api_token', config.lokalise.apiToken);
form.append('id', config.lokalise.projectId);
form.append('type', 'json');
form.append('use_original', 0);
form.append('bundle_filename', '%PROJECT_NAME%-Locale.zip');
form.append('bundle_structure', '%LANG_ISO%.%FORMAT%');
form.append('filter', 'translated');

var spinner = ora('exporting from lokalise...');
spinner.start();
fetch('https://lokalise.co/api/project/export', {
  method: 'POST',
  body: form
}).then(resp => resp.json()).then(body => {
  spinner.stop();
  if (body.response.code == 200) {
    const bundleFile = urlPrefix + body.bundle.file;
    console.log(chalk.green(`Extract ${bundleFile} to ${config.lokalise.localeRoot}`));
    fetch(bundleFile).then(resp => {
      if (!resp.ok) {
        throw new Error(`Wrong status ${resp.status} ${resp.statusText}`);
      }
      var entries = [];

      return new Promise((resolve, reject) => {
        rm(config.lokalise.localeRoot, err => {
          if (err) {
            return reject(err);
          }
          resp.body.pipe(unzip.Extract({
            path: config.lokalise.localeRoot
          })).on('entry', entry => {
            entries.push(entry);
            console.log(chalk.blue(`Extract ${entry}`));
          }).on('error', reject)
            .on('close', () => {
              resolve(entries);
            });
        });
      });
    }).then(result => {
      console.log(chalk.green(`Done`));
    }).catch(err => {
      console.log(chalk.red(err.message));
    });
  } else {
    console.log(chalk.red(body.response.message));
  }
}).catch(err => {
  throw err;
});
