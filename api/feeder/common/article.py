from datetime import date
from feeder.util.api import get_summary

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

  def get_keywords(self):
    self.summary = (self.summary if self.summary is None else self.brief)

  # https://realpython.com/python-f-strings/
  # def __str__(self):
  #     return f"{self.first_name} {self.last_name} is {self.age}."

  # def __repr__(self):
  #     return f"{self.first_name} {self.last_name} is {self.age}. Surprise!"

  def woof(self):
    print(f"title: {self.title}")
    print(f"url: {self.url[:50]}...")
    print(f"source: {self.source}")
    print(f"date: {self.date}")
    print(f"brief: {self.brief[:80]}...")
    if hasattr(self, 'summary'):
      print(f"summary: {self.summary}")
      