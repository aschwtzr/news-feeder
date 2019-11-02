import React from 'react';
import './css/NavBar.scss';

function NavBar(props) {
  return (
    <div className="">
      <nav className="navbar" role="navigation" aria-label="main navigation">
        <div id="navbarBasicExample" className="navbar-menu">
          <div className="navbar-start NavBar">
            <button href="#" className="button is-white" onClick={props.setHome}> 
              Home
            </button>
            <button href="#" className="button is-white" onClick={props.setAbout}>
              About
            </button>
            <button href="#" className="button is-white" onClick={props.setNews}>
              News
            </button>
            <button href="#" className="button is-white" onClick={props.setSettings}>
              Settings
            </button>
          </div>
          <div className="navbar-end">
            <div className="navbar-item">
              <div className="buttons">
                <button  href="#" className="button is-light">
                  Remove Delay
                </button>
              </div>
            </div>
          </div>
        </div>
      </nav>
    </div>
  );
}

export default NavBar;
