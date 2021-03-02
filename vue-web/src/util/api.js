import axios from 'axios';

const baseURL = 'http://localhost:5000';

const baseAxios = axios.create({
  baseURL,
  responseType: 'json',
  mode: 'cors',
});

export const getFeedSources = () => {
  return baseAxios.get('/sources');
};

export const getBriefings = () => {
  return baseAxios.get('/briefings');
};

export const getTopics = (options) => {
  return baseAxios.get(`/topics?${options.join('')}`);
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

export const base = () => {
  return baseAxios;
};
