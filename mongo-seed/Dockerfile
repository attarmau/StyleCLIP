FROM mongo:latest
COPY tags.json /tags.json
CMD mongoimport --host mongo --username root --password example --authenticationDatabase admin --db fashion_db --collection tags --jsonArray --file /tags.json
