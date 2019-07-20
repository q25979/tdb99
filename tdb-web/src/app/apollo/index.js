import Vue from 'vue';
import ApolloClient, {createNetworkInterface} from 'apollo-client';
import VueApollo from 'vue-apollo';

import store from '../store';

const handleErrors = {
  applyAfterware({response}, next) {
    if (response.ok) {
      response.clone().json().then(({errors, extensions}) => {
        if (errors) {
          if(extensions.authRequired) {
            store.unauth();
          }
        }
        next();
      });
    } else {
      next();
    }
  }
};

// Create the apollo client
const apolloClient = new ApolloClient({
  networkInterface: createNetworkInterface({
    uri: '/graphql',
    transportBatching: true,
    opts: {
      credentials: 'same-origin'
    }
  }).useAfter([handleErrors])
});

Vue.use(VueApollo, {
  apolloClient
});

export default {
  apolloClient
};
