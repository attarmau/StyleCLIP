from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.routes.clothing_routes import router as clothing_router
from backend.app.models.clip_model import CLIPModel
from backend.app.models.recommender import generate_recommendations
from backend.app.config.database import init_db, close_db
from backend.app.config.settings import settings
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
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(clothing_router)

clip_model = CLIPModel()

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
        embedding = clip_model.get_image_embedding(image_url)
        detected_style = "mock_style"
        return {"style": detected_style}
    except Exception as e:
        return {"error": f"Failed to classify image style: {str(e)}"}

@mcp.tool()
def get_style_recommendations(style: str, user_id: str):
    try:
        user_clicks = ["floral", "loose-fit", "cotton"]  # mock data
        recommendations = generate_recommendations(style, user_clicks)
        return recommendations
    except Exception as e:
        return {"error": f"Failed to generate recommendations: {str(e)}"}

if __name__ == "__main__":
    print(f"Starting MCPServer on port {settings.PORT}")
    uvicorn.run("backend.app.server:app", host="0.0.0.0", port=settings.PORT, reload=True)
