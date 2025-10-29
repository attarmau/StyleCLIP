import os
import torch
import clip
from PIL import Image
from typing import List, Dict

device = "cuda" if torch.cuda.is_available() else "cpu"

class CLIPModel:
    def __init__(self, model_name="ViT-B/32"):
        self.model, self.preprocess = clip.load(model_name, device=device)

    def preprocess_pil_image(self, pil_image: Image.Image) -> torch.Tensor:
        """
        Preprocess a PIL image for CLIP model input.
        """
        image = pil_image.convert("RGB")
        return self.preprocess(image).unsqueeze(0).to(device)

    def get_image_embedding_from_pil(self, pil_image: Image.Image) -> torch.Tensor:
        """
        Get normalized CLIP embedding from a PIL image.
        """
        with torch.no_grad():
            image_input = self.preprocess_pil_image(pil_image)
            image_features = self.model.encode_image(image_input)
            return image_features / image_features.norm(dim=-1, keepdim=True)

    def get_text_embedding(self, text: str) -> torch.Tensor:
        """
        Get normalized CLIP embedding for a text string.
        """
        with torch.no_grad():
            text_input = clip.tokenize([text]).to(device)
            text_features = self.model.encode_text(text_input)
            return text_features / text_features.norm(dim=-1, keepdim=True)

    def batch_image_embeddings(self, image_paths: List[str]) -> Dict[str, torch.Tensor]:
        """
        Compute embeddings for a list of image paths.
        Returns a dict mapping image path to embedding tensor.
        """
        images = []
        image_map = {}

        for path in image_paths:
            try:
                img = Image.open(path).convert("RGB")
                img_tensor = self.preprocess_pil_image(img)
                images.append(img_tensor)
                image_map[path] = img_tensor
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
        """
        Compute embeddings for all images in a folder.
        """
        image_paths = [
            os.path.join(folder_path, fname)
            for fname in os.listdir(folder_path)
            if fname.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))
        ]
        return self.batch_image_embeddings(image_paths)
