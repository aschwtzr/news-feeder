import {
  getFeedSources,
  getRSSData,
} from '@/util/api';

const pipelines = {
  namespaced: true,
  state: {
    sources: [],
    rawData: [],
    feedData: {},
  },
  mutations: {
    setSources(state, sources) {
      state.sources = sources;
    },
    setFeedData(state, data) {
      state.rawData = data;
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
    getRSSData({ commit }, payload) {
      return new Promise((resolve, reject) => {
        getRSSData(payload.sourceIds, payload.limit).then((results) => {
          /* eslint-disable no-param-reassign */
          console.log(results.data.raw_data);
          // const sources = results.data.sources.reduce((acc, curr) => {
          //   acc[curr.id] = curr;
          //   return acc;
          // }, {});
          // console.log(sources);
          // /* eslint-enable no-param-reassign */
          commit('setFeedData', results.data.raw_data);
          resolve(results);
        }).catch(error => reject(error));
      });
    },
  },
};

export default pipelines;
