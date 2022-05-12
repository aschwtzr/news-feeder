# general imports
from collections import Counter, defaultdict
import json

# feeder imports
from feeder.formatter.keyword_extractor import keywords_from_string
from feeder.formatter.summarizer import summarize_nlp, small_summarize_nlp, summarize_nltk
import feeder.util.db as db
from feeder.util.api import summarize_text
from feeder.models.article import Article
from feeder.models.topic import Topic

def map_articles(rows):
  articles = []
  for row in rows:
    articles.append(Article(source=row[0], url=row[1], title=row[2], raw_text=row[9], date=row[4], keywords=row[5], id=row[7]))
  return articles

def keyword_frequency_map(articles):
  kw_map = defaultdict(list)
  for article in articles:
    keywords = article.keywords + article.nlp_kw
    for keyword in article.keywords:
      kw_map[keyword].append(article.id)
  return dict(sorted(kw_map.items(), key=lambda item: len(item[1]), reverse=True))

def map_article_relationships(rows, mapped_kw):
  relationship_map = {}
  for article in rows:
    siblings = defaultdict(int)
    for keyword in article.keywords:
      for id in mapped_kw[keyword]:
        siblings[id] += 1
    relationship_map[article.id] = siblings
  return relationship_map

def intersection(lst1, lst2):
  return list(set(lst1) & set(lst2))

def make_topics_map (processed, relationship_map, dataframe, debug=False):
  topics = defaultdict(dict)
  topic_idx = 0
  for article in processed:
    if debug ==True:
      print(article.id)
      print(f"KEYWORDS {', '.join(article.keywords)}")
      print(f"SIBS: {relationship_map[article.id]}")
    topic_article_ids = []
    all_keywords = []
    for id, freq in dict(relationship_map[article.id]).items():
      # find sibling articles (at least two kw match)
      if freq > 1:
        # print(dataframe.loc[dataframe['id'] == id]['title'])
        topic_article_ids.append(id)
        a = dataframe.loc[dataframe['id'] == id]
        all_keywords += a.iloc[0]['keywords']
    cnt = Counter(all_keywords)
    filtered = [k for k, v in cnt.items() if v > 1]
    # print(f"FILTERED {filtered}")
    best_match_cnt = 0
    best_match_key = f"topic_{topic_idx}"
    for topic_key, topic in topics.items():
      overlap = len(intersection(topic['keywords'], filtered))
      if overlap > 1 and overlap > best_match_cnt:
        best_match_cnt = overlap
        best_match_key = topic_key
    if best_match_key in topics:
      topics[best_match_key]['articles'].append(article.id)
      topics[best_match_key]['keywords'] = list(set(topics[best_match_key]['keywords']) | set(filtered))
      # topics[best_match_key]['keywords'] =  topics[best_match_key]['keywords'] + filtered
    else:
      topics[best_match_key]['articles'] = [article.id]
      topics[best_match_key]['keywords'] = article.keywords
      topic_idx+=1
  # print(json.dumps(topics, sort_keys=True, indent=2))
  return dict(sorted(topics.items(), key=lambda item: len(item[1]['articles']), reverse=True))

def print_topic_map(topic_map, dataframe):
  for k, values in topic_map.items():
    print(values['keywords'])
    print(len(values['articles']))
    # print(values)
    titles = []
    for id in values['articles']:
      a = dataframe.loc[dataframe['id'] == id]
      titles.append(a.iloc[0]['title'])
    for title in titles:
      print(title)
    print(' ')
    print(' ')

def map_topic(topic, dataframe):
  articles = []
  for id in topic['articles']:
    topic_summary = ''
    a = dataframe.loc[dataframe['id'] == id]
    row = a.iloc[0]
    if row['content'] is not None and len(row['content']) > 0:
      raw_text = row['content']
    else:
      raw_text = f"{row['title']}. "
    article = Article(
      source=row['source'], 
      url=row['url'], 
      title=row['title'], 
      raw_text=raw_text, 
      date=row['date'], 
      keywords=row['keywords'], 
      id=row['id'], 
      summary=row['summary'], 
      nlp_kw=row['nlp_kw']
    )
    articles.append(article)
    if article.summary is not None:
      topic_summary += article.summary
  by_brief = sorted(articles, key=lambda x: x.date, reverse=True)
  if len(articles) > 3:
    reduced = " ".join(list(map(lambda x: x.summary if x.summary is not None else '', articles[:5])))
    summary = small_summarize_nlp(reduced)
    if len(summary) > 120:
      nlp_kw = keywords_from_string(summary)
      headline = summarize_nltk(summary, 1)
    else:
      nlp_kw = keywords_from_string(reduced)
      headline = summarize_nltk(reduced, 1)
  else:
    reduced = " ".join(list(map(lambda x: x.summary if x.summary is not None else '', articles)))
    nlp_kw = keywords_from_string(reduced) if len(articles) > 2 else articles[0].nlp_kw
    headline = summarize_nltk(reduced, 1) if len(articles) > 2 else articles[0].title
    summary = summarize_nltk(reduced, 3) if len(articles) > 2 else articles[0].summary
  return Topic(by_brief, topic['keywords'], headline, summary, nlp_kw)

def map_topic_test(topic, dataframe):
  # print(topic)
  # print(dataframe)
  articles = []
  for id in topic['articles']:
    a = dataframe.loc[dataframe['id'] == id]
    # print(a.iloc[0])  
    row = a.iloc[0]
    if row['content'] is not None and len(row['content']) > 0:
      raw_text = row['content']
    else:
      raw_text = f"{row['title']}. "
    article = Article(source=row['source'], url=row['url'], title=row['title'], raw_text=raw_text, date=row['date'], keywords=row['keywords'], id=row['id'])
    articles.append(article)
  by_brief = sorted(articles, key=lambda x: len(x.raw_text), reverse=True)
  topic = Topic(by_brief, topic['keywords'])
  topic.woof()
  return topic

# res = get_summary()

# i = iter(range(res['counts']['topics']))
# while (x := next(i, None)) is not None and x < 5:
#   res['topics'][x].woof()