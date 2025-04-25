import { useState } from 'react';
import { uploadClothingItem, tagClothingImage } from './utils/api';
import ImageUpload from './components/ImageUpload';
import DetectedTags from './components/DetectedTags';
import Recommendations from './components/Recommendations';

function App() {
  const [image, setImage] = useState(null);
  const [detectedItems, setDetectedItems] = useState([]);

  const handleUpload = async () => {
    const reader = new FileReader();
    reader.onloadend = async () => {
      const base64Image = reader.result.split(',')[1];

      const payload = {
        filename: image.name,
        image_base64: base64Image
      };

      const res = await fetch('http://localhost:8000/clothing/upload', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      const data = await res.json();
      setDetectedItems(data.tags || {});
    };

    if (image) {
      reader.readAsDataURL(image);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center p-6">
      <h1 className="text-2xl font-bold mb-4">Clothing Recommender</h1>

      <input
        type="file"
        accept="image/*"
        onChange={(e) => setImage(e.target.files[0])}
        className="mb-4"
      />
      <button
        onClick={handleUpload}
        className="bg-blue-500 text-white px-4 py-2 rounded shadow"
      >
        Submit
      </button>

      {detectedItems && (
        <div className="mt-6 w-full max-w-md bg-white p-4 rounded shadow">
          <h2 className="text-xl font-semibold mb-2">Detected Tags:</h2>
          <ul className="list-disc ml-6 space-y-1">
            {Object.entries(detectedItems).map(([key, value]) => (
              <li key={key}>
                <strong>{key}:</strong> {value}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default App;
