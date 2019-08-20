import React from 'react'
import { connect } from 'react-redux'
import { bindActionCreators } from 'redux'
import { fetchBriefingRequest, fetchBriefingSuccess, fetchBriefingFailure } from '../../modules/briefings'

import ScrollingBriefingTable from '../../components/briefings/ScrollingBriefingTable';


const Briefings = props => (
  <div>
    <ScrollingBriefingTable />
  </div>
)

const mapStateToProps = ({ briefings }) => ({
  isFetching: briefings.isFetching,
  isDecrementing: briefings.isDecrementing,
  briefings: briefings.briefings,
  briefingsBySource: briefings.briefingsBySource,
  fetchError: briefings.fetchError,
})

const mapDispatchToProps = dispatch =>
  bindActionCreators(
    {
      fetchBriefingRequest,
      fetchBriefingSuccess,
      fetchBriefingFailure,
    },
    dispatch
  )

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(Briefings)
