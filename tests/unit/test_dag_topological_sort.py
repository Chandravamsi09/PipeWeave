"""Test Topological Sort"""
from pipeweave.engine.graph import DAG, DAGNode

def test_linear_topological_sort():
    dag = DAG(name="LinearDAG")
    dag.add_node(DAGNode("src", "Source", "SOURCE"))
    dag.add_node(DAGNode("trans", "Transform", "TRANSFORM"))
    dag.add_node(DAGNode("sink", "Sink", "SINK"))
    dag.add_edge("src", "trans")
    dag.add_edge("trans", "sink")
    assert dag.topological_sort() == ["src", "trans", "sink"]

def test_diamond_tiers():
    dag = DAG(name="DiamondDAG")
    dag.add_node(DAGNode("root", "Root", "SOURCE"))
    dag.add_node(DAGNode("b1", "Branch 1", "TRANSFORM"))
    dag.add_node(DAGNode("b2", "Branch 2", "TRANSFORM"))
    dag.add_node(DAGNode("join", "Join", "SINK"))
    dag.add_edge("root", "b1")
    dag.add_edge("root", "b2")
    dag.add_edge("b1", "join")
    dag.add_edge("b2", "join")
    tiers = dag.compute_execution_tiers()
    assert len(tiers) == 3
    assert tiers[0] == ["root"]
    assert set(tiers[1]) == {"b1", "b2"}
    assert tiers[2] == ["join"]
