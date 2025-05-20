import torch
from typing import List, Dict, Tuple
from backend.app.models.clip_model import CLIPModel
from backend.app.config.tag_list_en import garment_types
from PIL import Image

class TagExtractor:
    def __init__(self, tag_dict: Dict[str, Dict[str, List[str]]], model_name="ViT-B/32"):
        self.clip_model = CLIPModel(model_name)
        self.tag_dict = tag_dict
        self.garment_types = list(tag_dict.keys())  # e.g., ["Tops", "Pants", "Skirts", ...]
        self.garment_type_embeddings = self._compute_garment_type_embeddings()

    def _compute_garment_type_embeddings(self) -> Dict[str, torch.Tensor]:
        embeddings = {}
        for g_type in self.garment_types:
            embeddings[g_type] = self.clip_model.get_text_embedding(f"a photo of {g_type.lower()}")
        return embeddings

    def determine_garment_type(self, image_embedding: torch.Tensor) -> str:
        best_score = float("-inf")
        best_type = "Unknown"
        for g_type, g_emb in self.garment_type_embeddings.items():
            score = torch.cosine_similarity(image_embedding, g_emb).item()
            if score > best_score:
                best_score = score
                best_type = g_type
        return best_type

    def extract_tags(self, image_embedding: torch.Tensor, garment_type: str, top_k: int = 1) -> Dict[str, str]:
        tag_scores: Dict[str, float] = {}

        tag_categories = self.tag_dict.get(garment_type, {})
        flattened_tags = []
        tag_to_category = {}
        for category, tags in tag_categories.items():
            for tag in tags:
                flattened_tags.append(tag)
                tag_to_category[tag] = category

        for tag in flattened_tags:
            tag_emb = self.clip_model.get_text_embedding(tag)
            similarity = torch.cosine_similarity(image_embedding, tag_emb).item()
            tag_scores[tag] = similarity

        category_top: Dict[str, Tuple[str, float]] = {}
        for tag, score in tag_scores.items():
            category = tag_to_category[tag]
            if category not in category_top or score > category_top[category][1]:
                category_top[category] = (tag, score)

        return {cat: tag for cat, (tag, _) in category_top.items()}

    def get_tags_from_image(self, image: Image.Image, top_k: int = 1) -> Dict[str, str]:
        image_embedding = self.clip_model.get_image_embedding(image)
        garment_type = self.determine_garment_type(image_embedding)
        tags = self.extract_tags(image_embedding, garment_type, top_k=top_k)
        return {
            "garment_type": garment_type,
            "tags": tags
        }

def get_tags_from_clip(image: Image.Image, top_k: int = 1) -> Dict[str, str]:
    extractor = TagExtractor(tag_dict=garment_types)
    return extractor.get_tags_from_image(image, top_k=top_k)
