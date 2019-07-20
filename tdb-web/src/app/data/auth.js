import gql from 'graphql-tag';

const sendSmsCode = gql`mutation sendSmsCode($country_code:String, $mobile: String!) {
  sendSmsCode(country_code:$country_code, mobile: $mobile) {
    code
    message
  }
}`;

const mobileRegister = gql`mutation mobileRegister($mobileRegister: mobileRegisterInput!){
  mobileRegister(mobileRegister: $mobileRegister) {
    code
    message
  }
}`;

export default {
  sendSmsCode,
  mobileRegister,
};
