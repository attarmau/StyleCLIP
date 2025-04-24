# backend/app/models/recommender.py

import numpy as np
from typing import List, Dict
from backend.app.controllers.tag_extractor import TagExtractor
from backend.app.config.tag_list_en import GARMENT_TYPES
from backend.app.config.database import get_db  # Assuming you will implement a function to get your DB connection

# Use TagExtractor for consistent tag embedding
tag_extractor = TagExtractor(tag_dict=GARMENT_TYPES)

def encode_tags_to_embeddings(tags: Dict[str, List[str]]) -> np.ndarray:
    """
    Encode each tag value using CLIP and average to get a garment-level embedding.
    Uses TagExtractor to maintain consistent embeddings.
    """
    embeddings = []
    for category, values in tags.items():
        for tag in values:
            embedding = tag_extractor.tag_embeddings.get(tag)
            if embedding is None:
                embedding = tag_extractor.clip_model.get_text_embedding(tag)
            embeddings.append(embedding.numpy())
    if embeddings:
        return np.mean(embeddings, axis=0)
    return np.zeros(512)  # Default vector if no tags present

def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

async def get_garment_items_from_db() -> List[Dict]:
    """
    Fetch garment items from the real database.
    Modify this based on your actual database logic.
    """
    db = get_db()  # This is a placeholder, assuming you have a function to connect to your DB
    garments = await db.garments.find({}).to_list(length=100)  # Example MongoDB query to fetch garments
    return garments

async def generate_recommendations(garment_tags: List[Dict[str, List[str]]], user_clicks: List[str] = []) -> List[Dict]:
    """
    Recommend similar garments by comparing multi-tag embeddings.
    """
    results = []
    
    # Fetch real garment items from the database
    garments_from_db = await get_garment_items_from_db()
    
    for tags in garment_tags:
        garment_embedding = encode_tags_to_embeddings(tags)

        # Compare with database garments
        similarities = []
        for db_item in garments_from_db:
            db_embedding = encode_tags_to_embeddings(db_item['tags'])
            similarity = cosine_similarity(garment_embedding, db_embedding)
            similarities.append((similarity, db_item))

        top_matches = sorted(similarities, key=lambda x: x[0], reverse=True)[:3]
        results.append({
            "input_tags": tags,
            "recommendations": [match[1] for match in top_matches]
        })

    return results
