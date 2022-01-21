from feeder.formatter.topic_mapper import clean_article_data, keyword_frequency_map, map_article_relationships, make_topics_map, print_topic_map, map_topic
from feeder.models.article import Article
from datetime import datetime, timedelta
import pandas as pd
import json

# db_rows = fetch_articles(18, 15)
# db_rows = fetch_article(61203)
# db_rows = fetch_article(61160)
# db_rows = fetch_article(61154)
# articles = map_articles(db_rows)

def fix_most_recent(hours_ago=12):
    hours_ago_date_time = datetime.now() - timedelta(hours = hours_ago)
    articles = Article.select().where(Article.date > hours_ago_date_time)
    print(f"ARTICLES ARE THIS MANY: {len(articles)}\n")
    # processed = []
    # for article in articles.iterator():
    processed = list(map(lambda article: clean_article_data(article, True, True, True), articles))
    mapped_kw = keyword_frequency_map(articles)
    print(mapped_kw)

    relationship_map = map_article_relationships(articles, mapped_kw)
    # print(json.dumps(relationship_map, sort_keys=True, indent=2))

    df = pd.DataFrame(data = list(map(lambda x: [x.source, x.url, x.title, x.date, x.id, x.keywords, x.raw_text, x.summary, x.nlp_kw], articles)), columns = ['source', 'url', 'title', 'date', 'id', 'keywords', 'content', 'summary', 'nlp_kw'])

    topic_map = make_topics_map(articles, relationship_map, df)
    mapped_topics = map(lambda tuple: map_topic(tuple[1], df), topic_map.items())
    mapped_topics_list = sorted(list(mapped_topics), key=lambda topic: (len(topic.articles), topic.date), reverse=True)  
    print_topic_map(topic_map, df)

    i = iter(range(len(mapped_topics_list)))
    while (x := next(i, None)) is not None and x < 10:
      mapped_topics_list[x].woof()

fix_most_recent(18)

# res = get_summary()


# article = Article.select().where(Article.id == 61749).execute()[0]
# clean_article_data(article, False, True, True)