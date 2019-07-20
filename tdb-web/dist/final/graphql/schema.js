const g = require('graphql');
const data = require('./data');

const queryType = new g.GraphQLObjectType({
  name: 'Query',
  fields: () => data.query
});

const mutationType = new g.GraphQLObjectType({
  name: 'Mutation',
  fields: ()=> data.mutation
});

const schema = new g.GraphQLSchema({
  query: queryType,
  mutation: mutationType
});

module.exports = schema;
