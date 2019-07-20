import gql from 'graphql-tag';

const countries = gql`query countries{
  countries{
    en
    cn
    hk
    code
    abbr
  }
}`;

export default {
  countries
};
