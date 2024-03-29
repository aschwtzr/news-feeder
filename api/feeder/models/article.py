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
  feed_source_id = IntegerField()
  # sanitized body of the article
  raw_text = TextField(column_name='content')
  # keywords from v1 pipeline extraction
  keywords = ArrayField(default=[])
  id = IntegerField()
  # nlp api summary
  summary = TextField(column_name='smr_summary')
  # nlp api keywords
  nlp_kw = ArrayField(column_name='smr_keywords')
  named_entities = ArrayField()
  paragraphs = ArrayField()
  skip_extract = BooleanField()
  
  def get_smmry(self):
    text = get_summary(self.url)
    self.summary = text.summary

  def get_keywords(self):
    self.summary = (self.summary if self.summary is None else self.raw_text)

  def to_dict(self):
    return {
        'source': self.source,
        'date': self.date,
        'url': self.url,
        'title': self.title,
        'raw_text': self.raw_text,
        'keywords': self.keywords,
        'id': self.id,
        'summary': self.summary,
        'nlp_kw': self.nlp_kw
    }

  def woof(self):
    print(f"{self.source} --  {self.title}")
    # print(f"url: {self.url[:50]}...")
    # print(f"source: {self.source}")
    # print(f"date: {self.date}")
    print(f"keywords: {self.keywords}")
    if self.nlp_kw is not None and len(self.nlp_kw) > 0:
      print(f"nlp_kw: {self.nlp_kw}")
    if self.summary is not None and len(self.summary) > 0:
      print(f"summary: {self.summary}")
    if self.raw_text is not None and len(self.raw_text) > 0:
      print(f"raw_text: {self.raw_text[:600]}...")
    print(f"\n")
      