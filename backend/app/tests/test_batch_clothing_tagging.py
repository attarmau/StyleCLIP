import os
from PIL import Image
from backend.app.controllers.clothing_tagging import crop_by_bounding_box
from backend.app.controllers.tag_extractor import get_tags_from_clip
from backend.app.aws.rekognition_wrapper import rekognition

IMAGE_FOLDER = "Your images folder route"

MIN_CONFIDENCE = 50

def tag_image_per_garment(image_path: str, min_confidence=MIN_CONFIDENCE):
    """
    For a given image, return separate tags for each unique garment type detected.
    Uses AWS Rekognition for detection, CLIP for tagging.
    """
    with open(image_path, "rb") as f:
        image_bytes = f.read()
    image = Image.open(image_path).convert("RGB")

    results = []
    seen_garment_types = set()  

    try:
        response = rekognition.detect_labels(Image={'Bytes': image_bytes}, MinConfidence=min_confidence)
        
    except Exception as e:
        print(f"AWS Rekognition error: {e}")
        response = {"Labels": []}

    for label in response.get("Labels", []):
        for instance in label.get("Instances", []):
            box = instance.get("BoundingBox")
            if not box:
                continue
            cropped = crop_by_bounding_box(image, box)
            tags_result = get_tags_from_clip(cropped)
            g_type = tags_result.get("garment_type", "Unknown")

            # Avoid duplicates
            if g_type in seen_garment_types:
                continue
            seen_garment_types.add(g_type)

            results.append({
                "aws_label": label.get("Name", "Unknown"),
                "box": box,
                "garment_type": g_type,
                "tags": {k: v[:3] for k, v in tags_result.get("tags", {}).items()}  # Top 3 per category
            })

    # Fallback if no garments detected
    if not results:
        tags_result = get_tags_from_clip(image)
        results.append({
            "aws_label": None,
            "box": None,
            "garment_type": tags_result.get("garment_type", "Unknown"),
            "tags": {k: v[:3] for k, v in tags_result.get("tags", {}).items()}
        })

    return results

if __name__ == "__main__":
    image_files = sorted([f for f in os.listdir(IMAGE_FOLDER) if f.lower().endswith((".jpg", ".jpeg", ".png"))])

    for img_file in image_files:
        img_path = os.path.join(IMAGE_FOLDER, img_file)
        print(f"[Image] {img_file}")

        try:
            garment_results = tag_image_per_garment(img_path)
            if not garment_results:
                print("  No garments detected by AWS Rekognition.")
            else:
                for idx, g in enumerate(garment_results, 1):
                    print(f"  Garment {idx}:")
                    print(f"   Type: {g['garment_type']}")
                    for cat, tags in g['tags'].items():
                        print(f"    {cat}: {tags}")
        except Exception as e:
            print(f"  Error processing image: {e}")

        print("\n")
