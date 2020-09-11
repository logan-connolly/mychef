# develop stage
FROM node:lts-alpine as develop-stage
WORKDIR /srv/app
COPY package.json ./
RUN npm install
COPY . .

# build stage
FROM develop-stage as build-stage
RUN npm run build

# production stage
FROM build-stage as production-stage
RUN npm run start
RUN npm run generate
