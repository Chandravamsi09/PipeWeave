import React from "react";
import { Navbar } from "./components/common/Navbar";
import { DagCanvas } from "./components/dag/DagCanvas";

export const App: React.FC = () => {
  return (
    <div className="h-screen w-screen flex flex-col bg-surface-950 text-slate-100 font-sans">
      <Navbar />
      <main className="flex-1"><DagCanvas /></main>
    </div>
  );
};
export default App;
