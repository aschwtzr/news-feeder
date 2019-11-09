import React from 'react';
import { getBriefings } from "../utils/Api";
import Article from './Article';
import ACTIONS from '../modules/action';
import { connect } from 'react-redux';

const mapStateToProps = state => ({
  count: state.news.count
});

const mapDispatchToProps = dispatch => ({
  increaseCount: () => dispatch(ACTIONS.increaseCount()),
  fetchRSSBriefing: () => dispatch(ACTIONS.fetchRSSBriefing())
});
class ArticleList extends React.Component {
  constructor(props) {
    super(props);
    var options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
    const today = new Date();

    this.state = {
      today: today.toLocaleDateString(undefined, options),
      currentView: 'home',
      briefings: []
    };
    this.setView = this.setView.bind(this);
    this.briefings = this.briefings.bind(this)
  }

  briefings () {
    const briefings = this.state.briefings //props.briefings;
    const listItems = briefings.map((briefing) =>  {
      const articles = briefing.articles.map((article) => 
        <Article 
          title={article.title}
          summary={article.summary}
          content={article.content}
          url={article.url}
          formattedDate={article.formattedDate}
          key={article.url}
          articleButtons={this.buttons()}
          onButtonClick={this.props.increaseCount}
        ></Article>
      )
      return (
        <li key={briefing.source}>
          <strong>
            <a href="#">{briefing.source}</a>
            { articles }
          </strong>
        </li>
      )}
    );
    return (
      <ul>{listItems}</ul>
    );
  }

  async componentDidMount() {
    // Load async data.
    let briefings = await getBriefings();
    this.props.fetchRSSBriefing()
        // Parse the results for ease of use.
    briefings = briefings.data.results;
    console.log(briefings)

    // // Update state with new data and re-render our component.
    // const name = `${userData.name.first} ${userData.name.last}`;
    // const avatar = userData.picture.large;
    // const email = userData.email;

    this.setState({ briefings });
  }
  
  buttons () {
    return [{
      title: 'Save',
      class: 'this.savedButtonClass',
      callback: () => { this.props.increaseCount() },
    },
    {
      title: 'Summarize',
      class: 'this.footerSummarizeClass',
      callback: () => { console.log('this.addToSummarizeFeed') },
    },
    {
      title: 'View',
      class: 'this.viewButtonClass',
      callback: () => { console.log('this.openArticle') },
    }]
  }

  setView (val) {
    this.currentView = val
    console.log(val);
  };

  render () {
    return (
      <div className="">
        <div>
          {this.props.count}
        </div>
        <div className="">
          { this.briefings() }
        </div>
      </div>
    );
  }
}

export default connect(
  mapStateToProps,
  mapDispatchToProps
  )(ArticleList);
