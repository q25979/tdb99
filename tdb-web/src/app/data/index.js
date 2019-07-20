import auth from './auth';
import country from './country';

const dataTypes = [
  auth,
  country
];

function merge() {
  return (all, item) => {
    const keys = Object.keys(item);
    let existedItem;
    for(let i=0; i<keys.length; i++) {
      if(keys[i] == all[i]) {
        existedItem = keys[i];
      }
    }
    if (existedItem) {
      throw new Error('duplicated item ' + existedItem);
    }
    return Object.assign(all, item);
  };
}

const data = dataTypes.reduce(merge(r => r), {});

export default data;
