from api.feeder.common.source import google, guardian, reuters, yahoo, bbc, dw, custom_google_source

users = {
  1: {
    'id': 1,
    'name': 'Albert',
    'sources': ['google', 'venezuela'],
    'email': 'schweitzer.albert@gmail.com'
  }
}

def load_preferences(user_id):
 prefs = users[user_id]
 print(prefs)

def fetch_feeds():
  preferences = load_preferences(1)
  google.get_feed_articles()


# def get_feed_from(source):
