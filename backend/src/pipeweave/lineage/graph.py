"""Column Lineage Graph"""
class LineageGraph:
    def __init__(self): self.nodes = {}; self.edges = []
    def add_column_edge(self, src_table: str, src_col: str, tgt_table: str, tgt_col: str):
        src = f"{src_table}.{src_col}"; tgt = f"{tgt_table}.{tgt_col}"
        self.nodes[src] = {"table": src_table, "column": src_col}
        self.nodes[tgt] = {"table": tgt_table, "column": tgt_col}
        self.edges.append({"source": src, "target": tgt})
    def to_dict(self): return {"nodes": self.nodes, "edges": self.edges}
