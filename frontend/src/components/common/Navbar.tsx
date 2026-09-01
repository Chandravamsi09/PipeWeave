import React from "react";
import { usePipelineStore } from "../../store/usePipelineStore";

export const Navbar: React.FC = () => {
  const { currentPipeline } = usePipelineStore();
  return (
    <header className="h-16 bg-surface-900 border-b border-surface-800 flex items-center justify-between px-6">
      <div className="flex items-center space-x-3">
        <div className="w-8 h-8 rounded-lg bg-emerald-500 flex items-center justify-center font-bold text-surface-950">PW</div>
        <span className="font-bold text-white text-base">PipeWeave Studio</span>
      </div>
      <span className="text-xs text-slate-400 font-mono">{currentPipeline.name}</span>
      <button className="bg-emerald-500 text-surface-950 font-bold px-4 py-1.5 rounded-lg text-xs">Execute Pipeline</button>
    </header>
  );
};
