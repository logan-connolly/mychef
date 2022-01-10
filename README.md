## 🌱 MyChef

[![tests](https://github.com/logan-connolly/mychef/actions/workflows/test.yaml/badge.svg)](https://github.com/logan-connolly/mychef/actions)

<div align="center">
  <p>
    <a href="https://github.com/logan-connolly/mychef">
      <img src="frontend/static/mychef_example.png" alt="MyChef" />
    </a>
  </p>
</div>

## 📦 Overview

**MyChef** is an application that helps you decide what meal to make based on what you have at home. Simply enter in ingredients you have at home and get back tasty plant-based recipes from top recipe websites.

## ⚙️ Setup

_FYI: an installation of docker and docker-compose is required to run the application._

Define `.env` configuration in root directory of project to develop locally:

```
POSTGRES_USER=mychef
POSTGRES_PASSWORD=mychef
POSTGRES_DB=mychef_db
POSTGRES_HOST=db
```

## ⌨️ Commands

```shell
# Download trained ingredient extraction model
make download

# Pull application images
make pull

# Start application containers
make run

# Scrape recipes
make scrape
```

When you refresh the UI, you should start seeing recipes populating the DB and the ingredients search bar should be showing which ingredients the application has extracted thus far. To stop the scraper just `CTR-C` in the terminal with the running service.

## 🧭 Project Structure

**Api**

- Developed with [FastAPI](https://fastapi.tiangolo.com/) - fast (async support), simple and very intuitive.
- Endpoints:
  - `/sources`: website source for recipes
  - `/sources/<id>/recipes`: list of recipes from given source id
  - `/ingredients`: unique ingredients extracted from recipes (extractor trained using [spaCy](https://spacy.io/))

**Frontend**

- Developed with [Nuxt.js](https://nuxtjs.org/) an intuitive framework built on top of [Vue](https://vuejs.org/) that supports server side rendering.
- Also uses [Vuetify](https://vuetifyjs.com/en/) for component styling

**Scraper**

- Developed using [Scrapy](https://scrapy.org/) a framework for extracting data from websites.
- For each source, a `spider` needs to be defined that extracts the data and makes post request to api with recipe

**Search**

- Leverages [MeiliSearch](https://docs.meilisearch.com/) to filter recipes based on ingredient input
