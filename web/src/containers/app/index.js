import React from 'react'
import { Route, Link } from 'react-router-dom'
import Home from '../home'
import About from '../about'
import Briefings from '../briefings'
import './index.css'

const App = () => (
  <div>
    <header className="navigation-bar">
      {/* <Link to="/">Home</Link> */}
      <Link to="/about-us">About</Link>
      <Link to="/briefings">Briefings</Link>
    </header>

    <main className="main">
      <Route exact path="/" component={Home} />
      <Route exact path="/about-us" component={About} />
      <Route exact path="/briefings" component={Briefings} />
    </main>
  </div>
)

export default App
