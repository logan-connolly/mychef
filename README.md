<div align="center">
  <p>
    <a href="https://github.com/logan-connolly/mychef">
      <img src="ui/static/mychef_example.png" alt="MyChef" />
    </a>
  </p>
</div>

## Overview

[![Build Status](https://travis-ci.com/logan-connolly/mychef.svg?branch=master)](https://travis-ci.com/logan-connolly/mychef)

**MyChef** is an application that helps you decide what meal to make based on what you have at home. Simply enter in ingredients you have at home and get back tasty plant-based recipes from top recipe websites.


## Setup

_FYI: an installation of docker and docker-compose is required to run the application._

Define `.env` configuration in root directory of project:

```
POSTGRES_USER=mychef
POSTGRES_PASSWORD=mychef
POSTGRES_DB=mychef_db
POSTGRES_HOST=db

WEB_HOST=ui
WEB_PORT=8000

SEARCH_HOST=search
SEARCH_PORT=7700

API_PORT=8002
API_INGREDIENT_MODEL=v1
```

Copy trained `spacy` ingredient extraction model into repository (~650MB>):

```
$ docker create -it --name tmp lvconnolly/mychef_model:v1 bash
$ docker cp tmp:/version ./api/app/services/models/ingredient
$ docker rm -f tmp
```

Start application locally with:

```
$ docker-compose -f ./docker-compose.dev.yml up ui -d
```

You should see a UI with no recipes loaded at `localhost:8000`. To add recipes start the web scraping service:

```
$ docker-compose -f ./docker-compose.dev.yml run scraper
```

When you refresh the UI, you should start seeing recipes populating the DB and the ingredients search bar should be showing which ingredients the application has extracted thus far. To stop the scraper just `CTR-C` in the terminal with the running service.


## Project Structure

**Api**

- Developed with [FastAPI](https://fastapi.tiangolo.com/) - fast (async support), simple and very intuitive.
- Endpoints:
  - `/sources`: website source for recipes
  - `/sources/<id>/recipes`: list of recipes from given source id
  - `/ingredients`: unique ingredients extracted from recipes (extractor trained using [spaCy](https://spacy.io/))

**UI**

- Developed with [Nuxt.js](https://nuxtjs.org/) an intuitive framework built on top of [Vue](https://vuejs.org/) that supports server side rendering.
- Also uses [Vuetify](https://vuetifyjs.com/en/) for component styling

**Scraper**

- Developed using [Scrapy](https://scrapy.org/) a framework for extracting data from websites.
- For each source, a `spider` needs to be defined that extracts the data and makes post request to api with recipe

**Search**

- Leverages [MeiliSearch](https://docs.meilisearch.com/) to filter recipes based on ingredient input
