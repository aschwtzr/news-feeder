import datetime
import heapq
import os
import re
from collections import Counter, defaultdict

import nltk

import feeder.formatter.keyword_extractor as keyword_extractor
import feeder.util.db as db
from feeder.util.api import summarize_text
import pandas as pd
import yagmail
from feeder.common.article import Article
from feeder.common.topic import Topic

conn = db.get_db_conn()

def fetch_articles(hours_ago = 24):
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
  # return list(lst1 + lst2)

def make_topics_map (processed, rel):
  topics = defaultdict(dict)
  topic_idx = 0
  for article in processed:
    # print(f"KEYWORDS {', '.join(article[8])}")
    # print(f"SIBS: {rel[article[7]]}")
    topic_article_ids = []
    all_keywords = []
    for id, freq in dict(rel[article[7]]).items():
      # find sibling articles (at least two kw match)
      if freq > 2:
        # print(df.loc[df['id'] == id]['title'])
        topic_article_ids.append(id)
        a = df.loc[df['id'] == id]
        all_keywords += a.iloc[0]['keywords']
    cnt = Counter(all_keywords)
    filtered = [k for k, v in cnt.items() if v > 1]
    # print(f"FILTERED {filtered}")
    best_match_cnt = 0
    best_match_key = f"topic_{topic_idx}"
    for topic_key, topic in topics.items():
      overlap = len(intersection(topic['keywords'], filtered))
      if overlap > 2 and overlap > best_match_cnt:
        best_match_cnt = overlap
        best_match_key = topic_key
    if best_match_key in topics:
      topics[best_match_key]['articles'].append(article[7])
      topics[best_match_key]['keywords'] = list(set(topics[best_match_key]['keywords']) | set(filtered))
      # topics[best_match_key]['keywords'] =  topics[best_match_key]['keywords'] + filtered
    else:
      topics[best_match_key]['articles'] = [article[7]]
      topics[best_match_key]['keywords'] = filtered
      topic_idx+=1

  return dict(sorted(topics.items(), key=lambda item: len(item[1]['articles']), reverse=True))


def print_topic_map(topic_map):
  for k, values in topic_map.items():
    print(values['keywords'])
    titles = []
    for id in values['articles']:
      a = df.loc[df['id'] == id]
      titles.append(a.iloc[0]['title'])
    for title in titles:
      print(title)
    print(' ')
    print(' ')

def map_topic(topic):
  articles = []
  for id in topic['articles']:
    a = df.loc[df['id'] == id]
    row = a.iloc[0]
    if row['smr_summary'] is not None:
      brief = row['smr_summary']
    elif row['content'] is not None and len(row['content']) > 0:
      brief = row['content']
    else:
      brief = f"{row['title']}. "
    article = Article(row['source'], row['url'], row['title'], brief, row['date'], row['keywords'], row['id'])
    articles.append(article)
  return Topic(articles, topic['keywords'])

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

