import React from 'react';
import { ShoppingBag, ArrowRight } from 'lucide-react';

function Recommendations({ recommendations }) {
  return (
    <div className="w-full glass-panel rounded-2xl p-6">
      <div className="flex items-center gap-2 mb-4">
        <ShoppingBag className="text-violet-600" size={20} />
        <h2 className="text-lg font-bold text-slate-800">Smart Recommendations</h2>
      </div>

      <div className="grid gap-3">
        {recommendations.length === 0 ? (
          <p className="text-slate-400 text-sm italic">No recommendations yet. Upload an image to start.</p>
        ) : (
          recommendations.map((item, i) => (
            <div key={i} className="group flex items-center justify-between p-3 rounded-xl bg-white border border-slate-100 shadow-sm hover:shadow-md transition-all cursor-pointer">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-lg bg-slate-100 flex items-center justify-center text-lg">
                  👗
                </div>
                <div>
                  <p className="font-semibold text-slate-700 text-sm">{item.garment_name || "Similar Item"}</p>
                  <p className="text-xs text-slate-400">Match Score: 98%</p>
                </div>
              </div>
              <ArrowRight size={16} className="text-slate-300 group-hover:text-violet-500 transform group-hover:translate-x-1 transition-all" />
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default Recommendations;
