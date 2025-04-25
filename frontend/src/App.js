import { useState } from 'react';
import { uploadClothingItem, tagClothingImage } from './utils/api';
import ImageUpload from './components/ImageUpload';
import DetectedTags from './components/DetectedTags';
import Recommendations from './components/Recommendations';

function App() {
  const [image, setImage] = useState(null);
  const [detectedItems, setDetectedItems] = useState({});
  const [recommendations, setRecommendations] = useState([]);

  const handleUpload = async () => {
    try {
      // Step 1: Upload the clothing item to the backend
      const uploadResponse = await uploadClothingItem(image);
      setDetectedItems(uploadResponse.tags || {});

      // Step 2: Get recommendations from the backend
      const tagResponse = await tagClothingImage(image);
      setRecommendations(tagResponse.recommendations || []);
    } catch (error) {
      console.error('Error uploading or tagging clothing item:', error);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center p-6">
      <h1 className="text-2xl font-bold mb-4">Clothing Recommender</h1>

      <ImageUpload setImage={setImage} />

      <button
        onClick={handleUpload}
        className="bg-blue-500 text-white px-4 py-2 rounded shadow"
      >
        Submit
      </button>

      {Object.keys(detectedItems).length > 0 && (
        <DetectedTags detectedItems={detectedItems} />
      )}

      {recommendations.length > 0 && <Recommendations recommendations={recommendations} />}
    </div>
  );
}
export default App;
