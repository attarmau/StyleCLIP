export const uploadClothingItem = async (image) => {
  const formData = new FormData();
  formData.append("image", image);

  const response = await fetch("http://localhost:8000/clothing/upload", {
    method: "POST",
    body: formData,
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
  const formData = new FormData();
  formData.append("image", image);

  const response = await fetch("http://localhost:8000/clothing/tag", {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    throw new Error("Failed to tag clothing image");
  }

  return await response.json();
};
