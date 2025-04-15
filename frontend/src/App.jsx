import { useState } from 'react';

function App() {
  const [image, setImage] = useState(null);
  const [tags, setTags] = useState([]);
  const [recommendations, setRecommendations] = useState([]);

  const handleUpload = async () => {
    const formData = new FormData();
    formData.append("image", image);

    const res = await fetch("http://localhost:8000/upload", {
      method: "POST",
      body: formData,
    });

    const data = await res.json();
    setTags(data.tags || []);
    setRecommendations(data.recommendations || []);
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

      {tags.length > 0 && (
        <div className="mt-6">
          <h2 className="text-xl font-semibold">Detected Tags:</h2>
          <ul className="list-disc ml-6">
            {tags.map((tag, i) => (
              <li key={i}>{tag}</li>
            ))}
          </ul>
        </div>
      )}

      {recommendations.length > 0 && (
        <div className="mt-6">
          <h2 className="text-xl font-semibold">Recommended Clothes:</h2>
          <ul className="list-disc ml-6">
            {recommendations.map((item, i) => (
              <li key={i}>{item.name}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default App;
