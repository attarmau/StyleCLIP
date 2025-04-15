import torch
import clip
from PIL import Image
from pathlib import Path

# Load the CLIP model
class CLIPModel:
    def __init__(self, model_name="ViT-B/32", device=None):
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.model, self.preprocess = clip.load(model_name, device=self.device)

    def get_image_embedding(self, image_path: Path) -> torch.Tensor:
        image = Image.open(image_path).convert("RGB")
        image_input = self.preprocess(image).unsqueeze(0).to(self.device)

        with torch.no_grad():
            image_features = self.model.encode_image(image_input)
            image_features = image_features / image_features.norm(dim=-1, keepdim=True)

        return image_features.squeeze()

    def get_text_embedding(self, texts: list[str]) -> torch.Tensor:
        text_tokens = clip.tokenize(texts).to(self.device)

        with torch.no_grad():
            text_features = self.model.encode_text(text_tokens)
            text_features = text_features / text_features.norm(dim=-1, keepdim=True)

        return text_features

    def rank_tags_by_similarity(self, image_embedding: torch.Tensor, tag_list: list[str]) -> list[tuple[str, float]]:
        text_features = self.get_text_embedding(tag_list)

        similarities = (image_embedding @ text_features.T).squeeze(0).tolist()
        ranked_tags = sorted(zip(tag_list, similarities), key=lambda x: x[1], reverse=True)
        return ranked_tags
