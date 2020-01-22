import yagmail
import os
from collections import defaultdict
import requests
import json

password = os.environ.get('EMAIL_PASSWORD')
email = os.environ.get('EMAIL_ADDRESS')
url = 'http://127.0.0.1:5000'

default_sources = requests.get(url + '/sources')
contents = []
briefings = requests.get(url + '/briefings?limit=6')
google = requests.get(url + '/google-news?limit=6')
print(briefings.text)
parsed_source_results = json.loads(briefings.text)["results"]
for source in parsed_source_results:
    head = source["source"]
    summary = source["summary"]
    contents.append(f"<h2>{head}</h2>")
    contents.append(f"{summary}")
    for article in source["articles"]:
        title = article["title"]
        date = article["date"]
        url = article["url"]
        preview = article["preview"]
        contents.append(f"<h3>{title}</h3>")
        contents.append(f"<h4>{date}</h4>")
        contents.append(f"{url}")
        contents.append(f"{preview}")
        contents.append("<br>")
    
    contents.append("<br><br>")

# additional parameter attachments=filename
yagmail.SMTP(email, password).send(
    to='schweitzer.albert@gmail.com',
    subject="Here is your daily news briefing", 
    contents=contents)
