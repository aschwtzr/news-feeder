import { combineReducers } from 'redux'
import counter from './counter'
import briefings from './briefings'
import settings from './settings'

export default combineReducers({
  counter,
  briefings,
  settings
})
