Heads up: this repo is currently a work in progress.

Imagine an evening news cast personalized to your interests...

This application is an experiment with news aggregation and summarization. The goal is to replicate the experience of a newscaster or news team aggregating the most important news items related to a subject (e.g. world news or NASA) and aggregating them into a summary of summaries. 

It is a news feed web app and backend built with React and Flask. 

To run all services you will need an  key for SMMRY.

## Build and Run
### API 
1. Install pipenv and run `pipenv install`.
2. Run the Flask API with:
`FLASK_ENV=development SUMMRY_KEY=[summary API key] pipenv run flask run`
(set the environment to dev)(start the pipenv environment)(start the Flask app)

### Vue Frontend
1. Install node modules with `yarn`.
2. Run the application with `yarn serve`.

### React Frontend
1. Install node modules with `yarn`.
2. Run the application with `yarn start`. 
