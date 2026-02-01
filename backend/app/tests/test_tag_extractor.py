from PIL import Image
from backend.app.controllers.tag_extractor import TagExtractor, get_tags_from_clip
from backend.app.config.tag_list_en import garment_types

image_path = "/Users/judyhuang/Downloads/StyleCLIP-main/image_3.png"  
image = Image.open(image_path)

tag_extractor = TagExtractor(tag_dict=garment_types, model_name="ViT-B/32")

result = tag_extractor.get_tags_from_image(image)
print("Pipeline result:", result)

tags = get_tags_from_clip(image)
print("Top tags from CLIP:", tags)