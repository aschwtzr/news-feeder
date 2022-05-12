# Primarily a grouping of articles useful when pulling from Google News
class Topic:
  def __init__(self, articles, keywords, headline='', summary='', nlp_kw=[], kw_map={}):
    self.articles = articles
    self.keywords = keywords
    self.summary = summary
    self.nlp_kw = nlp_kw
    self.headline = headline
    self.date = sorted(articles, key=lambda x: x.date, reverse=True)[0].date
  
  def add_articles(self, articles):
    self.articles += articles
  
  def string_date(self):
    self.date.strftime('%m/%d/%Y, %H:%M')

  def set_keywords(self, keywords):
    self.keywords = keywords

  def to_dict(self):
    if self.articles is not None: 
      articles = list(map(lambda art: art.to_dict(), self.articles)),
    else:
      articles = []
    return {
        'date': self.date,
        'headline': self.headline,
        'keywords': self.keywords,
        'articles': articles,
        'summary': self.summary,
        'nlp_kw': self.nlp_kw
    }

  def woof(self):
    print(f"{self.headline}")
    print(f"{len(self.articles)} articles")
    if self.summary is not None:
      print(f"{self.summary}\n")
    print(f"TOPIC KW: {self.keywords}")
    if self.nlp_kw is not None:
      print(f"NLP KW: {self.nlp_kw}")
    print(f"\n")
    i = iter(range(len(self.articles)))
    while (x := next(i, None)) is not None and x < 5:
      article = self.articles[x]
      print(f"{article.source} -- {article.title}")
      print(f"KW: {article.keywords}")
      if article.nlp_kw is not None:
        print(f"NLP KW: {article.nlp_kw}")
      if article.summary is not None:
        print(f"{article.summary}")
      print("\n")
    print(f"\n")
    print(f"###")
    print(f"\n\n")
