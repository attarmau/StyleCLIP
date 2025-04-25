import React from 'react';

function ImageUpload({ setImage }) {
  const handleImageChange = (e) => {
    setImage(e.target.files[0]);
  };

  return (
    <div className="mb-4">
      <input
        type="file"
        accept="image/*"
        onChange={handleImageChange}
        className="mb-4"
      />
    </div>
  );
}

export default ImageUpload;
