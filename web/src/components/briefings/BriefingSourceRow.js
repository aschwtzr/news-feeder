import React from "react";
import { List, Card } from 'antd';
import PropTypes from "prop-types";
import './ScrollingTable.css';

class BriefingSourceRow extends React.Component {
  state = {
    showSummary: false,
  }
  
  toggleSummary () {
    this.setState({showSummary: !this.state.showSummary})
  }

  render() {
    const { source, summary, articles } = this.props;
    return (
        <div >
          <h2 
            onClick={ () => { this.setState({showSummary: !this.state.showSummary}) } }
            className="header">
            {source}</h2>
          <div className={this.state.showSummary ? 'summary_visible' : 'summary_hidden'}>{summary}</div>
          <List
          header={<div></div>}
          dataSource={articles}
          style={{
            display: 'flex',
            flexDirection: 'colmn',
            alignItems: 'center'
          }}
          renderItem={article => (
            <List.Item>
              <Card 
                title={article.title} 
                style={{backgroundColor: 'rgba(51, 101, 138, .8)', minHeight: '15rem', width: '80vw' }}
                extra={<a href={article.link} >Source</a>} 
                  >
                <div>
                  {article.content}
                </div>
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