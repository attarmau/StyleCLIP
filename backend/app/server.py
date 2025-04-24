from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.routes.clothing_routes import router as clothing_router
from backend.app.models.clip_classifier import classify_image_style
from backend.app.recommender import generate_recommendations
from backend.app.user_data import get_user_behavior
from backend.app.config.database import init_db, close_db
import uvicorn

class MCPServer:
    def __init__(self, app):
        self.app = app
        print("MCPServer initialized with app:", self.app)

    def tool(self):
        def decorator(func):
            return func
        return decorator

    def run(self, transport="sse"):
        print(f"Running MCPServer with transport: {transport}")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourfrontenddomain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(clothing_router)

mcp = MCPServer(app)

@app.on_event("startup")
async def startup_db():
    await init_db()

@app.on_event("shutdown")
async def shutdown_db():
    await close_db()

@mcp.tool()
def upload_user_image(image_url: str, user_id: str):
    try:
        detected_style = classify_image_style(image_url)
        return {"style": detected_style}
    except Exception as e:
        return {"error": f"Failed to classify image style: {str(e)}"}

@mcp.tool()
def get_style_recommendations(style: str, user_id: str):
    try:
        user_clicks = get_user_behavior(user_id)
        recommendations = generate_recommendations(style, user_clicks)
        return recommendations
    except Exception as e:
        return {"error": f"Failed to generate recommendations: {str(e)}"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
