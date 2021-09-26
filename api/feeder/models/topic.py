# Primarily a grouping of articles useful when pulling from Google News
class Topic:
  def __init__(self, articles, keywords):
    self.articles = articles
    self.keywords = keywords
    self.date = sorted(articles, key=lambda x: x.date, reverse=True)[0].date
  
  def add_articles(self, articles):
    self.articles += articles
  
  def string_date(self):
    self.date.strftime('%m/%d/%Y, %H:%M')

  def set_keywords(self, keywords):
    self.keywords = keywords

  def woof(self):
    print(f"{len(self.articles)} articles")
    for article in self.articles:
      article.woof()
    print(f"keywords: {self.keywords}")
    print(f"\n\n")
