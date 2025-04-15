import torch
from typing import List, Dict, Tuple
from clip_utils import CLIPModel

class TagExtractor:
    def __init__(self, tag_dict: Dict[str, List[str]], model_name="ViT-B/32"):
        self.clip_model = CLIPModel(model_name)
        self.tag_dict = tag_dict
        self.flattened_tags, self.tag_to_category = self._flatten_tags()
        self.tag_embeddings = self._compute_tag_embeddings()

    def _flatten_tags(self) -> Tuple[List[str], Dict[str, str]]:
        tags = []
        mapping = {}
        for category, tag_list in self.tag_dict.items():
            for tag in tag_list:
                tags.append(tag)
                mapping[tag] = category
        return tags, mapping

    def _compute_tag_embeddings(self) -> Dict[str, torch.Tensor]:
        embeddings = {}
        for tag in self.flattened_tags:
            embeddings[tag] = self.clip_model.get_text_embedding(tag)
        return embeddings

    def extract_tags(
        self, image_embedding: torch.Tensor, top_k: int = 1
    ) -> Dict[str, str]:
        tag_scores: Dict[str, float] = {}

        for tag, tag_emb in self.tag_embeddings.items():
            similarity = torch.cosine_similarity(image_embedding, tag_emb).item()
            tag_scores[tag] = similarity

        # Select top tags per category
        category_top: Dict[str, Tuple[str, float]] = {}
        for tag, score in tag_scores.items():
            category = self.tag_to_category[tag]
            if category not in category_top or score > category_top[category][1]:
                category_top[category] = (tag, score)

        return {cat: tag for cat, (tag, _) in category_top.items()}
