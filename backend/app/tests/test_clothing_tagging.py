# test the full pipeline from: Image bytes input→ AWS Rekognition garment detection → CLIP tag extraction for each garment crop

import pytest
from unittest.mock import patch

from PIL import Image
import io

from backend.app.controllers.clothing_tagging import tag_image_with_aws_and_clip

def fake_image_bytes():
    img = Image.new("RGB", (200, 200), color="white")
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    return buf.getvalue()

@patch("backend.app.controllers.clothing_tagging.detect_garments")
@patch("backend.app.controllers.clothing_tagging.get_tags_from_clip")
@patch("backend.app.controllers.clothing_tagging.crop_by_bounding_box")
def test_tag_image_with_aws_and_clip(mock_crop, mock_clip, mock_detect):
    image_bytes = fake_image_bytes()

    mock_detect.return_value = [{"Width": 0.5, "Height": 0.5, "Left": 0.1, "Top": 0.1}]
    mock_crop.return_value = "cropped_image"
    mock_clip.return_value = ["T-shirt", "Cotton", "Casual"]

    result = tag_image_with_aws_and_clip(image_bytes)

    assert len(result) == 1
    assert result[0]["tags"] == ["T-shirt", "Cotton", "Casual"]
    assert "box" in result[0]

@patch("backend.app.controllers.clothing_tagging.detect_garments")
def test_no_garments_detected(mock_detect):
    mock_detect.return_value = []
    result = tag_image_with_aws_and_clip(fake_image_bytes())
    assert result == []

@patch("backend.app.controllers.clothing_tagging.detect_garments")
@patch("backend.app.controllers.clothing_tagging.get_tags_from_clip")
@patch("backend.app.controllers.clothing_tagging.crop_by_bounding_box")
def test_clip_returns_no_tags(mock_crop, mock_clip, mock_detect):
    mock_detect.return_value = [{"Width": 0.5, "Height": 0.5, "Left": 0.1, "Top": 0.1}]
    mock_crop.return_value = "cropped_image"
    mock_clip.return_value = []

    result = tag_image_with_aws_and_clip(fake_image_bytes())
    assert len(result) == 1
    assert result[0]["tags"] == []

@patch("backend.app.controllers.clothing_tagging.detect_garments")
def test_aws_rekognition_failure(mock_detect):
    mock_detect.side_effect = Exception("AWS Rekognition Error")

    with pytest.raises(RuntimeError, match="AWS Rekognition failed: AWS Rekognition Error"):
        tag_image_with_aws_and_clip(fake_image_bytes())

def test_invalid_image_format():
    invalid_bytes = b"not an image at all"
    with pytest.raises(ValueError, match="Invalid image format"):
        tag_image_with_aws_and_clip(invalid_bytes)
