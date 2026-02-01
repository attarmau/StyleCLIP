import React from 'react';

const ImageUpload = ({ setImage }) => {
  const handleImageChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setImage(file);
    }
  };

  return (
    <div className="mb-4">
      <input
        type="file"
        accept="image/*"
        onChange={handleImageChange}
        className="block text-sm text-gray-500"
      />
    </div>
  );
};

export default ImageUpload;
