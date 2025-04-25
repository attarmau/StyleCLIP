import React from 'react';

function Recommendations({ recommendations }) {
  return (
    <div className="mt-6">
      <h2 className="text-xl font-semibold">Recommended Clothes:</h2>
      <ul className="list-disc ml-6">
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
