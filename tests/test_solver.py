import math

import pytest

from solve import DijkstraShortestPathSolver, Edge, Error


def test_valid_file_reading():
    edge_to_weight = {
        Edge('1', '2'): 7,
        Edge('1', '3'): 9,
        Edge('1', '6'): 14,
        Edge('2', '3'): 10,
        Edge('2', '4'): 15,
        Edge('3', '4'): 11,
        Edge('3', '6'): 2,
        Edge('4', '5'): 6,
        Edge('5', '6'): 9,
    }
    solver = DijkstraShortestPathSolver.create_from_file('tests/valid.in')
    assert solver._edge_to_weight == edge_to_weight


def test_invalid_file_reading():
    with pytest.raises(Error):
        DijkstraShortestPathSolver.create_from_file('tests/invalid.in')


def test_connected_graph():
    edge_to_weight = {
        Edge('1', '2'): 7,
        Edge('1', '3'): 9,
        Edge('1', '6'): 14,
        Edge('2', '3'): 10,
        Edge('2', '4'): 15,
        Edge('3', '4'): 11,
        Edge('3', '6'): 2,
        Edge('4', '5'): 6,
        Edge('5', '6'): 9,
    }
    solver = DijkstraShortestPathSolver(edge_to_weight, '1', '5')
    solver.solve()
    assert math.isclose(solver.min_weight, 20)
    assert solver.path == ['1', '3', '6', '5']


def test_disconnected_graph():
    edge_to_weight = {
        Edge('1', '2'): 7,
        Edge('1', '3'): 9,
        Edge('1', '6'): 14,
        Edge('2', '3'): 10,
        Edge('3', '6'): 2,
        Edge('4', '5'): 6,
    }
    solver = DijkstraShortestPathSolver(edge_to_weight, '1', '5')
    solver.solve()
    assert solver.path is None
