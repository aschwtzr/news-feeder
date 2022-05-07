# general imports
import heapq
import re
from collections import Counter, defaultdict
import nltk
import pandas as pd
import json
from datetime import datetime, timedelta

# feeder imports
from feeder.formatter.keyword_extractor import keywords_from_text_title, remove_known_junk, keywords_from_string
from feeder.formatter.summarizer import summarize_nlp, small_summarize_nlp
import feeder.util.db as db
from feeder.util.api import summarize_text
from feeder.models.article import Article
from feeder.models.topic import Topic

def update_v1_keywords(article, debug=False):
  cleaned = remove_known_junk(article.raw_text, True)
  article.raw_text = cleaned
  keywords = keywords_from_text_title(cleaned, article.title)
  article.keywords = keywords
  if debug == True:
    # print("AFTER\n")
    # print(cleaned)
    print("\nKEYWORDS\n")
    print(keywords)
  return article

def update_article_summary(article, debug):
  # TODO: split into nlp_kw and nlp summary
  try:
    summary = summarize_nlp(article.raw_text, debug)
  except IndexError as e:
    print(f"unable to transform ID: {article.id}, trying NLTK")
    summary = summarize(article.raw_text, 12)
  article.summary = summary
  article.nlp_kw = keywords_from_text_title(article.summary, article.title)

def clean_article_data(article, kw=False, summ=False, debug=False):
  print(f"ARTICLE_ID: {article.id}")
  if debug == True:
    print("RAW_TEXT - BEFORE\n")
    print(article.raw_text)
  if kw is True:
    update_v1_keywords(article, debug)
  if summ is True:
    update_article_summary(article, debug)
  article.save()
  return article

# TOPIC MAPPER 

def map_articles(rows):
  articles = []
  for row in rows:
    articles.append(Article(source=row[0], url=row[1], title=row[2], raw_text=row[9], date=row[4], keywords=row[5], id=row[7]))
  return articles

def keyword_frequency_map(articles):
  kw_map = defaultdict(list)
  for article in articles:
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
    try:
      summary = small_summarize_nlp(reduced)
    except: 
      print(reduced)
      for article in articles:
        print(f"Article Id: {article.id}")
      print('too many tokens for summarizer')
    if len(summary) > 120:
      nlp_kw = keywords_from_string(summary)
      headline = summarize(summary, 1)
    else:
      nlp_kw = None
      headline = None
  else:
    nlp_kw = None
    headline = None
    summary = None
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

def summarize(article_text, sentences):
  article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)
  article_text = re.sub(r'\s+', ' ', article_text)
  formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text )
  formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)
  sentence_list = nltk.sent_tokenize(article_text)
  stopwords = nltk.corpus.stopwords.words('english')

  word_frequencies = {} 
  for word in nltk.word_tokenize(formatted_article_text):
    if word not in stopwords:
      if word not in word_frequencies.keys():
        word_frequencies[word] = 1
      else:
        word_frequencies[word] += 1
  maximum_frequncy = max(word_frequencies.values())

  for word in word_frequencies.keys(): 
    word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)
  sentence_scores = {}
  for sent in sentence_list:
    for word in nltk.word_tokenize(sent.lower()):
      if word in word_frequencies.keys():
        if len(sent.split(' ')) < 30:
          if sent not in sentence_scores.keys():
            sentence_scores[sent] = word_frequencies[word]
          else:
            sentence_scores[sent] += word_frequencies[word]
  summary_sentences = heapq.nlargest(sentences, sentence_scores, key=sentence_scores.get)
  summary = ' '.join(summary_sentences)
  print(summary)
  return summary

# might be a v1 candidate

def get_summary(hours_ago=18):
  hours_ago_date_time = datetime.now() - timedelta(hours = hours_ago)
  articles = Article.select().where((Article.date > hours_ago_date_time) & (Article.summary.is_null(False)))
  print(f"ARTICLES IS THIS MANY {len(articles)}")
  processed = list(map(lambda article: clean_article_data(article, False, False, True), articles))
  # processed = articles

  mapped_kw = keyword_frequency_map(processed)
  # print(mapped_kw)

  relationship_map = map_article_relationships(processed, mapped_kw)
  # print(json.dumps(relationship_map, sort_keys=True, indent=2))

  df = pd.DataFrame(data = list(map(lambda x: [x.source, x.url, x.title, x.date, x.id, x.keywords, x.raw_text, x.summary, x.nlp_kw], processed)), columns = ['source', 'url', 'title', 'date', 'id', 'keywords', 'content', 'summary', 'nlp_kw'])

  topic_map = make_topics_map(processed, relationship_map, df)
  print_topic_map(topic_map, df)
  mapped_topics = map(lambda tuple: map_topic(tuple[1], df), topic_map.items())
  mapped_topics_list = sorted(list(mapped_topics), key=lambda topic: (len(topic.articles), topic.date), reverse=True)   
      
  counts = {
    'articles': len(processed),
    'topics': len(mapped_topics_list),
  }
  return {
    'counts': counts,
    'topics': mapped_topics_list,
    'mapped_kw': mapped_kw
  }

# res = get_summary()

# i = iter(range(res['counts']['topics']))
# while (x := next(i, None)) is not None and x < 5:
#   res['topics'][x].woof()