from datetime import date
from feeder.util.orm import BaseModel
from peewee import *
from playhouse.postgres_ext import *

class Article(BaseModel):
  class Meta:
    table_name = 'pipeline_events'
  
  type = TextField()
  created_at = DateTimeTZField()
  article_id = IntegerField()
  input_text = TextField()
  output_text = TextField()
  extra_data = JSONField()
  function = TextField()
  function_caller = TextField()
  id = IntegerField()
  # https://stackoverflow.com/questions/5067604/determine-function-name-from-within-that-function-without-using-traceback