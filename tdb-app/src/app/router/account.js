import Account from 'app/components/account/Index.vue';
import Profile from 'app/components/account/Profile.vue';
import ProfileNickname from 'app/components/account/profile/Nickname.vue';
import ProfileAvatar from 'app/components/account/profile/Avatar.vue';
import ProfileName from 'app/components/account/profile/Name.vue';
import ProfileWechat from 'app/components/account/profile/Wechat.vue';
import ProfileGender from 'app/components/account/profile/Gender.vue';
import Invite from 'app/components/account/Invite.vue';
import Friend from 'app/components/account/Friend.vue';
import Setting from 'app/components/account/Setting.vue';
import Contact from 'app/components/account/Contact.vue';
import SettingLang from 'app/components/account/setting/Lang.vue';
import SettingPassword from 'app/components/account/setting/Password.vue';
import SettingSecurity from 'app/components/account/setting/Security.vue';
import SettingMobile from 'app/components/account/setting/Mobile.vue';
import Receivable from 'app/components/account/Receivable.vue';
import ReceiveWay from 'app/components/account/ReceiveWay.vue';
import News from 'app/components/account/News.vue';
import AddBank from 'app/components/account/receivable/AddBank.vue';
import AddWeixin from 'app/components/account/receivable/AddWeixin.vue';
import AddAlipay from 'app/components/account/receivable/AddAlipay.vue';
import AddUSDT from 'app/components/account/receivable/AddUSDT.vue';
import NewsDetail from 'app/components/account/NewsDetail.vue';
export default [
  {
    path: '/account',
    name: 'Account',
    component: Account,
    meta: {
      requiresAuth: true,
      tab: 'account'
    },
  },
  {
    path: '/account/profile',
    name: 'AccountProfile',
    component: Profile,
    meta: {requiresAuth: true}
  },
  {
    path: '/account/profile/nickname',
    name: 'AccountProfileNickname',
    component: ProfileNickname,
    meta: {requiresAuth: true}
  },
  {
    path: '/account/profile/gender',
    name: 'AccountProfileGender',
    component: ProfileGender,
    meta: {requiresAuth: true}
  },
  {
    path: '/account/profile/name',
    name: 'AccountProfileName',
    component: ProfileName,
    meta: {requiresAuth: true}
  },
  {
    path: '/account/profile/wechat',
    name: 'AccountProfileWechat',
    component: ProfileWechat,
    meta: {requiresAuth: true}
  },
  {
    path: '/account/profile/avatar',
    name: 'AccountProfileAvatar',
    component: ProfileAvatar,
    meta: {requiresAuth: true}
  },
  {
    path: '/account/invite',
    name: 'AccountInvite',
    component: Invite,
    meta: {requiresAuth: true}
  },
  {
    path: '/account/friend',
    name: 'AccountFriend',
    component: Friend,
    meta: {requiresAuth: true}
  },
  {
    path: '/account/setting',
    name: 'AccountSetting',
    component: Setting,
    meta: {requiresAuth: true}
  },
  {
    path: '/account/contact',
    name: 'AccountContact',
    component: Contact,
    meta: {
      requiresAuth: true
    }
  },
  {
    path: '/account/setting/lang',
    name: 'AccountSettingLang',
    component: SettingLang,
  },
  {
    path: '/account/setting/mobile',
    name: 'AccountSettingMobile',
    component: SettingMobile,
  },
  {
    path: '/account/setting/password',
    name: 'AccountSettingPassword',
    component: SettingPassword,
    meta: {requiresAuth: true}
  },
  {
    path: '/account/setting/security',
    name: 'AccountSettingSecurity',
    component: SettingSecurity,
    meta: {requiresAuth: true}
  },
  {
    path: '/account/receivable',
    name: 'AccountReceivable',
    component: Receivable,
    meta: {requiresAuth: true}
  },
  {
    path: '/account/receiveway',
    name: 'AccountReceiveWay',
    component: ReceiveWay,
    meta: {requiresAuth: true}
  },{
    path: '/account/receiveway/addbank',
    name: 'AccountReceiveWayAddBank',
    component: AddBank,
    meta: {requiresAuth: true}
  },
  {
    path: '/account/receiveway/addalipay',
    name: 'AccountReceiveWayAddAlipay',
    component: AddAlipay,
    meta: {requiresAuth: true}
  },{
    path: '/account/receiveway/addweixin',
    name: 'AccountReceiveWayAddWeixin',
    component: AddWeixin,
    meta: {requiresAuth: true}
  },{
    path: '/account/receiveway/addusdt',
    name: 'AccountReceiveWayAddUSDT',
    component: AddUSDT,
    meta: {requiresAuth: true}
  },
  {
    path: '/account/news',
    name: 'AccountNews',
    component: News,
    meta: {requiresAuth: true}
  },
  {
    path: '/account/news_detail',
    name: 'AccountNewsDetail',
    component: NewsDetail,
    meta: {requiresAuth: true}
  }
];
