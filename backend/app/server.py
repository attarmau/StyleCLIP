from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.routes.clothing_routes import router as clothing_router
from backend.app.models.clip_model import CLIPModel
from backend.app.models.recommender import generate_recommendations
from backend.app.config.database import init_db, close_db
from backend.app.config.settings import settings
import uvicorn

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

@app.on_event("startup")
async def startup_db():
    await init_db()

@app.on_event("shutdown")
async def shutdown_db():
    await close_db()

if __name__ == "__main__":
    print(f"Starting Server on port {settings.PORT}")
    uvicorn.run("backend.app.server:app", host="0.0.0.0", port=settings.PORT, reload=True)
