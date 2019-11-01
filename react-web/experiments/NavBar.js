import React from 'react';
import './css/NavBar.css';
/* eslint-disable jsx-a11y/anchor-is-valid, jsx-a11y/anchor-is-valid, jsx-a11y/anchor-is-valid */
class NavBar extends React.Component {
  constructor(props) {
    super(props);
    var options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
    const today = new Date()

    this.state = {
      today: today.toLocaleDateString(undefined, options),
    }
    this.activateLasers = this.activateLasers
  }
  activateLasers () {
    console.log('pew pew')
  }
  
  render () {
    return (
      <div className="">
        <nav className="navbar" role="navigation" aria-label="main navigation">
          <div id="navbarBasicExample" className="navbar-menu">
            <div className="navbar-start NavBar">
              <a href="#" className="navbar-item" onClick={this.activateLasers}> 
                Home
              </a>
              <a href="#" className="navbar-item">
                About
              </a>
              <a href="#" className="navbar-item">
                News
              </a>
              <a href="#" className="navbar-item">
                Settings
              </a>
            </div>
            <div className="navbar-end">
              <div className="navbar-item">
                <div className="buttons">
                  <a  href="#" className="button is-light">
                    Remove Delay
                  </a>
                </div>
              </div>
            </div>
          </div>
        </nav>
      </div>
    );
  }
}

export default NavBar;
