import React from "react";
import { Icon } from 'antd';
import { getFeedSources } from '../../utils/api'
import './SourcesMenu.css';

class SourcesMenu extends React.Component {
  constructor(props) {
    super(props)

    this.state = {
      showMenu: false,
      sources: []
    }
    this.menuClass = this.menuClass.bind(this)
    this.sources = this.sources.bind(this)
  }

  componentDidMount () {
    getFeedSources().then(function(results) {
      this.setState({sources: results.data.sources})
    }.bind(this))
  }

  menuClass () {
    return `floating-menu_content ${this.state.showMenu ? '' : 'hidden'}`
  }

  sources() {
    const sources = this.state.sources
    let listItems
    if (sources && sources.length > 1) {
      listItems = sources.map((source) => {
        return <li key={source}>{source}</li>
      })
    } else listItems = ''
    return (
      <ul className="floating-menu_content">{listItems}</ul>
    )
  }

  render() {
    return (
      <nav className="floating-menu" >
        <Icon type="setting" className="floating-menu__icon" onClick={ () => { this.setState({showMenu: !this.state.showMenu}) } }/>
        <div className={this.menuClass()}>
          {this.sources()}
        </div>        
      </nav>
    );
  }
}

export default SourcesMenu;