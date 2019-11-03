import { createStore, applyMiddleware } from "redux";
import thunkMiddleware from 'redux-thunk'
// Logger with default options
import logger from "redux-logger";

import reducer from "./reducers/index";

export default function configureStore(initialState) {
  const store = createStore(reducer, initialState, applyMiddleware(thunkMiddleware, logger));
  return store;
}