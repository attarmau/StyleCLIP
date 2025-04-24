from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastmcp.server import MCPServer

# Import routes and tools
from backend.app.routes.clothing_routes import router as clothing_router
from backend.app.models.clip_classifier import classify_image_style
from backend.app.recommender import generate_recommendations
from backend.app.user_data import get_user_behavior

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Use specific frontend domain in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register all routers
app.include_router(clothing_router)

# Initialize MCP server
mcp = MCPServer(app)

@mcp.tool()
def upload_user_image(image_url: str, user_id: str):
    detected_style = classify_image_style(image_url)
    return {"style": detected_style}

@mcp.tool()
def get_style_recommendations(style: str, user_id: str):
    user_clicks = get_user_behavior(user_id)
    return generate_recommendations(style, user_clicks)

# Start if run directly
if __name__ == "__main__":
    mcp.run(transport="sse")
