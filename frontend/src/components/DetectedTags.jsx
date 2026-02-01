import React from 'react';

const DetectedTags = ({ detectedItems }) => {
  return (
    <div className="mt-6 w-full max-w-md bg-white p-4 rounded shadow">
      <h2 className="text-xl font-semibold mb-2">Detected Tags:</h2>
      <ul className="list-disc ml-6 space-y-1">
        {detectedItems.map((tag, index) => (
          <li key={index}>
            <strong>{tag.label}:</strong> {tag.value}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default DetectedTags;
