import boto3
from botocore.exceptions import BotoCoreError, ClientError
from typing import List, Dict

rekognition = boto3.client("rekognition")

def detect_garments(image_bytes: bytes, max_labels=10) -> List[Dict]:
    try:
        response = rekognition.detect_labels(
            Image={"Bytes": image_bytes},
            MaxLabels=max_labels,
            MinConfidence=70,
        )
        garment_instances = []
        for label in response["Labels"]:
            if label["Name"].lower() in {"dress", "long_sleeved_dress", "long_sleeved_outwear", "long_sleeved_shirt", "short_sleeved_outwear", "short_sleeved_shirt", "skirt", "shorts", "trousers", "vest", "vest_dress"}:
                for instance in label.get("Instances", []):
                    if "BoundingBox" in instance:
                        garment_instances.append(instance["BoundingBox"])
        return garment_instances
    except (BotoCoreError, ClientError) as e:
        raise RuntimeError(f"Rekognition failed: {e}")
