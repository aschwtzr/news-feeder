import React from 'react';
import logo from './logo.svg';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="navigation-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Welcome. You are using the free API mode or you are using paid mode. 
        </p>
        <p>
          Soon there will be a password input here. 
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

export default App;
