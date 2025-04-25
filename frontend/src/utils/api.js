export const uploadClothingItem = async (image) => {
  const reader = new FileReader();
  reader.onloadend = async () => {
    const base64Image = reader.result.split(',')[1];  // Get base64 part of the image

    const payload = {
      filename: image.name,
      image_base64: base64Image
    };

    const response = await fetch("http://localhost:8000/clothing/upload", {
      method: "POST",
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      throw new Error("Failed to upload clothing item");
    }

    return await response.json();
  };

  if (image) {
    reader.readAsDataURL(image);  // Converts the image to base64
  }
};

export const tagClothingImage = async (image) => {
  const reader = new FileReader();
  reader.onloadend = async () => {
    const base64Image = reader.result.split(',')[1];  // Get base64 part of the image

    const payload = {
      image_base64: base64Image
    };

    const response = await fetch("http://localhost:8000/clothing/tag", {
      method: "POST",
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      throw new Error("Failed to tag clothing image");
    }

    return await response.json();
  };

  if (image) {
    reader.readAsDataURL(image);  // Converts the image to base64
  }
};
