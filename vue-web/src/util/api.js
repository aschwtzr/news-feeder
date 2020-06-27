import axios from 'axios';

const baseURL = 'http://localhost:5000';

const baseAxios = axios.create({
  baseURL,
  responseType: 'json',
  mode: 'cors',
});

export const getFeedSources = () => {
  return baseAxios.get(`${baseURL}/sources`);
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

export const base = () => {
  return baseAxios;
};
