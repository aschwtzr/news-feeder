import React, { useState } from 'react';
import Icon from '@mdi/react'
import { mdiChevronDown, mdiChevronRight } from '@mdi/js'
import './css/Article.css';
import ArticleButtons from './ArticleButtons'

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
        <ArticleButtons buttons={props.articleButtons} />
      </div>
  );
}

export default Article;