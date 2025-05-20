# test the full pipeline from: Image bytes input→ AWS Rekognition garment detection → CLIP tag extraction for each garment crop

import pytest
from unittest.mock import patch, MagicMock
from backend.app.controllers.clothing_tagging import tag_image_with_aws_and_clip

def fake_image_bytes():
    from PIL import Image
    import io
    img = Image.new("RGB", (200, 200), color="white")
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    return buf.getvalue()

@patch("backend.app.controllers.clothing_tagging.detect_garments")
@patch("backend.app.controllers.clothing_tagging.get_tags_from_clip")
@patch("backend.app.controllers.clothing_tagging.crop_by_bounding_box")
def test_tag_image_with_aws_and_clip(mock_crop, mock_clip, mock_detect):
    image_bytes = fake_image_bytes()

    # Mock Rekognition returns one bounding box
    mock_detect.return_value = [{"Width": 0.5, "Height": 0.5, "Left": 0.1, "Top": 0.1}]
    
    # Mock crop returns a fake cropped image
    mock_crop.return_value = "cropped_image"

    # Mock CLIP tagging returns tags
    mock_clip.return_value = ["T-shirt", "Cotton", "Casual"]

    result = tag_image_with_aws_and_clip(image_bytes)

    assert len(result) == 1
    assert result[0]["tags"] == ["T-shirt", "Cotton", "Casual"]
    assert "box" in result[0]
