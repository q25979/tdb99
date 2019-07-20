const fs = require('fs');

function buildIndex(data) {
  return {
    data,
  };
}

class CountryDatabase {
  constructor(dbFile) {
    this._db = dbFile;
  }

  getAll() {
    return this._getDb().then(idx => idx.data);
  }
  
  _getDb() {
    if (this._index) {
      return Promise.resolve(this._index);
    } else {
      return new Promise((resolve, reject) => {
        fs.readFile(this._db, 'utf-8', (err, content) => {
          if (err) {
            reject(err);
          } else {
            this._index = buildIndex(JSON.parse(content));
            resolve(this._index);
          }
        });
      });
    }
  }
}

module.exports = CountryDatabase;
