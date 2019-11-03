import ACTIONS from "../action";

const defaultState = {
  saved: {},
  rssBriefings: [],
  count: 0,
};

const newsReducer = (state = defaultState, action) => {
  switch (action.type) {
    case ACTIONS.Types.SAVE_ARTICLE: {
      console.log(action);
      const article = action.payload;
      const newSaved = { ...state.saved, [article.url]: article };
      const newState = { ...state, saved: newSaved };
      return newState;
    }

    case ACTIONS.Types.SUMMARIZE_WITH_URL: {
      const incomingArticleURL = action.payload
      console.log(incomingArticleURL)
      const newState = state
      return newState;
    }

    case ACTIONS.Types.INCREASE_COUNT: {
      const newState = { ...state, count: state.count + 1}
      return newState;
    }

    default:
      return state;
  }
};

export default newsReducer;