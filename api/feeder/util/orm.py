import os
from peewee import *
from playhouse.postgres_ext import PostgresqlExtDatabase

pg_db = PostgresqlExtDatabase(os.environ.get("DB_NAME"), user=os.environ.get("DB_USER"), password=os.environ.get("DB_PASS"),
                           host=os.environ.get("DB_HOST"), port=5432)

class BaseModel(Model):
  class Meta:
    database = pg_db