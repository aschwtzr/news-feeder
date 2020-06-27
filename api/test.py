from feeder.formatter.debug_parser import print_source_articles
from feeder.emailer.emailer import run_digest
import datetime
# print_source_articles()

# user settings coming soon! 
albert = {
  'email': 'schweitzer.albert@gmail.com',
  'sources': ['guardian', 'bbc',  'dw', 'google'],
  'experimental': True,
  'keywords': False,
  'debug': True,
  'limit': 8
}

mansi = {
  'email': 'mansidhamija24@gmail.com',
  'sources': ['guardian', 'bbc', 'dw', 'google'],
  'keywords': True,
  'debug': False,
  'limit': 8,
  'experimental': True
}

marisel= {
  'email': 'marisel.schweitzer@gmail.com',
  'sources': ['guardian', 'bbc', 'dw', 'google'],
  'keywords': True,
  'debug': False,
  'limit': 8,
  'experimental': True
}

alberto= {
  'email': 'kerygma01@yahoo.com',
  'sources': ['guardian', 'bbc', 'dw', 'google'],
  'keywords': True,
  'debug': False,
  'limit': 8,
  'experimental': True
}

harald= {
  'email': 'heschwei@gmail.com',
  'sources': ['guardian', 'bbc', 'dw', 'google'],
  'keywords': True,
  'debug': False,
  'limit': 8,
  'experimental': True
}

timestamp = datetime.datetime.now()
print('script is runnint at ' + timestamp.strftime("%m/%d/%Y, %H:%M:%S"))

users = [albert, mansi, marisel, alberto, harald]
#users = [albert]
run_digest(users)
print('emails sent')
