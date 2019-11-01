import React from 'react';
import NavBar from './components/NavBar';
import './App.css';
import './App.sass';

class ArticleList extends React.Component {
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
          Tab Bar
        </div>
        <div className="">
        </div>
      </div>
    );
  }
}

export default ArticleList;
