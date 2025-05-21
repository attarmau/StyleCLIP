# FastMCP_RecSys
This is a CLIP-Based Fashion Recommender with MCP. 

### 📌 Sample Components for UI
1. Image upload
2. Submit button
3. Display clothing tags + recommendations

# Mockup
A user uploads a clothing image → YOLO detects clothing → CLIP encodes → Recommend similar

<img width="463" alt="Screenshot 2025-04-26 at 10 26 13 AM" src="https://github.com/user-attachments/assets/93c0a75b-4ed1-4fa1-b25d-5137b8eb6af0" />


# Folder Structure
```
/project-root
│
├── /backend
│   ├── Dockerfile            
│   ├── /app
│   ├── /aws
│   │   │   └── rekognition_wrapper.py         # AWS Rekognition logic
│   │   ├── /utils
│   │   │   └── image_utils.py                 # Bounding box crop utils
│   │   ├── /controllers
│   │   │   └── clothing_detector.py           # Coordinates Rekognition + cropping
│   │   ├── /tests
│   │   │   ├── test_rekognition_wrapper.py
│   │   │   └──
│   │   ├── server.py                    # FastAPI app code
│   │   ├── /routes
│   │   │   └── clothing_routes.py
│   │   ├── /controllers
│   │   │   ├── clothing_controller.py
│   │   │   ├── clothing_tagging.py
│   │   │   └── tag_extractor.py         # Pending: define core CLIP functionality
│   │   ├── schemas/
│   │   │   └── clothing_schemas.py
│   │   ├── config/
│   │   │   ├── tag_list_en.py           $ Tool for mapping: https://jsoncrack.com/editor
│   │   │   ├── database.py       
│   │   │   ├── settings.py       
│   │   │   └── api_keys.py     
│   │   └── requirements.txt      
│   └── .env                      
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
│   │   └── postcss.config.js                    
│   └── .env                                
├── docker-compose.yml                     
└── README.md 
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
Once running, the server logs a confirmation and opens the app in your browser: [http://localhost:3000/](http://localhost:3000/)

<img width="372" alt="Screenshot 2025-04-25 at 9 08 50 PM" src="https://github.com/user-attachments/assets/794a6dba-9fbb-40f1-9e57-c5c2e2af1013" />

# What’s completed so far:
1. FastAPI server is up and running (24 Apr)
2. Database connection is set up (24 Apr)
3. Backend architecture is functional (24 Apr)
4. Basic front-end UI for uploading picture (25 Apr)
## 5. Mock Testing for AWS Rekognition -> bounding box (15 May)
```
PYTHONPATH=. pytest backend/app/tests/test_rekognition_wrapper.py
```
<img width="1067" alt="Screenshot 2025-05-20 at 4 58 14 PM" src="https://github.com/user-attachments/assets/7a25a92d-2aca-42a8-abdd-194dd9d2e8a5" />

- Tested Rekognition integration logic independently using a mock → verified it correctly extracts bounding boxes only when labels match the garment set
- Confirmed the folder structure and PYTHONPATH=. works smoothly with pytest from root

## 6. Mock Testing for AWS Rekognition -> CLIP (20 May)
```
PYTHONPATH=. pytest backend/app/tests/test_clothing_tagging.py
```
<img width="1062" alt="Screenshot 2025-05-21 at 9 25 33 AM" src="https://github.com/user-attachments/assets/6c64b658-3414-4115-9e20-520132605cab" />

- Detecting garments using AWS Rekognition 

- Cropping the image around detected bounding boxes

- Tagging the cropped image using CLIP

## 7. Mock Testing for full image tagging pipeline (Image bytes → AWS Rekognition (detect garments) → Crop images → CLIP (predict tags)
```
PYTHONPATH=. pytest backend/app/tests/test_clothing_tagging.py
```
<img width="1072" alt="Screenshot 2025-05-21 at 11 19 47 AM" src="https://github.com/user-attachments/assets/b41f07f4-7926-44a3-8b64-34fe3c6ef049" />

- detect_garments: simulates AWS Rekognition returning one bounding box: {"Left": 0.1, "Top": 0.1, "Width": 0.5, "Height": 0.5}
- crop_by_bounding_box: simulates the cropping step returning a dummy "cropped_image" object
- get_tags_from_clip: simulates CLIP returning a list of tags: ["T-shirt", "Cotton", "Casual"]

Next Step:
1. Evaluate CLIP’s tagging accuracy on sample clothing images
2. Fine-tune the tagging system for better recommendations
3. Test the backend integration with real-time user data
4. Set up monitoring for model performance
5. Front-end demo
