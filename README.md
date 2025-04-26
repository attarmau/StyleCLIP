# FastMCP_RecSys
This is a CLIP-Based Fashion Recommender with MCP. 

# Mockup
A user uploads a clothing image → YOLO detects clothing → CLIP encodes → Recommend similar

<img width="478" alt="Screenshot 2025-04-25 at 8 58 41 PM" src="https://github.com/user-attachments/assets/81714a44-614d-4cc1-8b95-16de984c29d7" />

# Folder Structure
```
/project-root
│
├── /backend
│   ├── Dockerfile            
│   ├── /app
│   │   ├── server.py                    # FastAPI app code
│   │   ├── /routes
│   │   │   └── clothing_routes.py
│   │   ├── /controllers
│   │   │   └── clothing_controller.py
│   │   │   └──clothing_tagging.py
│   │   │   └── tag_extractor.py         # Pending: define core CLIP functionality
│   │   ├── schemas/
│   │   │   └── clothing_schemas.py
│   │   ├── config/
│   │   │   └── tag_list_en.py
│   │   │   └── database.py       
│   │   │   └── settings.py       
│   │   │   └── api_keys.py     
│   │   └── requirements.txt      
│   └── .env                      
│                      
├── /fastmcp
│   └── app
│       └── server.py  
│
├── /frontend 
│   ├── Dockerfile        
│   ├── package.json              
│   ├── package-lock.json         
│   ├── /public
│   │   └── index.html            
│   ├── /src
│   │   ├── /components            
│   │   │   ├── ImageUpload.jsx    
│   │   │   ├── DetectedTags.jsx   
│   │   │   └── Recommendations.jsx 
│   │   ├── /utils
│   │   │   └── api.js             
│   │   ├── App.js                    # Main React component
│   │   ├── index.js
│   │   ├── index.css            
│   │   ├── tailwind.config.js        
│   │   ├── postcss.config.js        
│   │   └── .env                      
│   ├── .gitignore                    
│   ├── docker-compose.yml            
│   └── README.md                    
└────── requirements.txt

```

## Quick Start Guide
### Step 1: Clone the GitHub Project
### Step 2: Set Up the Python Environment
```
python -m venv venv
source venv/bin/activate  # On macOS or Linux
venv\Scripts\activate     # On Windows
```
### Step 3: Install Dependencies
```
pip install -r requirements.txt
```
### Step 4: Start the FastAPI Server (Backend)
```
uvicorn backend.app.server:app --reload
```
Once the server is running and the database is connected, you should see the following message in the console:
```
Database connected
INFO:     Application startup complete.
```
<img width="750" alt="Screenshot 2025-04-25 at 1 15 45 AM" src="https://github.com/user-attachments/assets/7f3fc403-fb33-4107-a00c-61796a48ecec" />

### Step 5: Install Dependencies
Database connected
INFO:     Application startup complete.
```
npm install
```
### Step 6: Start the Development Server (Frontend)
```
npm start
```
Once the server is running, you should see the following message in the console and bring you to web page: [http://localhost:3000/](http://localhost:3000/)

<img width="372" alt="Screenshot 2025-04-25 at 9 08 50 PM" src="https://github.com/user-attachments/assets/794a6dba-9fbb-40f1-9e57-c5c2e2af1013" />

### 📌 Sample Components for UI
1. Image upload
2. Submit button
3. Display clothing tags + recommendations

# What’s completed so far:
1. FastAPI server is up and running (24 Apr)
2. Database connection is set up (24 Apr)
3. Backend architecture is functional (24 Apr)
4. Basic front-end UI for uploading picture (25 Apr)

Next Step:
1. Evaluate CLIP’s tagging accuracy on sample clothing images
2. Fine-tune the tagging system for better recommendations
3. Test the backend integration with real-time user data
4. Set up monitoring for model performance
5. Front-end demo
