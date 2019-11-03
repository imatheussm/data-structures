from graphs.Graph import *
from graphs.ListGraph import *
from graphs.MatrixGraph import *


def to_list_graph(graph):
    """Converts a Graph object into a ListGraph.

    Parameters
    ----------

    graph : Graph

        A Graph object. If the Graph object is already a ListGraph, it will just be returned.

    Returns
    -------

    ListGraph

        A ListGraph object.
    """
    if graph.is_list:
        return graph

    list_graph = ListGraph(graph.vertices, graph.is_directed, graph.is_pondered)

    for edge in graph.edges:
        list_graph.add_edge(*edge)

    return list_graph


def to_matrix_graph(graph):
    """Converts a Graph object into a MatrixGraph.

    Parameters
    ----------

    graph : Graph

        A Graph object. If the Graph object is already a MatrixGraph, it will just be returned.

    Returns
    -------

    MatrixGraph

        A MatrixGraph object.
    """
    if graph.is_matrix:
        return graph

    matrix_graph = MatrixGraph(graph.vertices, graph.is_directed, graph.is_pondered)

    for edge in graph.edges:
        matrix_graph.add_edge(*edge)

    return matrix_graph
