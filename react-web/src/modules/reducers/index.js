import { combineReducers } from 'redux'
import briefingReducer from './briefingReducer'
import newsReducer from './newsReducer'

export default combineReducers({
  briefing: briefingReducer,
  news: newsReducer,
})