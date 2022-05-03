Heads up: this repo is currently a work in progress.

Imagine an evening news cast personalized to your interests...

This application is an experiment with news aggregation and summarization. The goal is to replicate the experience of a newscaster or news team aggregating the most important news items related to a subject (e.g. world news or NASA) and aggregating them into a summary of summaries. 

The API has an extractor which pulls raw data from RSS feeds and extracts the content using BeautifulSoup. Articles are then sanitized and keywords are extracted using `nltk` and `gensim`. However this method is limited to Python 2.7 and does not yield the kind of results we could get from modern NLP techniques. 

This branch has two goals: to implement a modern keyword extraction and topic mapping pipeline using `huggingface` and `tensorflow` as well migrating away from AWS to reduce compute costs. To that end `content_fixer.py` and `topic_mapper.py` demonstrate the new pipeline using tensorflow. This pipeline is being tested on a Raspberry Pi 4 with a refactor to isolate incompatibility issues with the current environment. The extraction pipeline is being migrated to a Raspberry Pi 3B. 

Down the line the idea would be to expose the summarization service to a cloud hosted API for consumption by the frontend, thereby containing costs by isolating the heavy lifting to the on-prem RPis.

## Build and Run
### API 
1. Install and run with conda from the environment.yml file (`conda create -n news-feeder -f environment.yml`)

Note: For the API you may have to run `pip install flask-cors --upgrade` for `flask_cors` to work correctly ([see this issue.] (https://github.com/corydolphin/flask-cors/issues/194))

### Vue Frontend
1. Install node modules with `yarn`.
2. Run the application with `yarn serve`.

### React Frontend
1. Install node modules with `yarn`.
2. Run the application with `yarn start`. 
