import axios from 'axios';

const baseURL = 'http://127.0.0.1:5000';
const memeAxios = axios.create({
  baseURL: 'https://api.imgflip.com',
  responseType: 'json',
});
const baseAxios = axios.create({
  baseURL,
  responseType: 'json',
  mode: 'no-cors',
});

export const getArticles = () => {
  return baseAxios.get('/articles');
};

export const getFeedSources = () => {
  return baseAxios.get('/sources');
};

export const getTopics = () => {
  return baseAxios.get('/summaries');
};

export const extractContent = (data) => {
  return baseAxios.post('/articles/extract', data);
};

export const getRSSData = (sourceIds, limit) => {
  const baseUrl = '/rss_data?';
  const sourceFilter = `${sourceIds.length > 0 ? `ids=${sourceIds}` : ''}`;
  const mid = `${sourceFilter.length > 0 ? '&' : ''}`;
  /* eslint-disable no-extra-boolean-cast */
  const limitFilter = `${!!limit ? `limit=${limit}` : ''}`;
  return baseAxios.get(`${baseUrl}${sourceFilter}${mid}${limitFilter}`);
};

export const getSummaryForURL = (url) => {
  return baseAxios.get(`/smmry?url=${url}`);
};

export const getContentSummary = (content) => {
  return baseAxios.post('/gensim-summary', { content });
};

export const createUser = (googleUser) => {
  return baseAxios.post('/create-user', {
    userId: googleUser,
  });
};

export const getUserProfile = (userId) => {
  return baseAxios.get(`/get-user-profile?user_id=${userId}`)
    .then(res => res.data.profile);
};

export const getTopicImage = (options) => {
  const reducedOptions = Object.entries(options).reduce((acc, curr) => {
    const outstr = `${acc}&${curr[0]}=${curr[1]}`;
    return outstr;
  }, '');
  return new Promise((resolve, reject) => {
    memeAxios.post(`/caption_image?${reducedOptions}`)
      .then((res) => {
        resolve(res.data);
      }).catch(err => reject(err));
  });
};

export const base = () => {
  return baseAxios;
};
