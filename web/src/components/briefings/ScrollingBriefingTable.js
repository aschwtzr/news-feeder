import React from 'react';
import './ScrollingTable.css';
import { List, Button } from 'antd';
import "antd/dist/antd.css";
import BriefingSourceRow from './BriefingSourceRow'
import { getBriefings } from '../../utils/api'
import SourcesMenu from '../sources-menu/SourcesMenu'

class ScrollingBriefingTable extends React.Component {
  constructor(props) {
    super(props);
    var options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
    const today = new Date()

    this.state = {
      today: today.toLocaleDateString(undefined, options),
      briefings: [],
      isLoading: false,
    }
    this.getBriefings = this.getBriefings.bind(this);
    this.tableBody = this.tableBody.bind(this)
  }

  async getBriefings (source) {
    this.setState({isLoading: true})
    try {
      let results = getBriefings('/headlines').then(function (results) {
        this.setState({briefings: results.data.headlines})
        this.setState({isLoading: false})
      }.bind(this))
    } catch {
      console.log('error')
    }
  }

  componentDidMount () {
    this.getBriefings()
  }

  tableBody () {
    if (this.state.briefings.length >= 1) {
      return <List
        bordered
        dataSource={this.state.briefings}
        renderItem={item => (
          <List.Item>
            <BriefingSourceRow source={item.source} articles={item.articles} summary={item.summary}/>
          </List.Item>
        )}
      />
    } else {
      return <div/>
    }
  }

  render() {
    return (
      <div>
        <header className="briefingTableHeader">
          <SourcesMenu />
          <p>
            Welcome. Today's date is {this.state.today}
          </p>
          <Button type="primary" onClick={this.getBriefings} className="briefingTableButton">  
            Get News
          </Button>
          {this.state.isLoading ? 'loading...' : ''}
        </header>
        { this.tableBody() }
      </div>
    );
  }
}

export default ScrollingBriefingTable;