from PIL import Image

def crop_by_bounding_box(image: Image.Image, bbox: dict) -> Image.Image:
    width, height = image.size
    left = int(bbox["Left"] * width)
    top = int(bbox["Top"] * height)
    right = left + int(bbox["Width"] * width)
    bottom = top + int(bbox["Height"] * height)
    return image.crop((left, top, right, bottom))
