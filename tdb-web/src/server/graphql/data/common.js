const g = require('graphql');

module.exports = {
  list(itemType) {
    return new g.GraphQLList(itemType);
  },
  nonNull(type) {
    return new g.GraphQLNonNull(type);
  },
  mutationResult(name, respType, flag = false) {
    const type = new g.GraphQLObjectType({
      name,
      fields: () => ({
        code: {
          type: g.GraphQLInt
        },
        message: {
          type: g.GraphQLString
        },
        result: {
          type: flag ? respType:(new g.GraphQLList(respType))
        }
      })
    });
    type.resolveBodyWithParser = (parser) => {
      return resp => resp.json().then(result => {
        const payload = {};
        payload['code'] = result.code || resp.status;
        payload['message'] = JSON.stringify(result.message);
        if (payload['code'] == 200) {
          payload['result'] = parser(result);
        }
        return payload;
      });
    };
    type.resolveBody = () => type.resolveBodyWithParser(r => r);
    return type;
  },
  paginationResult(name, objectsType) {
    const paginationType = new g.GraphQLObjectType({
      name,
      fields: () => ({
        objects: {
          type: new g.GraphQLList(objectsType)
        },
        page: {
          type: g.GraphQLInt
        },
        per_page: {
          type: g.GraphQLInt
        },
        total_count: {
          type: g.GraphQLInt
        },
        total_pages: {
          type: g.GraphQLInt
        },
      })
    });
    return paginationType;
  },
  resultCodeType: new g.GraphQLObjectType({
    name: 'ResultCode',
    fields: () => ({
      code: {
        type: g.GraphQLInt
      },
      message: {
        type: g.GraphQLString
      }
    })
  })
};
