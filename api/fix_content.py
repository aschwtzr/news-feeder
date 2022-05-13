from feeder.formatter.topic_mapper import map_articles
from feeder.formatter.content_fixer import clean_article_data, fix_most_recent, extract_missing_features
from feeder.models import article

# db_rows = fetch_articles(18, 15)
# db_rows = fetch_article(61203)
# db_rows = fetch_article(61160)
# db_rows = fetch_article(61154)
# articles = map_articles(db_rows)

# fix_most_recent(12)
# print(48*3)
extract_missing_features(hours_ago=144)

# res = get_summary()


# article = Article.select().where(Article.id == 61749).execute()[0]
# clean_article_data(article, False, True, True)
