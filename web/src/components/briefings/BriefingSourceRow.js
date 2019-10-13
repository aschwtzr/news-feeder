import React from "react";
import { List, Card } from 'antd';
import PropTypes from "prop-types";
import './ScrollingTable.css';

class BriefingSourceRow extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      showSummary: true,
      unfurledSummaries: []
    }
    
    this.toggleSummary = this.toggleSummary.bind(this)
    this.summary = this.summary.bind(this)
  }

  toggleSummary (index) {
    const cardIndex = this.state.unfurledSummaries.indexOf(index)
    const newUnfurled = [...this.state.unfurledSummaries]
    if (cardIndex > -1) {
      newUnfurled.splice(index, 1)
    } else {
      newUnfurled.push(index)
    }
    this.setState({ unfurledSummaries: newUnfurled})
  }

  summary (index, content) {
    if (this.state.unfurledSummaries.indexOf(index) > -1) {
      return  <div>
          {content} 
        </div>
    } else {
      return <div/>
    }
  }

  render() {
    const { source, summary, articles } = this.props;
    return (
        <div >
          <h2 className="header">{source}</h2>
          <div className={this.state.showSummary ? 'summary_visible' : 'summary_hidden'}>{summary}</div>
          <List
          header={<div></div>}
          dataSource={articles}
          style={{
            display: 'flex',
            flexDirection: 'colmn',
            alignItems: 'center'
          }}
          renderItem={(article, index) => (
            <List.Item>
              <Card 
                title={article.title} 
                onClick={ () => this.toggleSummary(index) }
                style={{minHeight: '2rem', width: '80vw', cursor: 'pointer' }}
                extra={<a href={article.url} target="_blank" rel="noopener noreferrer">Source</a>} 
                  >
                { this.summary(index, article.content) }
              </Card>
            </List.Item>
          )}
        />
        </div>
    );
  }
}

BriefingSourceRow.propTypes = {
  source: PropTypes.string,
  timestamp: PropTypes.string,
  briefings: PropTypes.array,
  isLoading: PropTypes.bool
};



export default BriefingSourceRow;