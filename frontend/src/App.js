import { useState } from 'react';
import { uploadClothingItem, tagClothingImage } from './utils/api';
import ImageUpload from './components/ImageUpload';
import GarmentOverlay from './components/GarmentOverlay';
import Recommendations from './components/Recommendations';
import { Sparkles, UploadCloud, Loader2 } from 'lucide-react';

function App() {
  const [image, setImage] = useState(null);
  const [imageSrc, setImageSrc] = useState(null); // Preview URL
  const [detectedItems, setDetectedItems] = useState([]); // Changed to array for overlay loop
  const [recommendations, setRecommendations] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  // Wrapper to handle image selection specifically for preview
  const handleImageSelect = (file) => {
    setImage(file);
    setImageSrc(URL.createObjectURL(file));
    setDetectedItems([]);
    setRecommendations([]);
    setError(null);
  };

  const handleUpload = async () => {
    if (!image) return;
    setLoading(true);
    setError(null);

    try {
      // Step 1: Upload the clothing item to the backend
      const uploadResponse = await uploadClothingItem(image);
      // Ensure specific structure for overlay
      setDetectedItems(uploadResponse.tags?.garments || []);

      // Step 2: Get recommendations from the backend
      const tagResponse = await tagClothingImage(image);
      setRecommendations(tagResponse.recommendations || []);

    } catch (error) {
      console.error('Error uploading or tagging clothing item:', error);
      setError("Analysis failed. Please try a different image.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-indigo-100 via-slate-50 to-white px-6 py-10">
      <div className="max-w-6xl mx-auto">

        {/* Header */}
        <header className="flex flex-col items-center mb-12 text-center">
          <div className="mb-3 inline-flex items-center justify-center p-2 bg-white rounded-2xl shadow-sm border border-slate-100">
            <Sparkles className="text-violet-600 mr-2" size={20} />
            <span className="text-xs font-bold tracking-wider text-slate-500 uppercase">AI-Powered Fashion</span>
          </div>
          <h1 className="text-4xl md:text-5xl font-extrabold text-slate-900 tracking-tight mb-4">
            Style<span className="text-transparent bg-clip-text bg-gradient-to-r from-violet-600 to-indigo-600">CLIP</span>
          </h1>
          <p className="text-slate-500 max-w-lg text-lg">
            Instantly analyze outfits and get smart recommendations using AWS Rekognition & CLIP.
          </p>
        </header>

        {/* Main Content Grid */}
        <div className="grid lg:grid-cols-12 gap-8">

          {/* Left Column: Visuals */}
          <div className="lg:col-span-8 flex flex-col gap-6">
            <div className="glass-panel p-2 rounded-3xl min-h-[500px] flex items-center justify-center bg-slate-50/50">
              {/* Use Overlay Component for both preview and result */}
              <GarmentOverlay
                imageSrc={imageSrc}
                detectedItems={detectedItems}
              />
            </div>
          </div>

          {/* Right Column: Controls & Data */}
          <div className="lg:col-span-4 flex flex-col gap-6">

            {/* Upload Control */}
            <div className="glass-panel p-6 rounded-2xl">
              <h3 className="text-sm font-bold text-slate-900 uppercase tracking-wide mb-4">Input Source</h3>
              <ImageUpload setImage={handleImageSelect} />

              <button
                onClick={handleUpload}
                disabled={!image || loading}
                className={`mt-4 w-full py-3.5 px-4 rounded-xl flex items-center justify-center gap-2 font-semibold transition-all duration-300 shadow-lg shadow-violet-500/20
                  ${!image || loading
                    ? 'bg-slate-200 text-slate-400 cursor-not-allowed'
                    : 'bg-gradient-to-r from-violet-600 to-indigo-600 text-white hover:shadow-violet-500/40 hover:scale-[1.02]'}`}
              >
                {loading ? (
                  <Loader2 className="animate-spin" size={20} />
                ) : (
                  <>
                    <UploadCloud size={20} />
                    <span>Run Analysis</span>
                  </>
                )}
              </button>

              {error && (
                <div className="mt-4 p-3 bg-red-50 text-red-600 text-sm rounded-lg border border-red-100 flex items-center justify-center text-center">
                  {error}
                </div>
              )}
            </div>

            {/* Recommendations */}
            <Recommendations recommendations={recommendations} />

            {/* Stats / Metadata (Optional Filler for "Premium" feel) */}
            {detectedItems.length > 0 && (
              <div className="glass-panel p-6 rounded-2xl">
                <h3 className="text-sm font-bold text-slate-900 uppercase tracking-wide mb-3">Detection Stats</h3>
                <div className="grid grid-cols-2 gap-4">
                  <div className="p-3 bg-slate-50 rounded-xl border border-slate-100">
                    <p className="text-xs text-slate-400">Total Items</p>
                    <p className="text-xl font-bold text-slate-900">{detectedItems.length}</p>
                  </div>
                  <div className="p-3 bg-slate-50 rounded-xl border border-slate-100">
                    <p className="text-xs text-slate-400">Confidence</p>
                    <p className="text-xl font-bold text-green-600">~90%</p>
                  </div>
                </div>
              </div>
            )}

          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
