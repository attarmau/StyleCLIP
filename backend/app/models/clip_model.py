import os
import torch
import clip
from PIL import Image
from typing import List, Tuple, Dict
from torchvision.transforms import Compose, Resize, CenterCrop, ToTensor, Normalize

device = "cuda" if torch.cuda.is_available() else "cpu"

class CLIPModel:
    def __init__(self, model_name="ViT-B/32"):
        self.model, self.preprocess = clip.load(model_name, device=device)

    def preprocess_image(self, image_path: str) -> torch.Tensor:
        image = Image.open(image_path).convert("RGB")
        return self.preprocess(image).unsqueeze(0).to(device)

    def get_image_embedding(self, image_path: str) -> torch.Tensor:
        with torch.no_grad():
            image_input = self.preprocess_image(image_path)
            image_features = self.model.encode_image(image_input)
            return image_features / image_features.norm(dim=-1, keepdim=True)

    def get_text_embedding(self, text: str) -> torch.Tensor:
        with torch.no_grad():
            text_input = clip.tokenize([text]).to(device)
            text_features = self.model.encode_text(text_input)
            return text_features / text_features.norm(dim=-1, keepdim=True)

    def batch_image_embeddings(self, image_paths: List[str]) -> Dict[str, torch.Tensor]:
        images = []
        image_map = {}

        for path in image_paths:
            try:
                img = self.preprocess_image(path)
                images.append(img)
                image_map[path] = img
            except Exception as e:
                print(f"Error processing {path}: {e}")

        if not images:
            return {}

        with torch.no_grad():
            image_batch = torch.cat(images, dim=0)
            features = self.model.encode_image(image_batch)
            features = features / features.norm(dim=-1, keepdim=True)

        return {path: features[i] for i, path in enumerate(image_map)}

    def embed_folder(self, folder_path: str) -> Dict[str, torch.Tensor]:
        image_paths = [
            os.path.join(folder_path, fname)
            for fname in os.listdir(folder_path)
            if fname.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))
        ]
        return self.batch_image_embeddings(image_paths)

    def find_similar_images(
        self, text: str, image_embeddings: Dict[str, torch.Tensor], threshold: float = 0.3
    ) -> List[Tuple[str, float]]:
        text_embedding = self.get_text_embedding(text)
        similarities = {
            path: torch.cosine_similarity(text_embedding, emb.unsqueeze(0)).item()
            for path, emb in image_embeddings.items()
        }

        sorted_matches = sorted(
            [(path, score) for path, score in similarities.items() if score >= threshold],
            key=lambda x: x[1],
            reverse=True,
        )
        return sorted_matches

    # New method for classifying image style based on predefined styles
    def classify_image_style(self, image_path: str) -> str:
        # You can define predefined styles or categories here
        predefined_styles = {
            "casual": ["jeans", "t-shirt", "sneakers"],
            "formal": ["suit", "dress shoes", "blazer"],
            "sporty": ["track pants", "sneakers", "hoodie"],
            # Add more styles as needed
        }

        # Assuming we have a way to match the image with a predefined style
        # This can be extended using the image embeddings and comparing them with style categories
        image_embedding = self.get_image_embedding(image_path)

        # Here, you can integrate logic to compare the image embedding to predefined categories
        # For simplicity, we'll return a placeholder style, or use more complex logic to classify
        # You could implement this by using cosine similarity with predefined text embeddings for styles

        # Placeholder logic for now
        return "casual"  # Example output, change based on your actual classification logic
