from feeder.formatter.topic_mapper import map_articles
from feeder.formatter.content_fixer import extract_nlp_summ_kw, fix_most_recent, extract_missing_features, fetch_articles_missing
from feeder.models import article
from feeder.util.time_tools import print_timestamp

# db_rows = fetch_articles(18, 15)
# db_rows = fetch_article(61203)
# db_rows = fetch_article(61160)
# db_rows = fetch_article(61154)
# articles = map_articles(db_rows)

# fix_most_recent(12)
# print(48*3)
print_timestamp("START KEYWORD AND PARAGRAPGH EXTRACTION")
articles = articles = fetch_articles_missing(hours_ago=2, keywords=True, paragraphs=True, debug=True)
extract_missing_features(articles,keywords=True, paragraphs=True, debug=False)
print_timestamp("FINISH ARTICLE EXTRACTION, START ARTICLE FETCH 2")
articles = articles = fetch_articles_missing(hours_ago=2, nlp_kw=True, summary=True, paragraphs=True, debug=True)
extract_missing_features(articles,keywords=True, nlp_kw=True, summary=True, debug=False)
print_timestamp("FINISHED SECOND EXTRACTION")

# res = get_summary()


# article = Article.select().where(Article.id == 61749).execute()[0]
# extract_nlp_summ_kw(article, False, True, True)
