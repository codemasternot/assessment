from math import inf

from graph_router import GraphRouter


def test_simple_shortest_path():
    graph = GraphRouter()
    graph.add_edge("A", "B", 2)
    graph.add_edge("B", "C", 3)
    graph.add_edge("A", "C", 10)

    cost, path = graph.shortest_path("A", "C")
    assert cost == 5
    assert path == ["A", "B", "C"]

    ok, message = graph.validate()
    assert ok, message


def test_unreachable_and_identity_queries():
    graph = GraphRouter()
    graph.add_edge("A", "B", 1)
    graph.add_edge("X", "Y", 1)

    assert graph.shortest_path("A", "A") == (0.0, ["A"])
    cost, path = graph.shortest_path("A", "Y")
    assert cost == inf
    assert path == []


def test_remove_edge_is_symmetric():
    graph = GraphRouter()
    graph.add_edge(1, 2, 7)
    graph.add_edge(2, 3, 1)

    assert graph.remove_edge(1, 2) is True
    assert 2 not in graph.neighbors(1)
    assert 1 not in graph.neighbors(2)

    ok, message = graph.validate()
    assert ok, message


def test_competing_routes_basic_case():
    graph = GraphRouter()
    graph.add_edge("S", "A", 1)
    graph.add_edge("S", "B", 4)
    graph.add_edge("A", "T", 5)
    graph.add_edge("B", "T", 1)

    cost, path = graph.shortest_path("S", "T")
    assert cost == 5
    assert path in (["S", "B", "T"],)
