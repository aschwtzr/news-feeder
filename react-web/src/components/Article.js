import React, { useState } from 'react';
import Icon from '@mdi/react'
import { mdiChevronDown, mdiChevronRight } from '@mdi/js'
import './css/Article.css';

function Article(props) {
  const [expanded, setExpanded] = useState(false)

  const contentTeaser = !expanded ? 
    <p 
      className="OverflowingText"
      style={{cursor: 'pointer'}}
      onClick={() => setExpanded(!expanded)}
      >
        { props.summary || props.content }
    </p> : <div/>

  const contentPanel = expanded ? 
    <div className="card-content is-loading"  >
      <div className="Content">
        {props.content} <br/>
        source:<a href={props.url}>{props.url}</a>
        <br/>
        <br/>
        <time dateTime="2016-1-1">{props.formattedDate}</time>
      </div>
    </div> : <div/>

  const teaserIconPath = expanded ? mdiChevronDown : mdiChevronRight

  return (
      <div className="card ArticleCardContainer">
        <header className="card-header">
          <p className="card-header-title ArticleTitle">
            {props.title}
          </p>
          {contentTeaser}
          <div
            className="card-header-icon" 
            aria-label="more options"
            onClick={() => setExpanded(!expanded)}>
            <span className="icon is-small">
              <Icon 
                path={teaserIconPath}
                title="Toggle Content"
                size={2}
                />
            </span>
          </div>
        </header>
        { contentPanel }
        <footer
          className="card-footer"
          // style="background-color: #F7F7FF;"
          >
          <div
            // v-for="button in buttons"
            // :key="button.title"
            className="CardFooterButton"
            // :className="button.className()"
            // @click="button.callback"
            >
            <span
              // v-if="(loading || summary) && button.title === 'Summarize'"
              className="icon is-small"
              // @click="expanded = !expanded"
              >
              <i
                // :className="`mdi mdi-${loading ? 'loading loading-spinner' : 'check'}`"
                />
            </span>
            <div 
            // v-else
            onClick={() => props.onButtonClick()}
            >
              button title
            </div>
          </div>
        </footer>
      </div>
  );
}

export default Article;