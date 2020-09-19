<div align="center">
  <p>
    <a href="https://github.com/logan-connolly/mychef">
      <img src="ui/static/mychef.png" alt="MyChef" />
    </a>
  </p>
  <p>
    <a href="https://travis-ci.com/logan-connolly/mychef">
      <img src="https://travis-ci.com/logan-connolly/mychef.svg?branch=master" alt="Travis"/>
    </a>
  </p>
</div>

## TL;DR

**MyChef** is an application that helps you decide what meal to make based on what you have at home. Simply enter in your ingredients and get back tasty plant-based recipes from top recipe websites.

## Setup

Define configuration in root directory of project:

```
# .env with example values

POSTGRES_USER=mychef
POSTGRES_PASSWORD=mychef
POSTGRES_DB=mychef_db
POSTGRES_HOST=db
API_PORT=8002
WEB_PORT=8000
MODEL=ingredients_v1
```

Start application locally with:

```
# Warning: will build all images

$ docker-compose up -d
```

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
