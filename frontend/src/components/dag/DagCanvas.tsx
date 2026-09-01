import React from "react";
import { usePipelineStore } from "../../store/usePipelineStore";

export const DagCanvas: React.FC = () => {
  const { currentPipeline } = usePipelineStore();
  return (
    <div className="h-[calc(100vh-4rem)] bg-surface-950 p-8 flex items-center justify-center space-x-4">
      {currentPipeline.nodes.map((node) => (
        <div key={node.id} className="bg-surface-900 border border-emerald-500/40 rounded-xl p-4 w-52 shadow-lg">
          <span className="text-[10px] bg-surface-950 text-emerald-400 px-2 py-0.5 rounded font-bold">{node.type}</span>
          <h4 className="text-sm font-semibold text-white mt-2 truncate">{node.name}</h4>
        </div>
      ))}
    </div>
  );
};
