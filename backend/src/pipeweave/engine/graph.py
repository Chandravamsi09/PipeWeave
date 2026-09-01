"""DAG Graph Engine"""
from typing import Dict, List, Set, Optional, Any, Tuple
from collections import defaultdict, deque
import uuid
import copy
from ..core.exceptions import DAGCycleError, DAGValidationError

class DAGNode:
    def __init__(self, node_key: str, name: str, node_type: str, config: Optional[Dict[str, Any]] = None, retry_limit: int = 3, retry_delay_seconds: float = 5.0, timeout_seconds: int = 3600, position: Optional[Tuple[float, float]] = None):
        self.node_key = node_key
        self.name = name
        self.node_type = node_type
        self.config = config or {}
        self.retry_limit = retry_limit
        self.retry_delay_seconds = retry_delay_seconds
        self.timeout_seconds = timeout_seconds
        self.position = position or (0.0, 0.0)

    def to_dict(self):
        return {"node_key": self.node_key, "name": self.name, "node_type": self.node_type, "config": self.config, "position": self.position}

    @classmethod
    def from_dict(cls, data):
        return cls(node_key=data["node_key"], name=data.get("name", data["node_key"]), node_type=data.get("node_type", "TRANSFORM"), config=data.get("config", {}))

class DAGEdge:
    def __init__(self, source_key: str, target_key: str, condition_expression: Optional[str] = None):
        self.source_key = source_key
        self.target_key = target_key
        self.condition_expression = condition_expression

class DAG:
    def __init__(self, dag_id: Optional[str] = None, name: str = "PipelineDAG"):
        self.dag_id = dag_id or str(uuid.uuid4())
        self.name = name
        self.nodes: Dict[str, DAGNode] = {}
        self.edges: List[DAGEdge] = []
        self._adjacency_list = defaultdict(list)
        self._reverse_adjacency_list = defaultdict(list)
        self._in_degrees = defaultdict(int)

    def add_node(self, node: DAGNode):
        if node.node_key in self.nodes: raise DAGValidationError(f"Duplicate node: {node.node_key}")
        self.nodes[node.node_key] = node
        if node.node_key not in self._in_degrees: self._in_degrees[node.node_key] = 0

    def add_edge(self, source_key: str, target_key: str, condition_expression: Optional[str] = None):
        if source_key not in self.nodes or target_key not in self.nodes: raise DAGValidationError("Node does not exist in DAG")
        if source_key == target_key: raise DAGCycleError(f"Self loop on {source_key}")
        for e in self.edges:
            if e.source_key == source_key and e.target_key == target_key: return
        edge = DAGEdge(source_key, target_key, condition_expression)
        self.edges.append(edge)
        self._adjacency_list[source_key].append(target_key)
        self._reverse_adjacency_list[target_key].append(source_key)
        self._in_degrees[target_key] += 1

    def get_upstream_nodes(self, node_key: str): return list(self._reverse_adjacency_list.get(node_key, []))
    def get_downstream_nodes(self, node_key: str): return list(self._adjacency_list.get(node_key, []))

    def topological_sort(self) -> List[str]:
        in_deg = copy.deepcopy(self._in_degrees)
        queue = deque([k for k, node in self.nodes.items() if in_deg[k] == 0])
        order = []
        while queue:
            curr = queue.popleft()
            order.append(curr)
            for n in self._adjacency_list[curr]:
                in_deg[n] -= 1
                if in_deg[n] == 0: queue.append(n)
        if len(order) != len(self.nodes):
            raise DAGCycleError("Cycle detected in DAG graph")
        return order

    def compute_execution_tiers(self) -> List[List[str]]:
        self.topological_sort()
        in_deg = copy.deepcopy(self._in_degrees)
        curr_tier = [k for k in self.nodes.keys() if in_deg[k] == 0]
        tiers = []
        while curr_tier:
            tiers.append(curr_tier)
            next_tier = []
            for k in curr_tier:
                for neighbor in self._adjacency_list[k]:
                    in_deg[neighbor] -= 1
                    if in_deg[neighbor] == 0: next_tier.append(neighbor)
            curr_tier = next_tier
        return tiers

    def validate(self) -> bool:
        if not self.nodes: raise DAGValidationError("No nodes defined in DAG")
        self.topological_sort()
        return True
