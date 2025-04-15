# MCP_RecSys

project-root/
├── app/
├── mongo-seed/
│   ├── Dockerfile
│   └── tags.json
├── docker-compose.yml
├── Dockerfile
├── requirements.txt


Step 1: Update mongo service to add the same credentials:
  mongo:
    image: mongo:latest
    ports:
      - "27017:27017"
    environment:
      MONGO_INITDB_ROOT_USERNAME: root
      MONGO_INITDB_ROOT_PASSWORD: example
    volumes:
      - mongo-data:/data/db

Note: Since using environment variables in your FastAPI app, the Mongo URL should look like this:
MONGO_URL = "mongodb://root:example@mongo:27017"

Once it's running, open the browser and go to 👉 http://localhost:8081

Login with: Username: root / Password: example (temporarily setting)

Step 2: 
docker-compose up --build
