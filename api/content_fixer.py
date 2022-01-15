from feeder.formatter.topic_mapper import fetch_articles, map_articles
from feeder.formatter.article_formatter import get_full_text
from feeder.formatter.keyword_extractor import keywords_from_article
from feeder.formatter.topic_mapper import intersection
from feeder.util.db import upsert_article

db_rows = fetch_articles(18, 15)
articles = map_articles(db_rows)

for article in articles:
    print("### BEFORE ### \n")
    print(article.brief)
    print(article.keywords)
    text = get_full_text(article.url)
    if text["ok"]:
        print('### AFTER ### \n')
        print(text['text'])
        keywords = keywords_from_article(article)
        if article.keywords is not None and len(article.keywords) > 0:
            upsert_kw = intersection(keywords, article.keywords)
        else:
            upsert_kw = keywords
        print(upsert_kw)
        # upsert_article(upsert_kw, article.title, article.url, article.source, article.date, text['text'], article.id)
    else:
        print('no dice \n')
    print('')