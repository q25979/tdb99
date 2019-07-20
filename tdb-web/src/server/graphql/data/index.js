const dataTypes = [
  'auth',
  'country'
].map((name) => require('./' + name));

function merge(itemResolver) {
  return (all, item) => {
    const values = itemResolver(item);
    if (!values) {
      return all;
    }
    const existedItem = Object.keys(values).find(v => all[v]);
    if (existedItem) {
      throw new Error('duplicated item ' + existedItem);
    }
    return Object.assign(all, values);
  };
}

module.exports = {
  query: dataTypes.reduce(merge(r => r.queries), {}),
  mutation: dataTypes.reduce(merge(r => r.mutations), {})
};
