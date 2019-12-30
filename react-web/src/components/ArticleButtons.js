// import React, { useState } from 'react';
import React from 'react';
// import Icon from '@mdi/react';

function ArticleButtons(props) {
  const buttons = props.buttons.map(button => {
    return (
      <div
        key={ button.title }
        className="card-footer-item CardFooterButton"
        // :className="button.className()"
        onClick={() => button.callback()}
        >
        <span
          // v-if="(loading || summary) && button.title === 'Summarize'"
          className="icon is-small"
          // @click="expanded = !expanded"
          >
          {/* <Icon 
            path={teaserIconPath}
            title="Toggle Content"
            size={2}
            /> */}
          <i
            // :className="`mdi mdi-${loading ? 'loading loading-spinner' : 'check'}`"
            />
        </span>
        <div 
        // v-else
        // onClick={() => props.onButtonClick()}
        >
          { button.title }
        </div>
      </div>
    )
  })
  return (
    <footer
      className="card-footer"
      style={{backgroundColor: '#F7F7FF'}}
      >
      { buttons }
    </footer>
  )
}

export default ArticleButtons;