def build_email_body (topics, counts, dev_mode = False):
  contents = ['<body>']
  contents.append(f'<h2 style="color: #33658A; font-weight: 800px; margin: 0;">Hello from the newly Artificially Intelligent News Feeder</h2><br>')
  contents.append(f"<div>I scanned {counts['articles']} articles into {counts['topics']} news items. Here's the latest news:</div><br>")
  other_news = False
  for topic in topics:
    long_string = ''
    articles_html = []
    if len(topic.articles) > 1:
      headline = summarize('. '.join(list(map(lambda x: x.title, topic.articles))), 1)
      contents.append(f'<strong style="font-size: 15px;">{headline}</strong><br>')
      contents.append(f"<div style='{'' if dev_mode is True else 'display: none;'}'>{topic.keywords}</div>{'<br>' if dev_mode is True else ''}")
      for article in topic.articles:
        articles_html.append(f"<a href='{article.url}'><strong>{article.title}</strong></a><br>")
        articles_html.append(f"<strong>{article.source}</strong>")
        articles_html.append(f"<em>{article.date.strftime('%m/%d/%Y, %H:%M')}</em><br>")
        articles_html.append(f"<div style='{'' if dev_mode is True else 'display: none;'}'>{article.keywords}</div>{'<br>' if dev_mode is True else ''}")
        # if article.brief is not None:
        articles_html.append(f"<div>{'. '.join(list(article.brief.split('. '))[:2])}<div> {'<br>' if len(article.brief) > 0 else '' } ")
        long_string += article.brief
      if len(topic.articles) > 10:
        # sentences = 10
        sentences = 4
      elif len(topic.articles) > 6:
        # sentences = 8
        sentences = 3
      elif len(topic.articles) > 3:
        # sentences = 6
        sentences = 2
      else:
        # sentences = 4
        sentences = 1
      long_string.rstrip()
      print(long_string)
      # if len(long_string) > 0:
      topic_sum = summarize(long_string, sentences)
      # topic_sum = summarize_text(long_string, sentences)
      contents.append(f'<div>{topic_sum}</div>')
      contents.append('<br>')
      contents.append('<strong> *** Articles *** </strong>')
      contents += articles_html
    else:
      article = topic.articles[0]
      if other_news is False:
        contents.append('<br><br><h4>Other News </h4>')
        other_news = True
      contents.append(f"<strong style='font-size:15px; font-weight: bold!important'><a href='{article.url}'>{article.title}</a></strong>")
      articles_html.append(f"<strong>{article.source}</strong>")
      articles_html.append(f"<em>{article.date.strftime('%m/%d/%Y, %H:%M')}</em><br>")
      articles_html.append(f"<div style='{'' if dev_mode is True else 'display: none;'}'>{article.keywords}</div>{'<br>' if dev_mode is True else ''}")
      articles_html.append(f'<div>{topic.articles[0].brief}</div>')
      contents += articles_html
    contents.append("###<br>")
    contents.append("<br>")
  contents.append('</body>')
  return contents

articles = fetch_articles()
processed = process_db_rows(articles)

mapped_kw = keyword_frequency_map(processed)

rel = map_article_relationships(processed, mapped_kw)

df = pd.DataFrame(data = processed, columns = ['source', 'url', 'title', 'smr_summary', 'date', 'headline_keywords', 'smr_keywords', 'id', 'keywords', 'content'])

topic_map = make_topics_map(processed, rel)
mapped_topics = map(lambda tuple: map_topic(tuple[1]), topic_map.items())
mapped_topics_list = list(mapped_topics)
counts = {
  'articles': len(processed),
  'topics': len(mapped_topics_list),
}
body = build_email_body(mapped_topics_list, counts)
dev_body = build_email_body(mapped_topics_list, counts, True)

all_users = [
  {
    'email': 'schweitzer.albert@gmail.com',
    'body': dev_body
  },
  {
    'email': 'mansidhamija24@gmail.com',
    'body': body
  },
  {
    'email': 'heschwei@gmail.com',
    'body': body
  },
  {
    'email': 'kerygma01@yahoo.com',
    'body': body
  },
  {
    'email': 'mariselp_1305@yahoo.com',
    'body': body
  }
]

users_dev = [
  {
    'email': 'schweitzer.albert@gmail.com',
    'body': dev_body
  }
]

now = datetime.datetime.now()
timestamp = now.strftime('%m/%d/%Y, %H:%M')

print(f"""
*****************************************  
*****************************************  
  SENDING NEWS AT {timestamp}
*****************************************  
*****************************************  
""")

users = all_users if os.environ.get("PROD") is True else users_dev

for user in users:
  yagmail.SMTP(os.environ.get('EMAIL_ADDRESS'), os.environ.get('EMAIL_PASSWORD')).send(
    to=user['email'],
    subject=f"Your {timestamp} News Briefing",
    contents=user['body']
  )
  print(f"EMAIL SENT TO {user['email']}")
