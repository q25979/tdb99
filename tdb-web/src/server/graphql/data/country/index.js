const g = require('graphql');
const path = require('path');
const Database = require('./database');

const db = new Database(path.join(__dirname, 'countries.json'));

const currencyType = new g.GraphQLObjectType({
  name: 'Currency',
  fields: () => ({
    code: {
      type: g.GraphQLString
    },
    name: {
      type: g.GraphQLString
    },
    symbol: {
      type: g.GraphQLString
    }
  })
});

const languageType = new g.GraphQLObjectType({
  name: 'Language',
  fields: () => ({
    name: {
      type: g.GraphQLString
    },
    nativeName: {
      type: g.GraphQLString
    },
    iso639_1: {
      type: g.GraphQLString
    },
    iso639_2: {
      type: g.GraphQLString
    }
  })
});

const countryType = new g.GraphQLObjectType({
  name: 'Country',
  fields: () => ({
    cn: {
      type: g.GraphQLString
    },
    hk: {
      type: g.GraphQLString
    },
    en: {
      type: g.GraphQLString
    },
    code: {
      type: g.GraphQLString
    },
    abbr: {
      type: g.GraphQLString
    }
  })
});

const countries = {
  type: new g.GraphQLList(countryType),
  resolve: (root) => {
    return db.getAll();
  }
};

module.exports = {
  types: {
    countryType
  },
  queries: {
    countries
  }
};
