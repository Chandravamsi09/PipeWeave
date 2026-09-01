"""Test Cycle Detection"""
import pytest
from pipeweave.engine.graph import DAG, DAGNode
from pipeweave.core.exceptions import DAGCycleError

def test_dag_cycle_detection():
    dag = DAG(name="CycleDAG")
    dag.add_node(DAGNode("A", "Node A", "TRANSFORM"))
    dag.add_node(DAGNode("B", "Node B", "TRANSFORM"))
    dag.add_edge("A", "B")
    dag.add_edge("B", "A")
    with pytest.raises(DAGCycleError):
        dag.topological_sort()
