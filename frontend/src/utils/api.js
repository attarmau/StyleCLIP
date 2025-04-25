const convertImageToBase64 = (image) => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onloadend = () => {
      resolve(reader.result.split(',')[1]);
    };
    reader.onerror = (error) => reject(error);
    reader.readAsDataURL(image);
  });
};

export const uploadClothingItem = async (image) => {
  try {
    const base64Image = await convertImageToBase64(image);

    const payload = {
      filename: image.name,
      image_base64: base64Image,
    };

    const response = await fetch("http://localhost:8000/clothing/upload", {
      method: "POST",
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      throw new Error("Failed to upload clothing item");
    }

    return await response.json();
  } catch (error) {
    console.error("Error uploading clothing item:", error);
    throw error;
  }
};

export const tagClothingImage = async (image) => {
  try {
    const base64Image = await convertImageToBase64(image);

    const payload = {
      image_base64: base64Image,
    };

    const response = await fetch("http://localhost:8000/clothing/tag", {
      method: "POST",
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      throw new Error("Failed to tag clothing image");
    }

    return await response.json();
  } catch (error) {
    console.error("Error tagging clothing image:", error);
    throw error;
  }
};
