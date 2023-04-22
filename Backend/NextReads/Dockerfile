FROM node

# Create app directory
WORKDIR /usr/app

# Install app dependencies
COPY Backend/NextReads/package*.json ./

RUN NODE_ENV=development npm i

# Bundle app source
COPY . .

RUN ls /usr/app/

RUN ls/usr/app/Backend/NextReads

WORKDIR /usr/app/Backend/NextReads

EXPOSE 4000

ENV JWTPRIVATEKEY=mysecurekey

ARG JWTPRIVATEKEY=mysecurekey

CMD [ "node" , "index.js" ]
