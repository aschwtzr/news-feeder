import ACTIONS from "../action";
// https://redux.js.org/advanced/async-actions

const defaultState = {
  currentBriefing: 'rss',
  rssBriefings: [],
  loading: false,
};

const briefingsReducer = (state = defaultState, action) => {
  switch (action.type) {
    case ACTIONS.Types.REQUEST_NEWS_FEED: {
      const newState = { ...state, loading: true };
      return newState;
    }

    case ACTIONS.Types.FETCH_RSS_FAILURE: {
      const newState = { ...state, loading: false, error: action.payload }
      return newState;
    }
    
    case ACTIONS.Types.RECEIVE_NEWS_FEED: {
      const newState = { ...state, rssBriefings: action.payload }
      return newState;
    }

    case ACTIONS.Types.CLEAR_RSS_FEED: {
      const newState = { ...state, rssBriefings: []}
      return newState;
    }

    default:
      return state;
  }
};

export default briefingsReducer;