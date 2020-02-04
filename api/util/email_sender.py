import yagmail
import os
from collections import defaultdict
import requests
import json

password = os.environ.get('EMAIL_PASSWORD')
email = os.environ.get('EMAIL_ADDRESS')
url = 'http://127.0.0.1:5000'

default_sources = requests.get(url + '/sources')
contents = ['<body>']
briefings = requests.get(url + '/briefings?limit=6')
google = requests.get(url + '/google-news?limit=6')
#print(briefings.text)
parsed_source_results = json.loads(briefings.text)["results"]
print("running")
for source in parsed_source_results:
    head = source["source"]
    summary = source["summary"]
    # print(head)
    # print(summary)
    head_string = f"<h2>{head}</h2>"
    contents.append(head_string)
    contents.append(f"{summary}")
    for article in source["articles"]:
        title = article["title"]
        date = article["date"]
        url = article["url"]
        preview = article["preview"]
        contents.append(f"<strong>{title}</strong>")
        contents.append(f"{date}")
        contents.append(f"{url}")
        contents.append(f"{preview}")
        contents.append("<br>")
    
    contents.append("<br><br>")

print("done building email")
# additional parameter attachments=filename
yagmail.SMTP(email, password).send(
    to='schweitzer.albert@gmail.com',
    subject="Here is your daily news briefing", 
    contents=contents)

print('script has runeth')
