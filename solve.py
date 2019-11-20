"""
This program accepts a graph defined in a text file and finds the shortest path between given vertices.

Input format:
V_start,V_finish
Number_of_edges_given_below
V0,V_start,Weight1
...
V_finish,V32,WeightN

Output format (if the solution exists):
V1,V3,V2,V9
Minimal_weight

Output format (if the solution doesn't exist):
No
"""

import argparse
import math


def main():
    args = parse_arguments()
    solver = DijkstraShortestPathSolver.create_from_file(args.input)
    solver.solve()
    solver.write_to_file(args.output)


def parse_arguments():
    parser = argparse.ArgumentParser(description='Shortest path between two cities')
    parser.add_argument('input', type=str, help='input file path')
    parser.add_argument('--output', type=str, default='test.out', help='output file path')
    return parser.parse_args()


class DijkstraShortestPathSolver:
    """
    The Dijkstra algorithm for finding the shortest paths between vertices in a graph
    https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
    """

    def __init__(self, edge_to_weight, start_vertex, finish_vertex):
        self._edge_to_weight = edge_to_weight
        self._start_vertex = start_vertex
        self._finish_vertex = finish_vertex
        self._graph = {}
        self._vertex_to_min_weight = {}
        self.path = None
        self.min_weight = None

    @classmethod
    def create_from_file(cls, filepath):
        edge_to_weight = {}
        with open(filepath, 'r', encoding='utf-8') as fp:
            words = fp.readline().split(',')
            start_vertex, finish_vertex = words[0].strip(), words[1].strip()
            n = int(fp.readline().strip())
            for line in fp:
                words = line.split(',')
                edge = Edge(words[0].strip(), words[1].strip())
                edge_to_weight[edge] = float(words[2].strip())
        if len(edge_to_weight) != n:
            raise Error(f'invalid file {filepath}')
        return cls(edge_to_weight, start_vertex, finish_vertex)

    def solve(self):
        self._build_graph()
        self._calculate_min_weight_to_all_vertices()
        if self.min_weight < math.inf:
            self._find_shortest_path()

    def write_to_file(self, filepath):
        with open(filepath, 'w', encoding='utf-8') as fp:
            if self.path is None:
                fp.write('No\n')
            else:
                fp.write(','.join(self.path) + '\n')
                fp.write(f'{self.min_weight}\n')

    def _build_graph(self):
        for edge in self._edge_to_weight:
            u, v = edge.u, edge.v
            self._graph[u] = self._graph.get(u, set())
            self._graph[u].add(v)
            self._graph[v] = self._graph.get(v, set())
            self._graph[v].add(u)

    def _calculate_min_weight_to_all_vertices(self):
        self._vertex_to_min_weight = {vertex: math.inf for vertex in self._graph}
        self._vertex_to_min_weight[self._start_vertex] = 0

        unchecked_vertices = set(self._graph.keys())
        while unchecked_vertices:
            current_vertex = min(unchecked_vertices, key=lambda vertex: self._vertex_to_min_weight[vertex])
            vertices = self._graph[current_vertex]
            vertices = vertices.intersection(unchecked_vertices)
            vertices = sorted(vertices, key=lambda vertex: self._edge_to_weight[Edge(current_vertex, vertex)])
            for vertex in vertices:
                edge = Edge(current_vertex, vertex)
                min_duration = self._vertex_to_min_weight[current_vertex] + self._edge_to_weight[edge]
                if min_duration < self._vertex_to_min_weight[vertex]:
                    self._vertex_to_min_weight[vertex] = min_duration
            unchecked_vertices.remove(current_vertex)

        self.min_weight = self._vertex_to_min_weight[self._finish_vertex]

    def _find_shortest_path(self):
        self.path = [self._finish_vertex]
        current_vertex = self._finish_vertex
        weight = self.min_weight
        while not math.isclose(weight, 0):
            vertices = self._graph[current_vertex]
            for vertex in vertices:
                edge = Edge(current_vertex, vertex)
                if math.isclose(weight - self._edge_to_weight[edge], self._vertex_to_min_weight[vertex]):
                    self.path.append(vertex)
                    weight -= self._edge_to_weight[edge]
                    current_vertex = vertex
                    break
        self.path.reverse()


class Edge:

    def __init__(self, u, v):
        self.u = u
        self.v = v

    def __eq__(self, other):
        return (
            self.u, self.v == other.u, other.v
            or self.u, self.v == other.v, other.u)

    def __hash__(self):
        return hash(self.u) ^ hash(self.v)


class Error(Exception):
    pass


if __name__ == '__main__':
    main()
