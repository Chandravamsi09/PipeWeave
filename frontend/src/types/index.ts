export type ExecutionMode = "BATCH" | "STREAMING" | "MICRO_BATCH";
export type NodeType = "SOURCE" | "TRANSFORM" | "QUALITY_GATE" | "SINK";
export interface DAGNode { id: string; name: string; type: NodeType; config: Record<string, any>; position: { x: number; y: number }; }
export interface Pipeline { id: string; name: string; description: string; execution_mode: ExecutionMode; is_active: boolean; nodes: DAGNode[]; edges: Array<{ id: string; source: string; target: string }>; }
