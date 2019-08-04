import React from "react";
import { Icon } from 'antd';
import './SourcesMenu.css';

class BriefingSourceRow extends React.Component {
  state = {
    showSummary: false,
  }
  
  toggleSummary () {
    this.setState({showSummary: !this.state.showSummary})
  }

  render() {
    return (
      <nav className="floating-menu"><Icon type="setting"  /></nav>
    );
  }
}

export default BriefingSourceRow;