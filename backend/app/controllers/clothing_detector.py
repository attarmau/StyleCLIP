from io import BytesIO
from PIL import Image
from backend.app.aws.rekognition_wrapper import detect_garments
from backend.app.utils.image_utils import crop_from_normalized_bbox

def detect_and_crop_garments(image_bytes: bytes) -> list[Image.Image]:
    image = Image.open(BytesIO(image_bytes)).convert("RGB")
    bounding_boxes = detect_garments(image_bytes)

    cropped_images = []
    for bbox in bounding_boxes:
        cropped = crop_from_normalized_bbox(image, bbox)
        cropped_images.append(cropped)
    return cropped_images
