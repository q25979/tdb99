import Exchange from 'app/components/exchange/Index.vue';
import Order from 'app/components/exchange/Order.vue';
import Details from 'app/components/exchange/Details.vue';
export default [
  {
    path: '/exchange',
    name: 'Exchange',
    component: Exchange,
    meta: {
      requiresAuth: true,
      tab: 'exchange'
    },
  },
  {
    path: '/exchange/order',
    name: 'Order',
    component: Order,
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: '/exchange/details/:type/:number',
    name: 'OrderDetail',
    component: Details,
    meta: {
      requiresAuth: true,
    },
  },
];
