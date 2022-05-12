import {
  getFeedSources,
  getRSSData,
} from '@/util/api';

const pipelines = {
  namespaced: true,
  state: {
    sources: [],
    feed_data: {},
  },
  mutations: {
    setSources(state, sources) {
      state.sources = sources;
    },
    setFeedData(state, payload) {
      console.log(state.feed_data);
      console.log(payload);
      // state.sources = sources;
    },
  },
  getters: {},
  actions: {
    getSources({ commit }) {
      return new Promise((resolve, reject) => {
        getFeedSources().then((results) => {
          /* eslint-disable no-param-reassign */
          const sources = results.data.sources.reduce((acc, curr) => {
            acc[curr.id] = curr;
            return acc;
          }, {});
          /* eslint-enable no-param-reassign */
          commit('setSources', sources);
          resolve(sources);
        }).catch(error => reject(error));
      });
    },
    getRSSData({ commit }, sourceIds) {
      return new Promise((resolve, reject) => {
        getRSSData(sourceIds).then((results) => {
          /* eslint-disable no-param-reassign */
          console.log(results);
          // const sources = results.data.sources.reduce((acc, curr) => {
          //   acc[curr.id] = curr;
          //   return acc;
          // }, {});
          // console.log(sources);
          // /* eslint-enable no-param-reassign */
          commit('setFeedData', results);
          resolve(results);
        }).catch(error => reject(error));
      });
    },
  },
};

export default pipelines;
