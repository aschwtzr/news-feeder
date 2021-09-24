# general imports
import heapq
import re
from collections import Counter, defaultdict
import nltk
import pandas as pd
import json

# feeder imports
import feeder.formatter.keyword_extractor as keyword_extractor
import feeder.util.db as db
from feeder.util.api import summarize_text
from feeder.common.article import Article
from feeder.common.topic import Topic

def fetch_articles(hours_ago = 18):
  conn = db.get_db_conn()
  ARTICLE_SQL = f"""
    select 
      source, 
      url, 
      title, 
      smr_summary, 
      date, 
      keywords, 
      smr_keywords, 
      id, 
      keywords || smr_keywords as grouped_keywords,
      content 
    from articles 
    --where smr_summary is not null 
    --and smr_keywords is not null
    where date > now() - interval '{str(hours_ago)} hours';
  """
  cur = conn.cursor()
  cur.execute(ARTICLE_SQL)
  articles = cur.fetchall()
  cur.close()
  conn.close()
  print(f"*** FETCHED {len(articles)} ROWS FROM THE DATABASE")
  return articles

def process_db_rows(rows=[]):
  res = []
  for row in rows:
    row_list = list(row)
    row_list[8] = keyword_extractor.filter_stopwords_from_keywords(row[8])
    if row_list[3] is not None:
      row_list[3] = row_list[3].replace('ADVERTISEMENT', '')
    # row_list[2] = keyword_extractor.remove_publication_after_pipe(row_list[2])
    res.append(tuple(row_list))
  return res

def keyword_frequency_map(rows):
  kw_map = defaultdict(list)
  for row in rows:
    for keyword in row[8]:
      kw_map[keyword].append(row[7])
  return dict(sorted(kw_map.items(), key=lambda item: len(item[1]), reverse=True))

def map_article_relationships(rows, mapped_kw):
  relationship_map = {}
  for article in rows:
    siblings = defaultdict(int)
    for keyword in article[8]:
      for id in mapped_kw[keyword]:
        siblings[id] += 1
    relationship_map[article[7]] = siblings
  return relationship_map

def intersection(lst1, lst2):
  return list(set(lst1) & set(lst2))

def make_topics_map (processed, relationship_map, dataframe):
  topics = defaultdict(dict)
  topic_idx = 0
  for article in processed:
    # print(article)
    # print(f"KEYWORDS {', '.join(article[8])}")
    # print(f"SIBS: {rel[article[7]]}")
    topic_article_ids = []
    all_keywords = []
    for id, freq in dict(relationship_map[article[7]]).items():
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
      topics[best_match_key]['articles'].append(article[7])
      topics[best_match_key]['keywords'] = list(set(topics[best_match_key]['keywords']) | set(filtered))
      # topics[best_match_key]['keywords'] =  topics[best_match_key]['keywords'] + filtered
    else:
      topics[best_match_key]['articles'] = [article[7]]
      topics[best_match_key]['keywords'] = article[8]
      topic_idx+=1
  print(json.dumps(topics, sort_keys=True, indent=2))
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
    a = dataframe.loc[dataframe['id'] == id]
    row = a.iloc[0]
    if row['smr_summary'] is not None:
      brief = row['smr_summary']
    elif row['content'] is not None and len(row['content']) > 0:
      brief = row['content']
    else:
      brief = f"{row['title']}. "
    article = Article(row['source'], row['url'], row['title'], brief, row['date'], row['keywords'], row['id'])
    articles.append(article)
  by_brief = sorted(articles, key=lambda x: len(x.brief), reverse=True)
  return Topic(by_brief, topic['keywords'])

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
  return summary

def get_summary(hours_ago=18):
  articles = fetch_articles(hours_ago)
  processed = process_db_rows(articles)

  mapped_kw = keyword_frequency_map(processed)

  relationship_map = map_article_relationships(processed, mapped_kw)
  print(json.dumps(relationship_map, sort_keys=True, indent=2))

  df = pd.DataFrame(data = processed, columns = ['source', 'url', 'title', 'smr_summary', 'date', 'headline_keywords', 'smr_keywords', 'id', 'keywords', 'content'])

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