# backend/app/main.py
from fastapi import FastAPI
from fastmcp.server import MCPServer
from typing import List
from app.models.clip_classifier import classify_image_style
from app.recommender import generate_recommendations
from app.user_data import get_user_behavior
from router import router

app = FastAPI()
app.include_router(router)
mcp = MCPServer(app)

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
