FROM node:lts
WORKDIR /app
COPY ./codebase/package.json /app
RUN npm install
COPY ./codebase /app
CMD npm start
EXPOSE 3000
