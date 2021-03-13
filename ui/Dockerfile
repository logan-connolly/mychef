# develop stage
FROM node:lts-alpine as develop-stage
WORKDIR /srv/app
COPY package.json ./
RUN apk --update-cache add --virtual build-deps python make g++ \
    && npm install \
    && apk del build-deps
COPY . .

# production stage
FROM develop-stage as production-stage
RUN npm run build
ENTRYPOINT ["npm"]
CMD ["run", "start"]
