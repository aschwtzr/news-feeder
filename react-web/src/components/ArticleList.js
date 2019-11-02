import React from 'react';
import { getBriefings } from "../utils/Api";
import Article from './Article'

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
    this.cuticles = this.cuticles.bind(this)
  }

  cuticles (props) {
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
        // Parse the results for ease of use.
    briefings = briefings.data.results;
    console.log(briefings)

    // // Update state with new data and re-render our component.
    // const name = `${userData.name.first} ${userData.name.last}`;
    // const avatar = userData.picture.large;
    // const email = userData.email;

    this.setState({ briefings });
  }
 

  setView (val) {
    this.currentView = val
    console.log(val);
  };

  render () {
    return (
      <div className="">
        <div>
          Tab Bar
        </div>
        <div className="">
          { this.cuticles() }
        </div>
      </div>
    );
  }
}

export default ArticleList;
