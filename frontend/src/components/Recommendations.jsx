import React from 'react';

function Recommendations({ recommendations }) {
  return (
    <div className="mt-6 w-full max-w-md bg-white p-4 rounded shadow">
      <h2 className="text-xl font-semibold mb-2">Recommended Clothes:</h2>
      <ul className="list-disc ml-6 space-y-1">
        {recommendations.map((item, i) => (
          <li key={i}>
            <strong>{item.garment_name}</strong>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Recommendations;
