from feeder.emailer.emailer import run_digest
from feeder.util import firebase
from feeder.models.source import active_topics, topics_by_key, custom_google_source

sources = firebase.get_default_sources()
customFeeds = firebase.get_custom_feeds()
users = firebase.get_users()
mapped_users = []
for user in users.values():
  if 'briefingIsActive' not in user or user['briefingIsActive'] == False:
    continue
  if 'sources' in user and len(user['sources']) > 0:
    mapped_keys = list(map(lambda source: sources[source]["key"], user['sources']))
    mapped_sources = list(map(lambda key: topics_by_key[key], mapped_keys))
  else:
    mapped_sources = active_topics
  if 'customFeeds' in user and len(user['customFeeds']) > 0:
    for key in user['customFeeds']:
      config = customFeeds[key]
      query_string =  "+".join(config['keywords'])
      custom_feed = custom_google_source(query_string, config['description'])
      mapped_sources.append(custom_feed)
  user['email_sources'] = mapped_sources
  mapped_users.append(user)

run_digest(mapped_users)