const topic = {
  namespaced: true,
  state: {
    articles: [],
    date: '',
    keywords: [],
    nlp_kw: [],
    title: '',
    topic_summ: '',
  },
  mutations: {
    setCurrentTopic(state, newTopic) {
      state.articles = newTopic.articles;
      state.date = newTopic.date;
      state.keywords = newTopic.keywords;
      state.nlp_kw = newTopic.nlp_keywords.map(arr => arr[0]);
      state.title = newTopic.title;
      state.topic_summ = newTopic.topic_summ;
    },
  },
  getters: {},
  actions: {},
};

export default topic;
