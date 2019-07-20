const g = require('graphql');
const api = require('../api');
const {resultCodeType, nonNull} = require('./common');

const authenticationResultType = new g.GraphQLObjectType({
  name: 'AuthenticationResult',
  fields: () => ({
    code: {
      type: g.GraphQLInt
    },
    message: {
      type: g.GraphQLString
    },
    token: {
      type: g.GraphQLString
    },
  })
});

const mobileRegisterInputType = new g.GraphQLInputObjectType({
  name: 'mobileRegisterInput',
  fields: () => ({
    mobile: {
      type: g.GraphQLString
    },
    name: {
      type: g.GraphQLString
    },
    pin_code: {
      type: g.GraphQLString
    },
    password: {
      type: g.GraphQLString
    },
    sponsor_uid: {
      type: g.GraphQLString
    },
    source: {
      type: g.GraphQLString
    },
    gender: {
      type: g.GraphQLString
    },
    active: {
      type: g.GraphQLString
    },
    nickname: {
      type: g.GraphQLString
    },
    country_code: {
      type: g.GraphQLString
    },
    uid: {
      type: g.GraphQLString
    },
    security_password: {
      type: g.GraphQLString
    },
    country_abbr: {
      type: g.GraphQLString
    }
  })
});

const sendSmsCode = {
  type: resultCodeType,
  args: {
    country_code: {
      type: g.GraphQLString
    },
    mobile: {
      type: nonNull(g.GraphQLString),
    }
  },
  resolve: (_, args) =>
    api.post('/sms_pin_code', null, args)
      .then(resp => resp.json().then(body => {
        const payload = {};
        payload.code = body.code || resp.status;
        payload['message'] = JSON.stringify(body.message);
        return payload;
      }))
};

const mobileRegister = {
  type: authenticationResultType,
  args: {
    mobileRegister: {
      type: nonNull(mobileRegisterInputType)
    }
  },
  resolve: (_, {mobileRegister}, ctx) =>
    api.post('/member/user/mobile_register', null, mobileRegister)
      .then(resp => resp.json().then(result => {
        const payload = {};
        payload['code'] = result.code || resp.status;
        payload['message'] = JSON.stringify(result.message);
        // if (payload['code'] == 200) {
        //   ctx.setToken(result.token);
        //   payload['token'] = result.token;
        // }
        return payload;
      }))
};

const loginInfoType = new g.GraphQLObjectType({
  name: 'loginInfo',
  fields: () => ({
    created_at: {
      type: g.GraphQLInt
    },
    client_ip: {
      type: g.GraphQLString
    },
    id: {
      type: g.GraphQLString
    }
  })
});

const loginInfos = {
  type: new g.GraphQLList(loginInfoType),
  args: {
    page: {
      type: g.GraphQLInt
    },
    per_page: {
      type: g.GraphQLInt
    }
  },
  resolve: (_, args, ctx) =>
    api.get('/member/login_info', ctx.with(args))
      .then(res => res.json())
      .then(body => body.objects)
};


module.exports = {
  mutations: {
    sendSmsCode,
    mobileRegister,
  },
  queries: {
    loginInfos
  }
};
