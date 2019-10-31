import axios from 'axios';

const baseURL = 'http://localhost:5000';

const baseAxios = axios.create({
  baseURL,
  responseType: 'json',
});

export const getFeedSources = () => {
  return baseAxios.get(`${baseURL}/sources`);
};

export const getBriefings = () => {
  return baseAxios.get('/briefings');
};

export const getGoogleFeed = () => {
  return baseAxios.get('/google-news');
};

export const getSummaryForURL = (url) => {
  return baseAxios.get(`/smmry?url=${url}`);
};

export const getContentSummary = (content) => {
  return baseAxios.post('/gensim-summary', { content });
};

export const base = () => {
  return baseAxios;
};
