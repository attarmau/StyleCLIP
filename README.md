# FastMCP_RecSys
This is a CLIP-Based Fashion Recommender with MCP. 

# Scenario
A user uploads a clothing image → YOLO detects clothing → CLIP encodes → Recommend similar

# Folder Structure
```
/project-root
│
├── /backend
│   ├── Dockerfile            
│   ├── /app
│   │   ├── server.py             # FastAPI app code
│   │   ├── /routes
│   │   │   └── clothing_routes.py
│   │   ├── /controllers
│   │   │   └── clothing_controller.py
│   │   │   └── tag_extractor.py  # for processing the tags and interacting with the CLIPModel
│   │   ├── schemas/
│   │   │   └── clothing_schemas.py
│   │   ├── config/
│   │   │   └── tag_list_en.py
│   │   │   └── database.py       (pending for DB configurations
│   │   │   └── settings.py       (pending for environment variables or application-wide settings)
│   │   │   └── api_keys.py       (pending for API keys or other sensitive data)
│   │   └── requirements.txt      # Python dependencies for the backend
│   └── .env                      # Environment variables (make sure to add this to .gitignore)
│
├── /frontend
│   ├── Dockerfile        
│   ├── package.json              # Node.js dependencies (for React)
│   ├── package-lock.json         # Lock file for React dependencies
│   ├── /public
│   │   └── index.html            # HTML file for the frontend (React app is mounted here)
│   ├── /src
│   │   ├── App.js                # Main React component
│   │   └── index.js              # React entry point
│   ├── tailwind.config.js        # Tailwind CSS config
│   ├── postcss.config.js         # PostCSS config
│   └── .env                      # Frontend environment variables (add to .gitignore)
│
├── .gitignore                    # Git ignore file (include .env, node_modules, etc.)
├── docker-compose.yml            # Docker Compose configuration
└── README.md                     # Project documentation


```

## Step 1

Update mongo service to add the same credentials:
```
  mongo:
    image: mongo:latest
    ports:
      - "27017:27017"
    environment:
      MONGO_INITDB_ROOT_USERNAME: root
      MONGO_INITDB_ROOT_PASSWORD: example
    volumes:
      - mongo-data:/data/db
```

Note: Since using environment variables in the FastAPI app, the Mongo URL should look like this:
MONGO_URL = "mongodb://root:example@mongo:27017"

Once it's running, open the browser and go to 👉 http://localhost:8081

Login with: Username: root / Password: example (temporarily setting)

## Step 2
docker-compose up --build

This will:

- Start FastAPI backend with hot reload
- Start MongoDB
- Start Mongo Express (for DB UI) (Frontend will not be built automatically in this mode)

## Step 3
- Access the frontend (React app) at:  http://localhost:3000
- Access the backend (FastAPI app) at:  http://localhost:8000

### 📌 Quick Tips

Visit your app at: http://localhost:8000/docs

View MongoDB UI: http://localhost:8081 (use user: root, password: example)

mongo-seed runs only once at startup to populate your tags collection.

### 📌 Sample Components for UI

1. Image upload
2. Submit button
3. Display clothing tags + recommendations
