from feeder.util.api import get_timeline_for_user
from datetime import timedelta, datetime, timezone
import json

def calc_virality(retweets, favs, timestamp, hours=False):
  reach = ((retweets * 2.5) + favs) * 10
  # twit_time = datetime.strptime(timestamp, "%c")
  twit_time = datetime.strptime(timestamp, "%a %b %d %H:%M:%S %z %Y")
  delta = datetime.now(timezone.utc) - twit_time
  return ((reach / ((delta.seconds / 60) / 60)),(reach / (delta.seconds / 60)))
  

  # res = { 
  #   'hourly': (reach / ((delta.seconds / 60) / 60), 
  #   'secondly': (reach / (delta.seconds / 60))
  # }
  # return reach / (delta.seconds / 60)
  # return res

# tweets = get_timeline_for_user('ap')
# tweets = get_timeline_for_user('ReutersWorld')
# tweets = get_timeline_for_user('dwnews')
# tweets = get_timeline_for_user('guardianworld')
# tweets = get_timeline_for_user('NHKWORLD_News')
# tweets = get_timeline_for_user('FT')
# tweets = get_timeline_for_user('nprworld')
# tweets = get_timeline_for_user('business')
tweets = get_timeline_for_user('BBCWorld')
sorted = mapped_topics_list = sorted(tweets['data'], key=lambda twit: calc_virality(twit['retweet_count'], twit['favorite_count'], twit['created_at'])[0], reverse=True)
for twit in tweets['data']:
  print(twit['text'])
  print(twit['created_at'])
  virality = calc_virality(twit['retweet_count'], twit['favorite_count'], twit['created_at'])
  print(virality)
  print(twit['entities']['urls'][0]['expanded_url'])
for twit in sorted:
  print(twit['text'])
  print(twit['created_at'])
  virality = calc_virality(twit['retweet_count'], twit['favorite_count'], twit['created_at'])
  print(virality)
  print(twit['entities']['urls'][0]['expanded_url'])

