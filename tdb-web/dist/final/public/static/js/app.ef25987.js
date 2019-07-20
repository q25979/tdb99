webpackJsonp([1],{135:function(e,t){},136:function(e,t){},164:function(e,t,o){"use strict";function r(e){return e&&e.__esModule?e:{default:e}}Object.defineProperty(t,"__esModule",{value:!0});var n=o(274),s=r(n),i=o(275),c=r(i),a=[s.default,c.default],u=a.reduce(function(){return function(e,t){for(var o=Object.keys(t),r=void 0,n=0;n<o.length;n++)o[n]==e[n]&&(r=o[n]);if(r)throw new Error("duplicated item "+r);return Object.assign(e,t)}}(),{});t.default=u},201:function(e,t){},202:function(e,t){},203:function(e,t){},248:function(e,t,o){"use strict";function r(e){return e&&e.__esModule?e:{default:e}}Object.defineProperty(t,"__esModule",{value:!0});var n=o(19),s=r(n),i=o(259),c=r(i),a=o(641),u=r(a),l=o(77),d=r(l),m={applyAfterware:function(e,t){var o=e.response;o.ok?o.clone().json().then(function(e){var o=e.errors,r=e.extensions;o&&r.authRequired&&d.default.unauth(),t()}):t()}},f=new c.default({networkInterface:(0,i.createNetworkInterface)({uri:"/graphql",transportBatching:!0,opts:{credentials:"same-origin"}}).useAfter([m])});s.default.use(u.default,{apolloClient:f}),t.default={apolloClient:f}},249:function(e,t,o){"use strict";function r(e){return e&&e.__esModule?e:{default:e}}Object.defineProperty(t,"__esModule",{value:!0});var n=o(19),s=r(n),i=o(654),c=r(i);s.default.use(c.default),t.default={}},250:function(e,t,o){"use strict";function r(e){return e&&e.__esModule?e:{default:e}}var n=o(19),s=r(n),i=o(246),c=r(i),a={locale:c.default.get("hl")};s.default.use(c.default),s.default.use(a)},251:function(e,t,o){"use strict";function r(e){return e&&e.__esModule?e:{default:e}}Object.defineProperty(t,"__esModule",{value:!0});var n=o(19),s=r(n),i=o(655),c=r(i),a=o(644),u=r(a),l=o(648),d=r(l),m=o(645),f=r(m),p=[{path:"",component:u.default,children:[{path:"/register/:id",name:"Register",component:d.default},{path:"/country_list/:id",name:"CountryList",component:f.default}]}];s.default.use(c.default);var _=new c.default({mode:"history",routes:p,scrollBehavior:function(){return{y:0}}});t.default=_},253:function(e,t){},254:function(e,t){},269:function(e,t,o){"use strict";Object.defineProperty(t,"__esModule",{value:!0}),t.default={data:function(){return{transitionName:"slide-left"}},watch:{$route:{handler:function(e,t){"Register"==e.name?this.transitionName="slide-right":this.transitionName="slide-left"}}}}},270:function(e,t,o){"use strict";function r(e){return e&&e.__esModule?e:{default:e}}Object.defineProperty(t,"__esModule",{value:!0});var n=o(202),s=(r(n),o(239)),i=r(s),c=o(203),a=(r(c),o(240)),u=r(a),l=o(135),d=(r(l),o(156)),m=r(d),f=o(136),p=(r(f),o(157)),_=r(p),g=o(67),h=(r(g),o(72)),y=r(h),b=o(164),v=r(b),k=o(77),w=r(k),$=o(59),C=r($),P=v.default.countries,L=C.default.localeList;t.default={data:function(){return{isShow:!1,store:w.default,search:"",countries:[],tempCountries:[]}},mounted:function(){this.getCountries()},computed:{currentData:{get:function(){return w.default.state.countrySelect},set:function(e){this.store.state.countrySelect=e}},activeLocale:{get:function(){return L.find(function(e){return e.value===C.default.locale})},set:function(e){}},currentLang:{get:function(){var e=this.activeLocale.value;return"zh_CN"==e?"cn":"zh_TW"==e?"hk":"en"}}},methods:{getCountries:function(){var e=this;this.$apollo.query({query:P}).then(function(t){var o=t.data;e.countries=o.countries,e.tempCountries=o.countries})},handleBack:function(){this.$router.push("/register/"+this.$route.params.id)},handleClick:function(e){this.currentData={code:e.code,abbr:e.abbr},this.$router.push("/register/"+this.$route.params.id)}},watch:{search:function(e){var t=this;this.countries=[],setTimeout(function(){t.countries=e?t.tempCountries.filter(function(o){return("(+"+o.code+")").indexOf(e)>=0||("en"==t.currentLang?o[t.currentLang].toLowerCase().indexOf(e.toLowerCase())>=0:o[t.currentLang].indexOf(e)>=0)}):t.tempCountries},100)}},components:{MtCell:y.default,MtField:_.default,MtButton:m.default,MtSearch:u.default,MtHeader:i.default}}},271:function(e,t,o){"use strict";function r(e){return e&&e.__esModule?e:{default:e}}Object.defineProperty(t,"__esModule",{value:!0});var n=o(136),s=(r(n),o(157)),i=r(s),c=o(67),a=(r(c),o(72)),u=r(a),l=o(77),d=r(l),m=o(59),f=r(m),p=f.default.localeList;t.default={props:["id"],data:function(){return{isShow:!1,store:d.default,search:"",countries:[],tempCountries:[]}},mounted:function(){},computed:{currentData:{get:function(){return d.default.state.countrySelect},set:function(e){this.store.state.countrySelect=e}},activeLocale:{get:function(){return p.find(function(e){return e.value===f.default.locale})},set:function(e){}},currentLang:{get:function(){var e=this.activeLocale.value;return"zh_CN"==e?"cn":"zh_TW"==e?"hk":"en"}},mobile:{get:function(){return d.default.state.mobile},set:function(e){this.store.state.mobile=e}}},methods:{toggleList:function(){this.$router.push("/country_list/"+this.id)}},components:{MtCell:u.default,MtField:i.default}}},272:function(e,t,o){"use strict";function r(e){return e&&e.__esModule?e:{default:e}}Object.defineProperty(t,"__esModule",{value:!0});var n=o(482),s=(r(n),o(627)),i=r(s),c=o(481),a=(r(c),o(626)),u=r(a),l=o(135),d=(r(l),o(156)),m=r(d),f=o(202),p=(r(f),o(239)),_=r(p),g=o(59),h=r(g),y=h.default.localeList;t.default={props:["showBack"],data:function(){return{picker:"",tempLang:"",isVisible:!1,slots:[{flex:1,values:["繁体中文","English","简体中文","日語","한국어"],className:"slot1",textAlign:"center"}]}},mounted:function(){var e=this.$cookie.get("hl")||h.default.locale;this.setLocale(e)},computed:{activeLocale:{get:function(){return y.find(function(e){return e.value===h.default.locale})},set:function(e){this.setLocale(e)}}},methods:{showPopup:function(){var e="";switch(this.activeLocale.value){case"en":e="English";break;case"zh_TW":e="繁体中文";break;case"zh_CN":e="简体中文";break;case"ko":e="한국어";break;case"ja":e="日語"}this.isVisible=!0,this.picker.setSlotValue(0,e)},setLocale:function(e){"string"==typeof e&&(e=y.find(function(t){return t.value===e})),e&&(h.default.locale=e.value,this.$cookie.set("hl",h.default.locale,365))},onValuesChange:function(e,t){var o=y.find(function(e){return e.name===t[0]});this.tempLang=o,this.picker=e},selectLang:function(){this.setLocale(this.tempLang),this.tempLang="",this.isVisible=!1}},components:{MtHeader:_.default,MtButton:m.default,MtPicker:u.default,MtPopup:i.default}}},273:function(e,t,o){"use strict";function r(e){return e&&e.__esModule?e:{default:e}}Object.defineProperty(t,"__esModule",{value:!0});var n=o(203),s=(r(n),o(240)),i=r(s),c=o(136),a=(r(c),o(157)),u=r(a),l=o(135),d=(r(l),o(156)),m=r(d),f=o(67),p=(r(f),o(72)),_=r(p),g=o(479),h=(r(g),o(624)),y=r(h),b=o(480),v=(r(b),o(625)),k=r(v),w=o(646),$=r(w),C=o(647),P=r(C),L=o(77),O=r(L),x=o(164),S=r(x),M=o(59),B=r(M),j=B.default.localeList,E=S.default.sendSmsCode,T=S.default.mobileRegister,R=/^\d+$/,z=/^[a-zA-Z0-9]*$/,A=/^\d{6}$/;t.default={data:function(){return{pinCode:"",loginPsd:"",reloginPsd:"",isSend:!1,time:60,sponsor:"",securityPsd:"",resecurityPsd:"",store:O.default}},mounted:function(){this.sponsor=this.$route.params.id},computed:{isFill:function(){return this.pinCode&&this.mobile&&this.loginPsd&&this.securityPsd&&this.reloginPsd&&this.resecurityPsd},isScroll:function(){return this.countryArr.length>3},sendText:function(){return this.$t("common.send_code")},countryCode:{get:function(){return this.store.state.countrySelect.code}},countryAbbr:{get:function(){return this.store.state.countrySelect.abbr}},activeLocale:{get:function(){return j.find(function(e){return e.value===B.default.locale})},set:function(e){}},mobile:{get:function(){return this.store.state.mobile}}},methods:{handleSubmit:function(){var e=this;return R.test(this.mobile)?z.test(this.pinCode)?this.loginPsd.length<6||this.loginPsd.length>20?((0,k.default)({message:this.$t("errors.valid_login_psd"),confirmButtonText:this.$t("common.ok")}),!1):this.reloginPsd!==this.loginPsd?((0,k.default)({message:this.$t("errors.psd_not_same"),confirmButtonText:this.$t("common.ok")}),!1):A.test(this.securityPsd)?this.resecurityPsd!==this.securityPsd?((0,k.default)({message:this.$t("errors.security_not_same"),confirmButtonText:this.$t("common.ok")}),!1):(y.default.open({text:this.$t("tips.registering"),spinnerType:"fading-circle"}),void this.$apollo.mutate({mutation:T,variables:{mobileRegister:{mobile:this.mobile,pin_code:this.pinCode,password:this.loginPsd,security_password:this.securityPsd,sponsor_uid:this.$route.params.id,country_code:this.countryCode,country_abbr:this.countryAbbr}}}).then(function(t){var o=t.data;y.default.close(),200==o.mobileRegister.code?(0,k.default)({message:e.$t("success.register_success"),confirmButtonText:e.$t("common.ok")}).then(function(){var e=document.createElement("a");e.setAttribute("href","http://download.lebo2019plus.com"),e.click()}):e.caseCode(o.mobileRegister.code)})):((0,k.default)({message:this.$t("tips.enter_security_password"),confirmButtonText:this.$t("common.ok")}),!1):((0,k.default)({message:this.$t("errors.pin_code.format_error"),confirmButtonText:this.$t("common.ok")}),!1):((0,k.default)({message:this.$t("errors.valid_mobile"),confirmButtonText:this.$t("common.ok")}),!1)},handleSend:function(){var e=this;return this.mobile?R.test(this.mobile)?void(0,k.default)({message:this.$t("tips.send_msg")+": +"+this.countryCode+" "+this.mobile,cancelButtonText:this.$t("common.cancel"),confirmButtonText:this.$t("common.ok"),showCancelButton:!0}).then(function(t){e.isSend||"confirm"!=t||(y.default.open({text:e.$t("common.sending"),spinnerType:"fading-circle"}),e.$apollo.mutate({mutation:E,variables:{country_code:"+"+e.countryCode,mobile:e.mobile}}).then(function(t){var o=t.data;if(y.default.close(),200==o.sendSmsCode.code){(0,k.default)({message:e.$t("tips.send_success"),confirmButtonText:e.$t("common.ok")}),e.isSend=!0;var r=setInterval(function(){--e.time<=0&&(clearInterval(r),e.isSend=!1,e.time=60)},1e3)}else(0,k.default)({message:e.$t("errors.system_error"),confirmButtonText:e.$t("common.ok")})}))}):((0,k.default)({message:this.$t("errors.valid_mobile"),confirmButtonText:this.$t("common.ok")}),!1):((0,k.default)({message:this.$t("tips.enter_mobile"),confirmButtonText:this.$t("common.ok")}),!1)},caseCode:function(e){var t="";switch(e){case 1002:t=this.$t("errors.register.sms_code_wrong");break;case 1005:t=this.$t("errors.register.sms_code_invalid");break;case 1011:t=this.$t("errors.mobile.has_registered",{mobile:this.mobile});break;case 1004:t=this.$t("errors.register.too_many_times");break;case 1001:t=this.$t("errors.register.link_invalid");break;default:t=this.$t("errors.system_error")}(0,k.default)({message:t,confirmButtonText:this.$t("common.ok")})}},watch:{},components:{MtCell:_.default,MtButton:m.default,MtField:u.default,MtSearch:i.default,LangSelect:P.default,CountrySelect:$.default}}},274:function(e,t,o){"use strict";function r(e,t){return Object.freeze(Object.defineProperties(e,{raw:{value:Object.freeze(t)}}))}Object.defineProperty(t,"__esModule",{value:!0});var n=r(["mutation sendSmsCode($country_code:String, $mobile: String!) {\n  sendSmsCode(country_code:$country_code, mobile: $mobile) {\n    code\n    message\n  }\n}"],["mutation sendSmsCode($country_code:String, $mobile: String!) {\n  sendSmsCode(country_code:$country_code, mobile: $mobile) {\n    code\n    message\n  }\n}"]),s=r(["mutation mobileRegister($mobileRegister: mobileRegisterInput!){\n  mobileRegister(mobileRegister: $mobileRegister) {\n    code\n    message\n  }\n}"],["mutation mobileRegister($mobileRegister: mobileRegisterInput!){\n  mobileRegister(mobileRegister: $mobileRegister) {\n    code\n    message\n  }\n}"]),i=o(205),c=function(e){return e&&e.__esModule?e:{default:e}}(i),a=(0,c.default)(n),u=(0,c.default)(s);t.default={sendSmsCode:a,mobileRegister:u}},275:function(e,t,o){"use strict";Object.defineProperty(t,"__esModule",{value:!0});var r=function(e,t){return Object.freeze(Object.defineProperties(e,{raw:{value:Object.freeze(t)}}))}(["query countries{\n  countries{\n    en\n    cn\n    hk\n    code\n    abbr\n  }\n}"],["query countries{\n  countries{\n    en\n    cn\n    hk\n    code\n    abbr\n  }\n}"]),n=o(205),s=function(e){return e&&e.__esModule?e:{default:e}}(n),i=(0,s.default)(r);t.default={countries:i}},276:function(e,t,o){"use strict";Object.defineProperty(t,"__esModule",{value:!0});var r=Object.assign||function(e){for(var t=1;t<arguments.length;t++){var o=arguments[t];for(var r in o)Object.prototype.hasOwnProperty.call(o,r)&&(e[r]=o[r])}return e},n=o(658),s=o(661),i=o(662),c=o(659),a=o(660),u=t.localeList=[{name:"简体中文",value:"zh_CN",messages:r({},s)},{name:"English",value:"en",messages:r({},n)},{name:"繁体中文",value:"zh_TW",messages:r({},i)},{name:"한국어",value:"ko",messages:r({},a)},{name:"日語",value:"ja",messages:r({},c)}];t.defaultLocale=u[0].value},277:function(e,t,o){"use strict";function r(e){return e&&e.__esModule?e:{default:e}}o(252);var n=o(19),s=r(n),i=o(251),c=r(i),a=o(249),u=r(a),l=o(59),d=r(l);o(250),o(248),o(254),o(253),s.default.config.productionTip=!1,new s.default({router:c.default,http:u.default,i18n:d.default}).$mount("#app")},479:function(e,t){},480:function(e,t){},481:function(e,t){},482:function(e,t){},483:function(e,t){},484:function(e,t){},485:function(e,t){},486:function(e,t){},487:function(e,t){},488:function(e,t){},59:function(e,t,o){"use strict";function r(e){return e&&e.__esModule?e:{default:e}}function n(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}function s(e,t){if(!e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return!t||"object"!=typeof t&&"function"!=typeof t?e:t}function i(e,t){if("function"!=typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function, not "+typeof t);e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,enumerable:!1,writable:!0,configurable:!0}}),t&&(Object.setPrototypeOf?Object.setPrototypeOf(e,t):e.__proto__=t)}Object.defineProperty(t,"__esModule",{value:!0});var c=function(){function e(e,t){for(var o=0;o<t.length;o++){var r=t[o];r.enumerable=r.enumerable||!1,r.configurable=!0,"value"in r&&(r.writable=!0),Object.defineProperty(e,r.key,r)}}return function(t,o,r){return o&&e(t.prototype,o),r&&e(t,r),t}}(),a=o(19),u=r(a),l=o(643),d=r(l),m=o(276),f=o(246),p=r(f),_=m.localeList.reduce(function(e,t){return e[t.value]=t.messages,e},{}),g=function(e){function t(){return n(this,t),s(this,(t.__proto__||Object.getPrototypeOf(t)).apply(this,arguments))}return i(t,e),c(t,[{key:"_initVM",value:function(e){var t=u.default.config.silent;u.default.config.silent=!0,this._vm=new u.default({data:e}),u.default.config.silent=t}},{key:"localeList",get:function(){return m.localeList}}]),t}(d.default);u.default.use(g);var h=new g({locale:m.localeList.find(function(e){return e.value==p.default.get("hl")})?p.default.get("hl"):m.defaultLocale,fallbackLocale:m.defaultLocale,messages:_});t.default=h},638:function(e,t,o){e.exports=o.p+"static/img/logo.4a48153.png"},644:function(e,t,o){o(488);var r=o(73)(o(269),o(653),null,null);e.exports=r.exports},645:function(e,t,o){o(484);var r=o(73)(o(270),o(649),null,null);e.exports=r.exports},646:function(e,t,o){o(487);var r=o(73)(o(271),o(652),null,null);e.exports=r.exports},647:function(e,t,o){o(486);var r=o(73)(o(272),o(651),null,null);e.exports=r.exports},648:function(e,t,o){o(485);var r=o(73)(o(273),o(650),null,null);e.exports=r.exports},649:function(e,t){e.exports={render:function(){var e=this,t=e.$createElement,o=e._self._c||t;return o("div",{staticClass:"country-list"},[o("div",{staticClass:"country-header"},[o("mt-header",{attrs:{title:e.$t("common.search")}},[o("mt-button",{attrs:{slot:"left",icon:"back"},nativeOn:{click:function(t){return e.handleBack(t)}},slot:"left"})],1),e._v(" "),o("mt-search",{attrs:{"cancel-text":e.$t("common.cancel"),placeholder:e.$t("common.search")},model:{value:e.search,callback:function(t){e.search=t},expression:"search"}})],1),e._v(" "),o("div",{staticClass:"country-content"},e._l(e.countries,function(t,r){return o("mt-cell",{key:r,attrs:{title:t[e.currentLang]+" (+"+t.code+")","is-link":""},nativeOn:{click:function(o){return e.handleClick(t)}}})}),1)])},staticRenderFns:[]}},650:function(e,t,o){e.exports={render:function(){var e=this,t=e.$createElement,o=e._self._c||t;return o("div",{staticClass:"register"},[o("lang-select"),e._v(" "),o("div",{staticClass:"mobile-form"},[e._m(0),e._v(" "),o("country-select",{attrs:{id:e.sponsor}}),e._v(" "),o("mt-field",{attrs:{label:e.$t("common.code"),placeholder:e.$t("tips.enter_code")},model:{value:e.pinCode,callback:function(t){e.pinCode=t},expression:"pinCode"}},[e.isSend?o("mt-button",{staticClass:"send-btn",attrs:{plain:!0}},[e._v("\n        "+e._s(e.$t("common.resend"))+"("+e._s(e.time)+"s)\n      ")]):o("mt-button",{staticClass:"send-btn",attrs:{plain:!0},nativeOn:{click:function(t){return e.handleSend(t)}}},[e._v("\n        "+e._s(e.sendText)+"\n      ")])],1),e._v(" "),o("mt-field",{attrs:{label:e.$t("common.login_psd"),placeholder:e.$t("tips.enter_password"),type:"password"},model:{value:e.loginPsd,callback:function(t){e.loginPsd=t},expression:"loginPsd"}}),e._v(" "),o("mt-field",{attrs:{label:e.$t("common.repsd"),placeholder:e.$t("tips.enter_repsd"),type:"password"},model:{value:e.reloginPsd,callback:function(t){e.reloginPsd=t},expression:"reloginPsd"}}),e._v(" "),o("mt-field",{attrs:{label:e.$t("common.security_psd"),placeholder:e.$t("tips.enter_security_password"),type:"password"},model:{value:e.securityPsd,callback:function(t){e.securityPsd=t},expression:"securityPsd"}}),e._v(" "),o("mt-field",{attrs:{label:e.$t("common.resecurity"),placeholder:e.$t("tips.enter_resecurity"),type:"password"},model:{value:e.resecurityPsd,callback:function(t){e.resecurityPsd=t},expression:"resecurityPsd"}}),e._v(" "),o("mt-field",{attrs:{label:e.$t("common.sponsor"),disabled:""},model:{value:e.sponsor,callback:function(t){e.sponsor=t},expression:"sponsor"}})],1),e._v(" "),o("div",{staticClass:"submit-button"},[o("div",[o("mt-button",{attrs:{type:"primary",disabled:!e.isFill},nativeOn:{click:function(t){return e.handleSubmit(t)}}},[e._v(e._s(e.$t("common.sign_up")))])],1),e._v(" "),o("div",[o("a",{attrs:{href:"http://download.lebo2019plus.com"}},[e._v(e._s(e.$t("tips.download")))])])])],1)},staticRenderFns:[function(){var e=this,t=e.$createElement,r=e._self._c||t;return r("div",{staticClass:"logo"},[r("div",{staticClass:"img"},[r("img",{attrs:{src:o(638),alt:""}})]),e._v(" "),r("div",{staticClass:"text"},[e._v("\n        LEBO\n      ")])])}]}},651:function(e,t){e.exports={render:function(){var e=this,t=e.$createElement,o=e._self._c||t;return o("div",[o("mt-header",{attrs:{title:" "}},[o("mt-button",{staticClass:"lang-title",attrs:{slot:"right"},nativeOn:{click:function(t){return e.showPopup(t)}},slot:"right"},[e._v("\n      "+e._s(e.activeLocale.name)+"\n    ")])],1),e._v(" "),o("mt-popup",{ref:"popup",attrs:{position:"bottom"},model:{value:e.isVisible,callback:function(t){e.isVisible=t},expression:"isVisible"}},[o("div",{staticClass:"btn"},[o("mt-button",{attrs:{plain:!0},nativeOn:{click:function(t){return e.selectLang(t)}}},[e._v("\n        "+e._s(e.$t("common.sure"))+"\n      ")])],1),e._v(" "),o("mt-picker",{attrs:{slots:e.slots},on:{change:e.onValuesChange}})],1)],1)},staticRenderFns:[]}},652:function(e,t){e.exports={render:function(){var e=this,t=e.$createElement,o=e._self._c||t;return o("div",{staticClass:"country-select"},[o("div",{staticClass:"mobile-input"},[o("mt-field",{attrs:{label:" ",type:"tel",placeholder:e.$t("tips.enter_mobile")},model:{value:e.mobile,callback:function(t){e.mobile=t},expression:"mobile"}}),e._v(" "),o("div",{staticClass:"country-code",on:{click:e.toggleList}},[o("span",[e._v("+"+e._s(e.currentData.code))]),e._v(" "),o("i",{staticClass:"arrow-icon"})])],1)])},staticRenderFns:[]}},653:function(e,t){e.exports={render:function(){var e=this,t=e.$createElement,o=e._self._c||t;return o("div",{staticClass:"app"},[o("transition",{attrs:{name:e.transitionName}},[o("router-view",{staticClass:"child-view"})],1)],1)},staticRenderFns:[]}},658:function(e,t){e.exports={"common.title":"Register","common.back":"Back","common.sure":"Sure","common.code":"Verification Code","common.mobile":"Mobile","common.username":"User Name","common.login_psd":"Password","common.sign_up":"Sign up","common.send_code":"Send Code","common.sending":"Sending...","common.resend":"Resend","common.cancel":"Cancel","common.sponsor":"Invitation Code","tips.enter_mobile":"Please enter mobile","tips.enter_code":"Enter code","tips.enter_username":"Please enter user name","tips.enter_password":"Enter 6 ~ 20 password ","tips.send_success":"Send successfully","tips.register_success":"Congratulations! Registration successful","tips.download":"Download LEBO","tips.download_btn":"Download LEBO APP","tips.registering":"Registering...","errors.valid_mobile":"Please enter a valid phone number","errors.pin_code":"Please enter verification code","errors.valid_login_psd":"Password must be 6 to 20 characters long ","errors.system_error":"System error, please try again later","errors.register.sms_code_wrong":"Incorrect verification code","errors.register.too_many_times":"Verification code try too many times. Please try again later","errors.register.sms_code_invalid":"The verification code is no longer valid. Please try again later","errors.register.has_registered":"The mobile or username has been registered","errors.register.link_invalid":"The link is invalid, please re-scan qr code","errors.pin_code.format_error":"Verification code format error","country.cn":"China","country.us":"United States","country.uk":"United Kingdom","country.hk":"Hong Kong","country.mo":"Macao","country.kr":"Korea","country.jp":"Japan","country.ph":"Philippines","country.th":"Thailand","country.au":"Australia","country.lb":"Lebanon","country.sy":"Syria","country.sgp":"Singapore","errors.mobile.has_registered":"Account number {mobile} already exists, There’s no need to sign up again.","errors.invalid_country_code":"The phone number does not exist, please try again.","errors.send_pin_code_more":"Too many operations.Try again later","common.ok":"OK","country.mys":"Malaysia","common.search":"Search","common.area":"Country/Region","success.register_success":"Registration successful, click to download LEBO","tips.send_msg":"We will send a verification code to the following number","common.security_psd":"Security Password","tips.enter_security_password":"Enter 6 digital security password","common.repsd":"Confirm Login Password","tips.enter_repsd":"Enter login password again","common.resecurity":"Confirm Security Password","tips.enter_resecurity":"Enter security password again","errors.psd_not_same":"Login password is not same","errors.security_not_same":"Security password is not same"}},659:function(e,t){e.exports={"common.title":"登録","common.back":"裏","common.sure":"確認","common.code":"検証コード","common.mobile":"モバイル","common.username":"ユーザー名","common.login_psd":"パスワード","common.sign_up":"登録","common.send_code":"送信コード","common.sending":"送信...","common.resend":"再送信","common.cancel":"消","common.sponsor":"招待コード","tips.enter_mobile":"ご入力くださいモバイル","tips.enter_code":"入力コード","tips.enter_username":"ご入力くださいユーザー名","tips.enter_password":"入力は6～20パスワード ","tips.send_success":"送信に成功","tips.register_success":"おめでとうございます！ 登録に成功","tips.download":"ダウンロードLEBO","tips.download_btn":"ダウンロードLEBOアプリ","tips.registering":"登録の---","errors.valid_mobile":"ご入力ください有効な電話番号","errors.pin_code":"認証コードをご入力ください","errors.valid_login_psd":"パスワードは6文字数が20文字長 ","errors.system_error":"システムエラーは、後ほど再度お試しください。","errors.register.sms_code_wrong":"誤った検証コード","errors.register.too_many_times":"検証コードしました。 後ほど再度お試しください。","errors.register.sms_code_invalid":"検証コードは有効ではなくなっている。 後ほど再度お試しください。","errors.register.has_registered":"モバイルまたはユーザー名で登録されてい","errors.register.link_invalid":"のリンクが無効になってください再スキャンのqrコード","errors.pin_code.format_error":"認証コードをフォーマットエラー","country.cn":"中国","country.us":"米国","country.uk":"英国","country.hk":"香港","country.mo":"マカオ","country.kr":"韓国","country.jp":"日本","country.ph":"フィリピン","country.th":"タイ","country.au":"豪州","country.lb":"レバノン","country.sy":"シリア","country.sgp":"シンガポール","errors.mobile.has_registered":"口座番号{モバイル}には、既に存在する必要はありませんサインです。","errors.invalid_country_code":"の電話番号が存在しない、もう一度入力してください。","errors.send_pin_code_more":"多すぎます。後で再試行せよ","common.ok":"OK","country.mys":"マレーシア","common.search":"検索","common.area":"国-地域","success.register_success":"登録に成功すると、クリックでダウンロードLEBO","tips.send_msg":"をお送りいたします検証コードは以下の番号","common.security_psd":"安全保障のパスワード","tips.enter_security_password":"入力する6でデジタルセキュリティパスワード","common.repsd":"確認ログインパスワード","tips.enter_repsd":"入力ログインパスワードを再","common.resecurity":"確認-安全保障のパスワード","tips.enter_resecurity":"パスワードを再度入","errors.psd_not_same":"ログインパスワードは異なっていても問題ないで","errors.security_not_same":"安全保障のパスワードは異なっていても問題ないで"}},660:function(e,t){e.exports={"common.title":"등록","common.back":"시","common.sure":"확인","common.code":"검증 코드","common.mobile":"모바일","common.username":"사용자 이름","common.login_psd":"비밀번호","common.sign_up":"Sign up","common.send_code":"을 보낼 코드","common.sending":"을 보내...","common.resend":"재발송","common.cancel":"취소","common.sponsor":"초대 코드","tips.enter_mobile":"를 입력하세요일","tips.enter_code":"코드 입력","tips.enter_username":"사용자 이름을 입력하십시오","tips.enter_password":"입력 6~20 비밀번호 ","tips.send_success":"보내는 성공적으로","tips.register_success":"축하합니다! 성공하는 등록","tips.download":"다운로드 LEBO","tips.download_btn":"다운로드 LEBO 램","tips.registering":"등록하기...","errors.valid_mobile":"를 입력해 주시 유효한 전화 번호","errors.pin_code":"를 입력해 주시 확인 코드","errors.valid_login_psd":"비밀번호는 6~20 자 ","errors.system_error":"시스템 오류가,나중에 다시 시도하십시오","errors.register.sms_code_wrong":"잘못된 코드 검증","errors.register.too_many_times":"인증 코드를 시도 너무 많은 시간입니다. 나중에 다시 시도하십시오","errors.register.sms_code_invalid":"인증 코드가 더 이상 유효하지 않습니다. 나중에 다시 시도하십시오","errors.register.has_registered":"모바일 또는 사용자 이름 등록","errors.register.link_invalid":"링크에 잘못된,다시 qr 코드를 스캔","errors.pin_code.format_error":"검증 코드 형식의 오류","country.cn":"중국","country.us":"United States","country.uk":"United Kingdom","country.hk":"홍콩","country.mo":"마카오","country.kr":"대한민국","country.jp":"일본","country.ph":"필리핀","country.th":"태국","country.au":"호주","country.lb":"레바논","country.sy":"시리아","country.sgp":"싱가포르","errors.mobile.has_registered":"계좌번호{모바일}이미 존재하는 필요가 없을 등록하시합니다.","errors.invalid_country_code":"전화 번호 존재하지 않는,다시 시도해 주시기 바랍니다.","errors.send_pin_code_more":"너무 많은 작업입니다.나중에 다시 시도하십시오","common.ok":"OK","country.mys":"말레이시아","common.search":"검색","common.area":"국가/지역","success.register_success":"등록이 성공을 클릭하여 다운로드 LEBO","tips.send_msg":"우리는 보낼 것이로 인증 코드가 다음 번호","common.security_psd":"보안 비밀번호","tips.enter_security_password":"입력 6 디지털 보안 비밀번호","common.repsd":"로그인 비밀번호 확인","tips.enter_repsd":"입력한 암호를 다시 로그인","common.resecurity":"인 보안 비밀번호","tips.enter_resecurity":"비밀번호를 다시 입력하라","errors.psd_not_same":"로그인 비밀번호와 동일하지 않습니다","errors.security_not_same":"보안 암호와 동일하지 않습니다"}},661:function(e,t){e.exports={"common.title":"注册","common.back":"返回","common.sure":"确定","common.code":"验证码","common.mobile":"手机号","common.username":"用户名","common.login_psd":"登录密码","common.sign_up":"注册","common.send_code":"发送验证码","common.sending":"正在发送...","common.resend":"重新发送","common.cancel":"取消","common.sponsor":"邀请码","tips.enter_mobile":"请输入手机号","tips.enter_code":"输入验证码","tips.enter_username":"请输入用户名","tips.enter_password":"请输入6~20位的密码","tips.send_success":"成功发送验证码","tips.register_success":"恭喜您，注册成功","tips.download":"下载 LEBO","tips.download_btn":"下载 LEBO APP","tips.registering":"注册中...","errors.pin_code":"请输入验证码","errors.valid_mobile":"请输入正确的手机号","errors.valid_login_psd":"密码长度必须是6-20字符,请再次输入密码","errors.system_error":"服务器繁忙，请稍后重试","errors.register.sms_code_wrong":"验证码错误","errors.register.too_many_times":"验证码尝试次数过多，请稍后重试","errors.register.sms_code_invalid":"验证码已失效，请稍后重试","errors.register.has_registered":"该手机号或者用户名已被注册","errors.register.link_invalid":"链接无效，请重新扫描二维码","errors.pin_code.format_error":"验证码格式错误","country.cn":"中国","country.us":"美国","country.uk":"英国","country.hk":"香港","country.mo":"澳门","country.kr":"韩国","country.jp":"日本","country.ph":"菲律宾","country.th":"泰国","country.au":"澳大利亚","country.lb":"黎巴嫩","country.sy":"叙利亚","country.sgp":"新加坡","errors.mobile.has_registered":"手机号 {mobile} 已存在，无需重复注册","errors.invalid_country_code":"请输入正确的电话区号，并输入正确的手机号码","errors.send_pin_code_more":"一个小时最多获取6次验证码，稍候再试","common.ok":"知道了","country.mys":"马来西亚","common.search":"搜索","common.area":"国家/地区","success.register_success":"注册成功，点击前往下载 LEBO","tips.send_msg":"我们将发送验证码短信到这个号码","common.security_psd":"交易密码","tips.enter_security_password":"请输入6位纯数字交易密码","common.repsd":"确认登录密码","tips.enter_repsd":"请再次输入登录密码","common.resecurity":"确认交易密码","tips.enter_resecurity":"请再次输入交易密码","errors.psd_not_same":"两次输入的登录密码不一致","errors.security_not_same":"两次输入的交易密码不一致"}},662:function(e,t){e.exports={"common.title":"註冊","common.back":"返回","common.sure":"確定","common.code":"驗證碼","common.mobile":"手機號","common.username":"用戶名","common.login_psd":"登錄密碼","common.sign_up":"註冊","common.send_code":"發送驗證碼","common.sending":"正在發送...","common.resend":"重新發送","common.cancel":"取消","common.sponsor":"邀請碼","tips.enter_mobile":"請輸入手機號","tips.enter_code":"輸入驗證碼","tips.enter_username":"請輸入用戶名","tips.enter_password":"請輸入6~20位的密碼","tips.send_success":"成功發送驗證碼","tips.register_success":"恭喜您，註冊成功","tips.download":"下載 LEBO","tips.download_btn":"下載 LEBO APP","tips.registering":"註冊中...","errors.pin_code":"請輸入驗證碼","errors.valid_mobile":"請輸入正確的手機號","errors.valid_login_psd":"密碼長度必須是6-20字符,請再次輸入密碼","errors.system_error":"服務器繁忙，請稍後重試","errors.register.sms_code_wrong":"驗證碼錯誤","errors.register.too_many_times":"驗證碼嘗試次數過多，請稍後重試","errors.register.sms_code_invalid":"驗證碼已失效，請稍後重試","errors.register.has_registered":"該手機號或者用戶名已被註冊","errors.register.link_invalid":"鏈接無效，請重新掃描二維碼","errors.pin_code.format_error":"驗證碼格式錯誤","country.cn":"中國","country.us":"美國","country.uk":"英國","country.hk":"香港","country.mo":"澳門","country.kr":"韓國","country.jp":"日本","country.ph":"菲律賓","country.th":"泰國","country.au":"澳大利亞","country.lb":"黎巴嫩","country.sy":"敘利亞","country.sgp":"新加坡","errors.mobile.has_registered":"手機號 {mobile} 已存在，無需重複註冊","errors.invalid_country_code":"請輸入正確的電話區號，並輸入正確的手機號碼","errors.send_pin_code_more":"一個小時最多獲取6次驗證碼，稍候再試","common.ok":"知道了","country.mys":"馬來西亞","common.search":"搜索","common.area":"國家/地區","success.register_success":"註冊成功，點擊前往下載 LEBO","tips.send_msg":"我們將發送驗證碼短信到這個號碼","common.security_psd":"交易密碼","tips.enter_security_password":"請輸入6位純數字交易密碼","common.repsd":"確認登錄密碼","tips.enter_repsd":"請再次輸入登錄密碼","common.resecurity":"確認交易密碼","tips.enter_resecurity":"請再次輸入交易密碼","errors.psd_not_same":"兩次輸入的登錄密碼不一致","errors.security_not_same":"兩次輸入的交易密碼不一致"}},663:function(e,t){},67:function(e,t){},77:function(e,t,o){"use strict";Object.defineProperty(t,"__esModule",{value:!0});var r=o(19),n=function(e){return e&&e.__esModule?e:{default:e}}(r),s={bus:new n.default,state:{countrySelect:{code:"86",abbr:"CN"},mobile:""}};t.default=s}},[277]);
//# sourceMappingURL=app.ef25987.js.map