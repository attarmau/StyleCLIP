import React, { useState } from 'react';
import { Tag, Maximize2 } from 'lucide-react';

const GarmentOverlay = ({ imageSrc, detectedItems }) => {
    const [hoveredIndex, setHoveredIndex] = useState(null);

    // Helper to convert normalized bounding box to percentages
    // AWS Rekognition returns normalized coords [0, 1]
    // Box: { Width, Height, Left, Top }
    const getBoxStyle = (box) => ({
        left: `${box.Left * 100}%`,
        top: `${box.Top * 100}%`,
        width: `${box.Width * 100}%`,
        height: `${box.Height * 100}%`,
    });

    return (
        <div className="relative w-full h-full group rounded-2xl overflow-hidden shadow-2xl bg-slate-900 border border-slate-800/50">
            {/* Main Image */}
            <img
                src={imageSrc}
                alt="Analyzed Input"
                className="w-full h-full object-contain max-h-[600px] transition-opacity duration-300"
            />

            {/* Overlay Layer */}
            <div className="absolute inset-0">
                {detectedItems.map((item, index) => {
                    if (!item.box) return null; // Skip if no bbox

                    const isHovered = hoveredIndex === index;

                    return (
                        <div
                            key={index}
                            className={`absolute border-2 transition-all duration-300 cursor-pointer
                ${isHovered
                                    ? 'border-white bg-white/10 z-20 shadow-[0_0_15px_rgba(255,255,255,0.5)]'
                                    : 'border-white/50 hover:border-white/80 z-10'}`}
                            style={getBoxStyle(item.box)}
                            onMouseEnter={() => setHoveredIndex(index)}
                            onMouseLeave={() => setHoveredIndex(null)}
                        >
                            {/* Tag Label Tooltip */}
                            <div
                                className={`absolute -top-10 left-1/2 -translate-x-1/2 px-3 py-1.5 
                  bg-slate-900/90 text-white text-xs font-medium rounded-lg backdrop-blur-md
                  border border-white/10 whitespace-nowrap transition-all duration-300
                  flex items-center gap-1.5 shadow-xl
                  ${isHovered ? 'opacity-100 translate-y-0 scale-100' : 'opacity-0 translate-y-2 scale-95 pointer-events-none'}`}
                            >
                                <Tag size={12} className="text-violet-400" />
                                <span className="capitalize">{item.garment_type}</span>
                                <span className="text-slate-500">|</span>
                                <span className="text-violet-200 capitalize">{item.aws_label}</span>
                            </div>

                            {/* Corner Accents for Tech Feel */}
                            {isHovered && (
                                <>
                                    <div className="absolute -top-0.5 -left-0.5 w-2 h-2 border-t-2 border-l-2 border-violet-500"></div>
                                    <div className="absolute -bottom-0.5 -right-0.5 w-2 h-2 border-b-2 border-r-2 border-violet-500"></div>
                                </>
                            )}
                        </div>
                    );
                })}
            </div>

            {/* Empty State Overlay */}
            {!imageSrc && (
                <div className="absolute inset-0 flex flex-col items-center justify-center bg-slate-100/50 backdrop-blur-sm text-slate-400 border-2 border-dashed border-slate-300 m-4 rounded-xl">
                    <Maximize2 size={48} className="mb-2 opacity-50" />
                    <p className="font-medium">Upload an image to visualize analysis</p>
                </div>
            )}
        </div>
    );
};

export default GarmentOverlay;
