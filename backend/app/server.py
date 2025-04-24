from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastmcp.app.server import MCPServer
from backend.app.routes.clothing_routes import router as clothing_router
from backend.app.models.clip_classifier import classify_image_style
from backend.app.recommender import generate_recommendations
from backend.app.user_data import get_user_behavior
from backend.app.config.database import init_db, close_db
import uvicorn

app = FastAPI()

# Middleware for CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourfrontenddomain.com"],  # Use your actual frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include clothing routes
app.include_router(clothing_router)

# Initialize the MCPServer separately
mcp = MCPServer(app)

@app.on_event("startup")
async def startup_db():
    """
    Start-up event to connect to the database.
    """
    await init_db()

@app.on_event("shutdown")
async def shutdown_db():
    """
    Shutdown event to close the database connection.
    """
    await close_db()

# MCP tools for image upload and recommendation generation
@mcp.tool()
def upload_user_image(image_url: str, user_id: str):
    """
    Upload user image and classify the style.
    """
    try:
        detected_style = classify_image_style(image_url)
        return {"style": detected_style}
    except Exception as e:
        return {"error": f"Failed to classify image style: {str(e)}"}

@mcp.tool()
def get_style_recommendations(style: str, user_id: str):
    """
    Get style recommendations based on the user's behavior.
    """
    try:
        user_clicks = get_user_behavior(user_id)
        recommendations = generate_recommendations(style, user_clicks)
        return recommendations
    except Exception as e:
        return {"error": f"Failed to generate recommendations: {str(e)}"}

# Running FastAPI with Uvicorn instead of mcp.run()
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
