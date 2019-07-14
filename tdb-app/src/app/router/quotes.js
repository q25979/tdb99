import Quotes from 'app/components/quotes/Quotes.vue';

export default [
  {
    path: '/quotes/list',
    name: 'QuotesList',
    component: Quotes,
    meta: {
      requiresAuth: true,
      tab: 'quotes'
    },
  },
];
