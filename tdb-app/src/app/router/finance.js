import Finance from 'app/components/finance/Index.vue';
import CommunityWallet from 'app/components/finance/CommunityWallet.vue';
import GeneralAsset from 'app/components/finance/GeneralAsset.vue';
import ExchangeAsset from 'app/components/finance/ExchangeAsset.vue';
import Exchange from 'app/components/finance/Exchange.vue';
import Transfer from 'app/components/finance/Transfer.vue';
import NodeProfit from 'app/components/finance/NodeProfit';
export default [
  {
    path: '/',
    name: 'Finance',
    component: Finance,
    meta: {
      requiresAuth: true,
      tab: 'finance'
    },
  },{
    path: '/finance/communitywallet',
    name: 'CommunityWallet',
    component: CommunityWallet,
    meta: {
      requiresAuth: true
    },
  },{
    path: '/finance/generalasset',
    name: 'GeneralAsset',
    component: GeneralAsset,
    meta: {
      requiresAuth: true
    },
  },{
    path: '/finance/exchangeasset',
    name: 'ExchangeAsset',
    component: ExchangeAsset,
    meta: {
      requiresAuth: true
    },
  },{
    path: '/finance/exchange',
    name: 'FinanceExchange',
    component: Exchange,
    meta: {
      requiresAuth: true
    },
  },{
    path: '/finance/transfer',
    name: 'FinanceTransfer',
    component: Transfer,
    meta: {
      requiresAuth: true
    },
  },{
    path: '/finance/node_profit',
    name: 'FinanceNodeProfit',
    component: NodeProfit,
    meta: {
      requiresAuth: true
    },
  }
];
