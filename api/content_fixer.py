from feeder.formatter.topic_mapper import fetch_articles, map_articles, fetch_article
from feeder.formatter.article_formatter import get_full_text
from feeder.formatter.keyword_extractor import keywords_from_article, nlp_keywords_from_article
from feeder.formatter.topic_mapper import intersection
from feeder.util.db import upsert_article

db_rows = fetch_articles(18, 15)
# db_rows = fetch_article(60862)
articles = map_articles(db_rows)

for article in articles:
    # print(article.raw_text)
    # print(article.keywords)
    text = get_full_text(article.url)
    print(f"Artcle ID: {article.id}")
    if text["ok"]:
        print("### FULL TEXT ### \n")
        print(text['text'])
        print('### AFTER ### \n')
        keywords = nlp_keywords_from_article(text['text'])
        # print(keywords)
        # if article.keywords is not None and len(article.keywords) > 0:
        #     upsert_kw = intersection(keywords, article.keywords)
        # else:
        #     upsert_kw = keywords
        # print(upsert_kw)
        # upsert_article(upsert_kw, article.title, article.url, article.source, article.date, text['text'], article.id)
    else:
        print('no dice \n')
    print('')