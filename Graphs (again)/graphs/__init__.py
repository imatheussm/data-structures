from graphs.Graph import *
from graphs.MatrixGraph import *
from graphs.ListGraph import *


def to_list_graph(graph):
    if graph.is_list:
        return graph

    list_graph = ListGraph(graph.vertices, graph.is_directed, graph.is_pondered)

    for edge in graph.edges:
        list_graph.add_edge(*edge)

    return list_graph


def to_matrix_graph(graph):
    if graph.is_matrix:
        return graph

    matrix_graph = MatrixGraph(graph.vertices, graph.is_directed, graph.is_pondered)

    for edge in graph.edges:
        matrix_graph.add_edge(*edge)

    return matrix_graph
