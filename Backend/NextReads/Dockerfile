FROM node

# Create app directory
WORKDIR /usr/app

# Install app dependencies
COPY ./package*.json ./

RUN ls /usr/app

RUN cat package.json

RUN NODE_ENV=development npm i


# Bundle app source
COPY . .

EXPOSE 4000

ENV JWTPRIVATEKEY=mysecurekey

ARG JWTPRIVATEKEY=mysecurekey

CMD [ "node" , "index.js" ]
