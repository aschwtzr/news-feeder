import { getBriefings } from "../utils/Api";

const Types = {
  SAVE_ARTICLE: "SAVE_ARTICLE",
  SUMMARIZE_WITH_URL: "SUMMARIZE_WITH_URL",
  INCREASE_COUNT: "INCREASE_COUNT",
  REQUEST_NEWS_FEED: "REQUEST_NEWS_FEED",
  RECEIVE_NEWS_FEED: "RECEIVE_NEWS_FEED",
  FEED_FETCH_FAILURE: "FEED_FETCH_FAILURE",
  FETCH_RSS_FEED: "FETCH_RSS_FEED",
  CLEAR_RSS_FEED: "CLEAR_RSS_FEED",
};

const addToSavedList = article => ({
  type: Types.SAVE_ARTICLE,
  payload: article,
});

const summarizeWithURL = url => ({
  type: Types.SUMMARIZE_WITH_URL,
  payload: url,
});

const increaseCount = () => ({
  type: Types.INCREASE_COUNT,
})

const requestNewsFeed = () => ({
  type: Types.REQUEST_NEWS_FEED,
});

const receiveNewsFeed = briefings => ({
  type: Types.RECEIVE_NEWS_FEED,
  payload: briefings,
});

const feedFetchFailure = error => ({
  type: Types.FEED_FETCH_FAILURE,
  payload: error,
});

const fetchRSSFeed = () => ({
  type: Types.FEED_FETCH_FAILURE,
});


const clearRSSFeed = () => ({
  type: Types.CLEAR_RSS_FEED,
});

export function fetchRSSBriefing () {
  return function (dispatch) {
    dispatch(requestNewsFeed())
    return getBriefings()
    // .then(response => response.json(), error => console.log('error, see docs'))
    .then(response => {
      dispatch(receiveNewsFeed(response.data.results))
    })
  }
}

export default {
  addToSavedList,
  summarizeWithURL,
  increaseCount,
  requestNewsFeed,
  receiveNewsFeed,
  feedFetchFailure,
  fetchRSSFeed,
  clearRSSFeed,
  fetchRSSBriefing,
  Types
};