// ACTION TYPES
export const TOGGLE_SOURCE = 'settings/TOGGLE_SOURCE'

const initialState = {
  sources: [],
  isFetching: false,
}

const stateTree = {
  sources: ['bbc', 'dw', 'google'],
  active: [0, 2]
}

// REDUCERS
export default (state = initialState, action) => {
  switch (action.type) {
    case TOGGLE_SOURCE:
      return Object.assign({}, state, {
        active: action.active
      })

    default:
      return state
  }
}

// ACTION CREATORS
// export const toggleSource = (source, sourceIndex) => {
//   let activeCopy = state.active.slice()
//   let index = activeCopy.indexOf(sourceIndex) >= 0
//   if (index >= 0) {
//     activeCopy.splice(index, 1)
//   } else activeCopy.push(sourceIndex)
//   return {
//     type: TOGGLE_SOURCE,
//     activeCopy
//   }
// }
