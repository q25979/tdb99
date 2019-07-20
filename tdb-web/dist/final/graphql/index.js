const graphqlHTTP = require('express-graphql');
const schema = require('./schema');
const {ApiError} = require('./api');

module.exports = graphqlHTTP((req, res) => {
  const token = req.cookies && req.cookies.token;
  return {
    schema: schema,
    graphiql: true,
    extensions({document, variables, operationName, result}) {
      let ext = {};
      if (result.errors) {
        result.errors.forEach(err => {
          if (err.originalError instanceof ApiError) {
            const apiError = err.originalError;
            const {authRequired, apiStatus, cause} = apiError;
            ext = Object.assign(ext, {
              authRequired,
              apiStatus,
              cause
            });
          }
        });
      }
      return ext;
    },
    context: {
      req,
      res,
      token,
      setToken(token) {
        const expires = new Date();
        expires.setDate(expires.getDate() + (token ? 30 : 0));
        res.cookie('token', token, {
          expires
        });
      },
      with(params) {
        return Object.assign({token}, params);
      }
    }
  };
});

