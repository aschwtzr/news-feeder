import React from 'react'
import ScrollingBriefingTable from '../../components/briefings/ScrollingBriefingTable';


const Briefings = props => (
  <div>
    <ScrollingBriefingTable />
  </div>
)

export default Briefings

// const mapStateToProps = ({ counter }) => ({
//   count: counter.count,
//   isIncrementing: counter.isIncrementing,
//   isDecrementing: counter.isDecrementing
// })

// const mapDispatchToProps = dispatch =>
//   bindActionCreators(
//     {
//       increment,
//       incrementAsync,
//       decrement,
//       decrementAsync,
//       changePage: () => push('/about-us')
//     },
//     dispatch
//   )

// export default connect(
//   mapStateToProps,
//   mapDispatchToProps
// )(Briefings)
