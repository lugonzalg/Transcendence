FROM node:20.10

WORKDIR /Trascendence
COPY package.json package.json
RUN npm install

RUN apt-get update
RUN apt-get install jq -y

RUN curl -k -H "X-Vault-Token: hvs.Dd77um8uAHucsxDQwx6RQSoz" https://127.0.0.1:8200/v1/transcendence/data/vue | jq -r '.data.data | to_entries[] | "\(.key)=\(.value)"' > .env

CMD ["/bin/bash", "-c", "npm run serve"]

