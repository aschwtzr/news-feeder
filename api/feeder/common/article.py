from datetime import date
from api.feeder.util.api import get_summary

class Article:
  def __init__(self, source, url, title, brief, date):
    self.source = source
    self.url = url
    self.title = title
    self.brief = brief
    self.date = (date.today() if date is None else date)
  
  def get_smmry(self):
    text = get_summary(self.url)
    self.summary = text
    print(text)

  def get_keywords(self):
    summary = (self.summary if self.summary is None else self.brief)
    print(summary)

  def print(self):
    print(self.title)
    print(self.url)
    print(self.source)
    print(self.date)
    print(self.brief)