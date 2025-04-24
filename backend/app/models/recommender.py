# recommender.py
import numpy as np
from typing import List, Dict
from backend.app.models.clip_model import CLIPModel
import json
import os

clip_model = CLIPModel()

# Load predefined tag embeddings (mocked for now)
TAG_EMBEDDINGS_PATH = "backend/app/data/tag_embeddings.json"

if os.path.exists(TAG_EMBEDDINGS_PATH):
    with open(TAG_EMBEDDINGS_PATH, "r") as f:
        TAG_EMBEDDINGS = json.load(f)
else:
    TAG_EMBEDDINGS = {}  # fallback if file doesn't exist


def encode_tags_to_embeddings(tags: Dict[str, List[str]]) -> np.ndarray:
    """
    Encode each tag value using CLIP and average to get garment-level embedding.
    """
    embeddings = []
    for category, values in tags.items():
        for tag in values:
            if tag in TAG_EMBEDDINGS:
                embeddings.append(np.array(TAG_EMBEDDINGS[tag]))
            else:
                embeddings.append(clip_model.get_text_embedding(tag))
    if embeddings:
        return np.mean(embeddings, axis=0)
    return np.zeros(512)  # default vector


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


def generate_recommendations(garment_tags: List[Dict[str, List[str]]], user_clicks: List[str] = []) -> List[Dict]:
    """
    Recommend similar garments by comparing multi-tag embeddings.
    """
    results = []
    for tags in garment_tags:
        garment_embedding = encode_tags_to_embeddings(tags)

        # Compare with database embeddings (mocked here)
        similarities = []
        for db_item in MOCK_DB_ITEMS:
            db_embedding = encode_tags_to_embeddings(db_item['tags'])
            similarity = cosine_similarity(garment_embedding, db_embedding)
            similarities.append((similarity, db_item))

        top_matches = sorted(similarities, key=lambda x: x[0], reverse=True)[:3]
        results.append({
            "input_tags": tags,
            "recommendations": [match[1] for match in top_matches]
        })

    return results


# MOCKED DB GARMENT ENTRIES (for testing)
MOCK_DB_ITEMS = [
    {
        "id": "1",
        "tags": {
            "category": ["Top"],
            "fabric": ["Knit"],
            "silhouette": ["Boxy"],
            "fit": ["Loose fit"],
            "color": ["Ivory"]
        }
    },
    {
        "id": "2",
        "tags": {
            "category": ["Pants"],
            "fabric": ["Denim"],
            "silhouette": ["Skinny"],
            "fit": ["Tight fit"],
            "color": ["Navy"]
        }
    },
    # Add more items as needed
]
