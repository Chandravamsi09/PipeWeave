import { create } from "zustand";
import { Pipeline } from "../types";

interface PipelineState { currentPipeline: Pipeline; activeTab: string; setActiveTab: (tab: string) => void; }
export const usePipelineStore = create<PipelineState>((set) => ({
  currentPipeline: {
    id: "pipe-ecom-stream",
    name: "E-Commerce Real-Time Order Stream",
    description: "Kafka Ingest -> Null Cleanse -> Quality Gate -> Revenue Agg -> ClickHouse",
    execution_mode: "STREAMING",
    is_active: true,
    nodes: [
      { id: "source_kafka", name: "Kafka Orders Topic", type: "SOURCE", config: {}, position: { x: 100, y: 150 } },
      { id: "clean_nulls", name: "Cleanse Null Values", type: "TRANSFORM", config: {}, position: { x: 380, y: 150 } },
      { id: "quality_gate", name: "Validate Non-Zero Price", type: "QUALITY_GATE", config: {}, position: { x: 660, y: 150 } },
      { id: "revenue_agg", name: "Tumbling Revenue Window", type: "TRANSFORM", config: {}, position: { x: 940, y: 150 } },
      { id: "sink_clickhouse", name: "ClickHouse Analytics Sink", type: "SINK", config: {}, position: { x: 1220, y: 150 } },
    ],
    edges: [
      { id: "e1-2", source: "source_kafka", target: "clean_nulls" },
      { id: "e2-3", source: "clean_nulls", target: "quality_gate" },
      { id: "e3-4", source: "quality_gate", target: "revenue_agg" },
      { id: "e4-5", source: "revenue_agg", target: "sink_clickhouse" },
    ]
  },
  activeTab: "canvas",
  setActiveTab: (tab) => set({ activeTab: tab }),
}));
