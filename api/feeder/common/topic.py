class Topic:
  def __init__(self, articles, keywords):
    self.articles = articles
    self.keywords = keywords
  
  def add_articles(self, articles):
    self.articles += articles

  def set_keywords(self, keywords):
    self.keywords = keywords

  def woof(self):
    print(f"{len(self.articles)} articles")
    print(self.keywords)
