from typing import List, Dict, Optional
from PIL import Image
from backend.app.aws.rekognition_wrapper import rekognition
from backend.app.controllers.clothing_tagging import crop_by_bounding_box
from backend.app.controllers.tag_extractor import get_tags_from_clip

class InferencePipeline:
    """
    Automated image recognition pipeline combining AWS Rekognition for detection
    and CLIP for fine-grained tagging/classification.
    """
    
    def __init__(self, min_confidence: int = 50):
        self.min_confidence = min_confidence
        self.rekognition = rekognition

    def process_image(self, image: Image.Image, image_bytes: bytes) -> List[Dict]:
        """
        Run the end-to-end inference pipeline on an image.
        
        Args:
            image: PIL Image object (for specific cropping/tagging)
            image_bytes: Raw bytes (for AWS Rekognition)
            
        Returns:
            List of detected garments with tags.
        """
        # Step 1: Detect with Rekognition
        try:
            response = self.rekognition.detect_labels(
                Image={'Bytes': image_bytes},
                MinConfidence=self.min_confidence
            )
        except Exception as e:
            # Log error or re-raise
            print(f"Pipeline Rekognition Error: {e}")
            raise e

        # Step 2: Process results
        results = []
        seen_garment_types = set()

        aws_labels = response.get("Labels", [])
        
        # If no labels found, try whole-image fallback
        if not aws_labels:
            return [self._process_single_crop(image, None, None)]

        for label in aws_labels:
            for instance in label.get("Instances", []):
                box = instance.get("BoundingBox")
                if not box:
                    continue

                # Deduplicate loosely based on garment type from CLIP
                # (In a real pipeline we might use IoU on boxes)
                result = self._process_single_crop(image, box, label.get("Name"))
                
                if result["garment_type"] in seen_garment_types:
                    continue
                
                seen_garment_types.add(result["garment_type"])
                results.append(result)

        # Fallback if detection found labels but no instances with boxes
        if not results:
             results.append(self._process_single_crop(image, None, None))
             
        return results

    def _process_single_crop(self, original_image: Image.Image, box: Optional[Dict], aws_label: Optional[str]) -> Dict:
        """
        Helper to crop and tag a specific region.
        """
        if box:
            cropped = crop_by_bounding_box(original_image, box)
        else:
            cropped = original_image

        tags_result = get_tags_from_clip(cropped)
        
        return {
            "aws_label": aws_label,
            "box": box,
            "garment_type": tags_result.get("garment_type", "Unknown"),
            "tags": {k: v[:10] for k, v in tags_result.get("tags", {}).items()}
        }
