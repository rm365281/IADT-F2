from domain.graph.graph import Graph
from vrp.vrp_builder import VrpFactory
from vrp.vrp import VRP

class DummyNode:
    def __init__(self, identifier):
        self.identifier = identifier

class DummyGraph(Graph):
    def __init__(self):
        self._nodes = {0: DummyNode(0)}
    def get_node(self, idx):
        return self._nodes[idx]

def test_vrp_factory_initialization():
    graph = DummyGraph()
    factory = VrpFactory(graph, population_size=10, number_vehicles=2)
    assert factory is not None

def test_create_vrp_returns_vrp_instance():
    graph = DummyGraph()
    factory = VrpFactory(graph, population_size=10, number_vehicles=2)
    vrp = factory.create_vrp()
    assert isinstance(vrp, VRP)
