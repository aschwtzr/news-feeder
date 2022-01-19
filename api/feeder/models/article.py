from datetime import date
from feeder.util.api import get_summary
from feeder.util.orm import BaseModel
from peewee import *
from playhouse.postgres_ext import *

class Article(BaseModel):
  class Meta:
    table_name = 'articles'
  
  source = TextField()
  date = DateTimeTZField()
  url = TextField()
  title = TextField()
  raw_text = TextField(column_name='content')
  keywords = ArrayField(default=[])
  id = IntegerField()
  
  def get_smmry(self):
    text = get_summary(self.url)
    self.summary = text.summary

  def get_keywords(self):
    self.summary = (self.summary if self.summary is None else self.raw_text)

  def woof(self):
    print(f"title: {self.title}")
    print(f"url: {self.url[:50]}...")
    print(f"source: {self.source}")
    print(f"date: {self.date}")
    if self.raw_text is not None:
      print(f"raw_text: {self.raw_text[:80]}...")
    if hasattr(self, 'summary'):
      print(f"summary: {self.summary}")
      