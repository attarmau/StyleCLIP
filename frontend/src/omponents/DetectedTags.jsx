import React from 'react';

function DetectedTags({ detectedItems }) {
  return (
    <div className="mt-6">
      <h2 className="text-xl font-semibold">Detected Tags:</h2>
      <ul className="list-disc ml-6">
        {Object.entries(detectedItems).map(([key, value], i) => (
          <li key={i}>
            <strong>{key}:</strong> {value}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default DetectedTags;
