import torch
import clip
from PIL import Image
import requests
from io import BytesIO

model, preprocess = clip.load("ViT-B/32")
style_labels = ["streetwear", "vintage", "minimal", "formal", "kawaii"]

def classify_image_style(image_url: str) -> str:
    response = requests.get(image_url)
    image = Image.open(BytesIO(response.content)).convert("RGB")
    image_input = preprocess(image).unsqueeze(0)

    text_tokens = clip.tokenize(style_labels)

    with torch.no_grad():
        image_features = model.encode_image(image_input)
        text_features = model.encode_text(text_tokens)
        logits_per_image = (image_features @ text_features.T).softmax(dim=-1)
        best_idx = logits_per_image[0].argmax().item()

    return style_labels[best_idx]
