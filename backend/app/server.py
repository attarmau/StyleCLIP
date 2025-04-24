# backend/app/server.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastmcp.server import MCPServer
from backend.app.routes.clothing_routes import router as clothing_router
from backend.app.models.clip_classifier import classify_image_style
from backend.app.recommender import generate_recommendations
from backend.app.user_data import get_user_behavior
from backend.app.config.database import init_db, close_db

app = FastAPI()
app.add_middleware(       # Middleware for CORS
    CORSMiddleware,
    allow_origins=["*"],  # Use specific frontend domain in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(clothing_router)
mcp = MCPServer(app)
@app.on_event("startup")
async def startup_db():
    await init_db()  # Connect to the database

@app.on_event("shutdown")
async def shutdown_db():
    await close_db()  # Close the database connection

@mcp.tool()
def upload_user_image(image_url: str, user_id: str):
    detected_style = classify_image_style(image_url)
    return {"style": detected_style}

@mcp.tool()
def get_style_recommendations(style: str, user_id: str):
    user_clicks = get_user_behavior(user_id)
    return generate_recommendations(style, user_clicks)

if __name__ == "__main__":
    mcp.run(transport="sse")
