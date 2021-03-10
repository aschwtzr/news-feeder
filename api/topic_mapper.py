import feeder.formatter.keyword_extractor as keyword_extractor
from collections import defaultdict
import pandas as pd
from collections import Counter
from feeder.common.article import Article
from feeder.common.topic import Topic
import yagmail
import os
import datetime
from gensim.summarization.summarizer import summarize

import feeder.util.db as db

conn = db.get_db_conn()
topic_keywords = defaultdict(list)
ARTICLE_SQL = """
    select 
      source, 
      url, 
      title, 
      smr_summary, 
      date, 
      keywords, 
      smr_keywords, 
      id, 
      keywords || smr_keywords as grouped_keywords 
    from articles 
    where smr_summary is not null 
    and smr_keywords is not null
    and date > now() - interval '24 hours';
  """

def fetch_articles():
  cur = conn.cursor()
  cur.execute(ARTICLE_SQL)
  articles = cur.fetchall()
  cur.close()
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
    article = Article(a.iloc[0]['source'], a.iloc[0]['url'], a.iloc[0]['title'], a.iloc[0]['smr_summary'], a.iloc[0]['date'], a.iloc[0]['keywords'], a.iloc[0]['id'])
    articles.append(article)
  return Topic(articles, topic['keywords'])

def build_email_body (topics):
  contents = ['<body>']
  contents.append(f'<h2 style="color: #33658A; font-weight: 800; margin: 0;">Hello from the newly Artificially Intelligent News Feeder</h2>')
  for topic in topics:
    if len(topic.keywords) > 2:
      headline_kw = topic.keywords
    else:
      headline_kw = topic.articles[0].keywords
    headline = " ".join(list(map(lambda x: x.capitalize(), headline_kw)))
    contents.append(f'<h3 style="font-weight=500;"> Headline: {headline}</strong><br>')
    long_string = ''
    articles_html = []
    if len(topic.articles) > 1:
      for article in topic.articles:
        articles_html.append(f"<a href='{article.url}'><strong>{article.title}</strong></a><br>")
        articles_html.append(f"<strong>{article.source}</strong>")
        articles_html.append(f"<em>{article.date.strftime('%m/%d/%Y, %H:%M')}</em><br>")
        articles_html.append(f"<div>{article.brief}<div> {'<br>' if len(article.brief) > 0 else '' } ")
        articles_html.append("<br>")
        long_string += article.brief
      if len(topic.articles) > 10:
        ratio = .02
      elif len(topic.articles) > 6:
        ratio = .05
      elif len(topic.articles) > 3:
        ratio = .1
      else:
        ratio = .2
      long_string.rstrip()
      topic_sum = summarize(long_string, ratio=ratio)
    else:
      articles_html.append(f"<a href='{article.url}'><strong>{article.title}</strong></a><br>")
      articles_html.append(f"<strong>{article.source}</strong>")
      articles_html.append(f"<em>{article.date.strftime('%m/%d/%Y, %H:%M')}</em><br>")
      articles_html.append("<br>")
      topic_sum = topic.articles[0].brief
    contents.append(f'<div>{topic_sum}</div>')
    contents.append('<br>')
    contents.append('<strong> *** Articles *** </strong>')
    contents += articles_html
    contents.append("<br><br>")
  contents.append('</body>')
  return contents

articles = fetch_articles()
processed = process_db_rows(articles)

mapped_kw = keyword_frequency_map(processed)

rel = map_article_relationships(processed, mapped_kw)

df = pd.DataFrame(data = processed, columns = ['source', 'url', 'title', 'smr_summary', 'date', 'headline_keywords', 'smr_keywords', 'id', 'keywords'])

topic_map = make_topics_map(processed, rel)
mapped_topics = map(lambda tuple: map_topic(tuple[1]), topic_map.items())

body = build_email_body(list(mapped_topics))

emails = ['schweitzer.albert@gmail.com', 'mansidhamija24@gmail.com', 'heschwei@gmail.com', 'kerygma01@yahoo.com']
#emails=['schweitzer.albert@gmail.com']

now = datetime.datetime.now()
timestamp = now.strftime('%m/%d/%Y, %H:%M')

print(f"""
*****************************************  
*****************************************  
  SENDING NEWS AT {timestamp}
*****************************************  
*****************************************  
""")

for email in emails:
  yagmail.SMTP(os.environ.get('EMAIL_ADDRESS'), os.environ.get('EMAIL_PASSWORD')).send(
    to=email,
    subject=f"Your {timestamp} News Briefing",
    contents=body
  )
  print(f"EMAIL SENT TO {email}")



