export const FETCH_BRIEFING_REQUEST = 'briefings/FETCH_BRIEFING_REQUEST'
export const FETCH_BRIEFING_SUCCESS = 'briefings/FETCH_BRIEFING_SUCCESS'
export const FETCH_BRIEFING_FAILURE = 'briefings/FETCH_BRIEFING_FAILURE'
export const REQUEST_BRIEFINGS = 'briefings/REQUEST_BRIEFINGS'
export const RECEIVE_BRIEFINGS = 'briefings/RECEIVE_BRIEFINGS'


const initialState = {
  briefings: 0,
  isFetching: false,
  isDecrementing: false
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
        brefings: state.count + 1,
        isFetching: false
      }

    case FETCH_BRIEFING_FAILURE:
      return {
        ...state,
        isFetching: false
      }

    case REQUEST_POSTS:
      return {
        ...state,
        count: state.count - 1,
        isDecrementing: !state.isDecrementing
      }

    default:
      return state
  }
}



export const requestBriefing = (source, limit) => {
  return {
    type: REQUEST_BRIEFINGS,
    source,
    limit
  }
}

export const fetchBriefings = (source, limit) => {
  return dispatch => {
    dispatch({
      type: FETCH_BRIEFING_REQUEST,
    })

    dispatch({
      type: REQUEST_BRIEFINGS
    })
  }
}

export const incrementAsync = () => {
  return dispatch => {
    dispatch({
      type: INCREMENT_REQUESTED
    })

    return setTimeout(() => {
      dispatch({
        type: INCREMENT
      })
    }, 3000)
  }
}

export const decrement = () => {
  return dispatch => {
    dispatch({
      type: DECREMENT_REQUESTED
    })

    dispatch({
      type: DECREMENT
    })
  }
}

export const decrementAsync = () => {
  return dispatch => {
    dispatch({
      type: DECREMENT_REQUESTED
    })

    return setTimeout(() => {
      dispatch({
        type: DECREMENT
      })
    }, 3000)
  }
}

const flattenResults (results) {
  
}
