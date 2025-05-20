import pytest
from unittest.mock import patch
from backend.app.aws.rekognition_wrapper import detect_garments

@patch("backend.app.aws.rekognition_wrapper.rekognition.detect_labels")
def test_detect_garments(mock_detect_labels):
    mock_detect_labels.return_value = {
        "Labels": [
            {
                "Name": "Long_Sleeved_Shirt",  # 👈 Match actual label check
                "Instances": [
                    {"BoundingBox": {"Left": 0.1, "Top": 0.1, "Width": 0.2, "Height": 0.3}}
                ]
            }
        ]
    }

    image_bytes = b"fake_image_data"
    boxes = detect_garments(image_bytes)
    assert isinstance(boxes, list)
    assert len(boxes) == 1
    assert boxes[0]["Left"] == 0.1
    assert boxes[0]["Top"] == 0.1
