import axios from "axios";

const baseURL = "http://localhost:5000"

const baseAxios = axios.create({
  baseURL,
  responseType: "json"
})
 
export const fetchNewsSources = function () {
  return baseAxios.get(`${baseURL}/sources`)
}

export const getBriefings = function () {
  return baseAxios.get('/headlines')
}

export const base = function () {
  return baseAxios
}
