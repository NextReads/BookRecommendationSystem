FROM node
RUN ls ./
# Create app directory
WORKDIR /usr/app

# Install app dependencies
COPY package*.json ./

RUN ls ./

RUN ls ../

RUN ls ../../

RUN ls ../../../


RUN NODE_ENV=development npm i


# Bundle app source
COPY . .

EXPOSE 4000

ENV JWTPRIVATEKEY=mysecurekey

ARG JWTPRIVATEKEY=mysecurekey

CMD [ "node" , "index.js" ]
