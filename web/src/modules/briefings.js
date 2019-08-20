// ACTION TYPES
export const FETCH_BRIEFING_REQUEST = 'briefings/FETCH_BRIEFING_REQUEST'
export const FETCH_BRIEFING_SUCCESS = 'briefings/FETCH_BRIEFING_SUCCESS'
export const FETCH_BRIEFING_FAILURE = 'briefings/FETCH_BRIEFING_FAILURE'

const initialState = {
  isFetching: false,
  briefings: [],
  briefingsBySource: [],
  fetchError: undefined
}

const tree = {
  sources: {
    byId: {
      id: '',
      briefings: ['articleId', 'articleIdo']
    },
    all: ['bbc', 'dw']
  },
  briefings: {
    byId: {
      id: 'hashed-title',
      content: '',
      url: '',
      date: '',
      author: ''
    },
    all: ['article1', 'article2']
  }
}

// REDUCERS
export default (state = initialState, action) => {
  switch (action.type) {
    case FETCH_BRIEFING_REQUEST:
      return {
        ...state,
        isFetching: true
      }

    case FETCH_BRIEFING_SUCCESS:
      return {
        ...state,
        brefings: action.results,
        isFetching: false
      }

    case FETCH_BRIEFING_FAILURE:
      return {
        ...state,
        isFetching: false
      }

    default:
      return state
  }
}

// ACTION CREATORS
export const fetchBriefingRequest = (source, limit) => {
  return {
    type: FETCH_BRIEFING_REQUEST,
    source,
    limit
  }
}

export const fetchBriefingSuccess = (results) => {
  return {
    type: FETCH_BRIEFING_SUCCESS,
    results
  }
}

export const fetchBriefingFailure = (error) => {
  return {
    type: FETCH_BRIEFING_FAILURE,
    fetchError: error
  }
}