import React from 'react';
import NavBar from './components/NavBar';
import ArticleList from './components/ArticleList'
import './App.css';
import './App.sass';

class App extends React.Component {
  constructor(props) {
    super(props);
    var options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
    const today = new Date();

    this.state = {
      today: today.toLocaleDateString(undefined, options),
      currentView: 'home'
    };
    this.setView = this.setView.bind(this);
  }
  setView (val) {
    this.currentView = val
    console.log(val);
  };
  currentView

  render () {
    return (
      <div className="">
        <div>
          <NavBar 
            setHome={() => this.setView('home')}
            setAbout={() => this.setView('about')}
            setNews={() => this.setView('news')}
            setSettings={() => this.setView('settings')}
            />
        </div>
        <div className="AppBody">
          <h1 className="title"> gossip </h1>
          <div className="">
            <ArticleList />
          </div>
        </div>
      </div>
    );
  }
}

export default App;
