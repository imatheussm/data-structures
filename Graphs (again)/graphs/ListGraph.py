import scipy as sp

from graphs import Graph


class ListGraph(Graph):
    """The Graph abstract data structure, implemented via adjacency lists. Extends the Graph superclass."""

    def __init__(self, vertices, is_directed, is_pondered):
        """Initializes the ListGraph class.

        This object calls Graph() to initialize parameters and definitions that are common to both Graph
        implementations.

        Parameters
        ----------

        vertices : iterable

            The vertices to be contained in the Graph object.

        is_directed : bool

            Whether the Graph object being initialized is directed. This can be changed later on through the
            Graph.is_directed setter.

        is_pondered : bool

            Whether the Graph object being initialized is pondered.This can be changed later on through the
            Graph.is_pondered setter.

        Returns
        -------

        ListGraph

            A ListGraph object.
        """
        super().__init__(is_directed, is_pondered)

        self.vertices_list = {str(vertex): {} for vertex in vertices}

    def __getitem__(self, vertex):
        """Returns the adjacency of a given vertex using the [] syntax.

        This is a safe implementation, given that ListGraph.__setitem__() is not defined. As such, any attempts of
        assignment of new values would result in a TypeError.

        Parameters
        ----------

        vertex : float or int or str

            The vertex whose adjacency is to be obtained.

        Returns
        -------

        dict

            The adjacency of a given vertex in a ListGraph object.
        """
        return self.vertices_list.__getitem__(str(vertex))

    def __repr__(self):
        """Returns a representation of the ListGraph object.

        Returns
        -------

        str

            The string representation of the object to be printed by the Python interpreter.
        """
        max_length = sp.fromiter(
            (len(str(vertex)) for vertex in self.vertices), int, len(self)
        ).max()

        representation = "<ListGraph object>\n"

        for vertex in self.vertices:
            if self.is_pondered:
                adjacency = [
                    f"{destination}: {weight}"
                    for destination, weight in self[vertex].items()
                ]
            else:
                adjacency = [f"{destination}" for destination in self[vertex].keys()]
            representation += (
                str(vertex).ljust(max_length, " ")
                + " -> "
                + ", ".join(adjacency)
                + "\n"
            )

        return representation

    @property
    def is_matrix(self):
        """Returns whether the Graph object is a MatrixGraph.

        Returns
        -------

        bool

            Whether the Graph object is a MatrixGraph.
        """
        return False

    @property
    def is_list(self):
        """Returns whether the Graph object is a ListGraph.

        Returns
        -------

        bool

            Whether the Graph object is a ListGraph.
        """
        return True

    @property
    def is_pondered(self):
        """Returns whether the ListGraph object is pondered.

        Returns
        -------

        bool

            Whether the ListGraph object is pondered.
        """
        return self._pondered

    @is_pondered.setter
    def is_pondered(self, pondered):
        """Changes the pondered property of the Graph, performing the required operations if needed.

        Parameters
        ----------

        pondered : bool

            Whether the Graph will be pondered.

        Raises
        ------

        TypeError

            When the object attributed is not of type bool.
        """
        if type(pondered) is not bool:
            raise TypeError("This property should receive a boolean value.")

        if self._pondered != pondered:
            self._pondered = pondered

            if not pondered:
                for origin in self.vertices:
                    for destination in self[origin].keys():
                        if self[origin][destination] != 0:
                            self[origin][destination] = 1

    def is_edge(self, origin, destination):
        """Returns whether a given edge is contained in the ListGraph object.

        Parameters
        ----------

        origin : float or int or str

            The origin vertex. Given that all vertices labels are treated as strings, this parameter will be casted
            to string prior to the verification.

        destination : float or int or str

            The destination vertex. Given that all vertices labels are treated as strings, this parameter will be
            casted to string prior to the verification.

        Returns
        -------

        bool

            Whether there is an edge that links the provided vertices in the ListGraph object.
        """
        origin, destination = str(origin), str(destination)

        try:
            if self.vertices_list[origin][destination]:
                return True
            else:
                return False
        except KeyError:
            return False

    def transpose(self):
        """Returns a transposed copy of the ListGraph object.

        Raises
        ------

        TypeError

            When the ListGraph object is non-directed, its transposed version is equal to itself. This implementation
            opted to raise an error instead of just returning itself, although this could change in the future.

        Returns
        -------

        ListGraph

            A ListGraph object with its edges transposed.
        """
        if not self.is_directed:
            raise TypeError("Non-directed graphs can't be transposed.")

        transposed_edges = tuple(((edge[1], edge[0], edge[2:]) for edge in self.edges))

        transposed_graph = ListGraph(self.vertices, self.is_directed, self.is_pondered)

        for edge in transposed_edges:
            transposed_graph.add_edge(*edge)

        return transposed_graph

    def add_edge(self, origin, destination, weight=1):
        """Adds an edge to the ListGraph object.

        Parameters
        ----------

        origin : float or int or str

            The origin vertex. Given that all vertices labels are treated as strings, this parameter will be casted
            to string prior to the addition.

        destination : float or int or str

            The destination vertex. Given that all vertices labels are treated as strings, this parameter will be
            casted to string prior to the addition.

        weight : float or int

            The weight of the edge. In non-pondered Graph objects this parameter is ignored. If not provided,
            it will default to 1.

        Raises
        ------

        ValueError

            When either a loop creation attempt has been made in a non-directed graph, or the edge already exists (
            multigraphs are not supported currently), or either of the vertices is not contained in the ListGraph
            object, or when the weight is 0.
        """
        origin, destination = str(origin), str(destination)

        if not self.is_directed and origin == destination:
            raise ValueError("Non-directed graphs cannot have loops.")
        if self.is_edge(origin, destination):
            raise ValueError("This edge already exists.")
        if not self.is_vertex(origin) or not self.is_vertex(destination):
            raise ValueError("Non-existent vertex. Add it first and try again.")

        if self.is_pondered:
            if weight == 0:
                raise ValueError("The weight must be a non-null number.")

            self.vertices_list[origin][destination] = float(weight)

            if not self.is_directed:
                self.vertices_list[destination][origin] = float(weight)
        else:
            self.vertices_list[origin][destination] = 1.0

            if not self.is_directed:
                self.vertices_list[destination][origin] = 1.0

    def remove_edge(self, origin, destination):
        """Removes an edge of the ListGraph object.

        Parameters
        ----------

        origin : float or int or str

            The origin vertex. Given that all vertices labels are treated as strings, this parameter will be casted
            to string prior to the addition.

        destination : float or int or str

            The destination vertex. Given that all vertices labels are treated as strings, this parameter will be
            casted to string prior to the addition.

        Raises
        ------

        ValueError

            When either the edge or either of the vertices do not exist.
        """
        if not self.is_edge(origin, destination):
            raise ValueError("This edge does not exist.")

        origin, destination = str(origin), str(destination)

        if origin not in self.vertices or destination not in self.vertices:
            raise ValueError("Non-existent vertex. Add it first and try again.")

        del self.vertices_list[origin][destination]

        if not self.is_directed:
            del self.vertices_list[destination][origin]

    @property
    def number_of_edges(self):
        """Returns the number of edges of the ListGraph object.

        Returns
        -------

        int

            The number of edges contained in the ListGraph object.
        """
        edge_counter = 0

        for vertex in self.vertices:
            edge_counter += len(self.vertices_list[vertex].keys())

        if not self.is_directed:
            return int(edge_counter / 2)
        return int(edge_counter)

    def degree_of(self, vertex):
        """Returns the degree of a given vertex the ListGraph object.

        Parameters
        ----------

        vertex : float or int or str

            The vertex. Given that all vertices labels are treated as strings, this parameter will be casted to
            string prior to the verification.

        Raises
        ------

        ValueError

            When the vertex is not contained in the ListGraph object.

        Returns
        -------

        int or tuple of int

            The degree or (in-degree, out-degree) of the vertex in the ListGraph object.
        """
        vertex = str(vertex)

        if not self.is_vertex(vertex):
            raise ValueError("Non-existent vertex. Add it first and try again.")

        out_degree = len(self.vertices_list[vertex].keys())

        if self.is_directed:
            in_degree = 0

            for v in self.vertices:
                if vertex in self.vertices_list[v].keys():
                    in_degree += 1

            return in_degree, out_degree

        return out_degree

    def adjacency_of(self, vertex, with_weight=True):
        """Returns the adjacency of a given vertex in a ListGraph object.

        Parameters
        ----------

        vertex : float or int or str

            The vertex on which the search shall begin. Given that all vertices labels are treated as strings,
            this parameter will be casted to string prior to the verification.

        with_weight : bool

            Whether to return, if applicable, the edge weights of the ListGraph object that link the vertex to its
            adjacency.

        Raises
        ------

        ValueError

            When the vertex is not contained in the ListGraph object.

        Returns
        -------

        tuple(tuple of (str, int) or str)

            The adjacency of the vertex with the weights (if applicable) contained in the ListGraph object.
        """
        if not self.is_vertex(vertex):
            raise ValueError("Non-existent vertex. Add it first and try again.")

        if (
            type(vertex) is not list
            and type(vertex) is not tuple
            and type(vertex) is not set
        ):
            if self.is_pondered and with_weight:
                return tuple(sorted(list(self[vertex].items()), key=lambda x: x[-1]))

            return tuple(sorted(list(self[vertex].keys())))
        else:
            adjacency = []
            vertex = [str(v) for v in vertex]

            for item in vertex:
                adjacency.extend(self.adjacency_of(item, with_weight))

            if self.is_pondered and with_weight:
                return tuple(
                    sorted(
                        (v for v in adjacency if v[0] not in vertex),
                        key=lambda x: x[-1],
                    )
                )

            return tuple(sorted(set(v for v in adjacency if v not in vertex)))

    def copy(self, with_edges=True):
        """Returns a copy of the ListGraph object.

        Parameters
        ----------

        with_edges : bool

            Whether the ListGraph object copy shall have its edges inserted or not.

        Returns
        -------

        ListGraph

            A copy of the ListGraph object.
        """
        copy = ListGraph(self.vertices, self.is_directed, self.is_pondered)

        if with_edges:
            for edge in self.edges:
                copy.add_edge(*edge)

        return copy

    def get_minimum_spanning_tree(self, initial_vertex=None, technique="prim"):
        """Provides the vertices and edges to build a ListGraph containing the Minimum Spanning Tree (MST) of the
        ListGraph object.

        This method overrides the implementation seen in the Graph superclass; however, it takes advantage of the
        superclass method to find the vertices and edges. Their implementation of this method is responsible only for
        the creation of the new ListGraph object containing the vertices and edges returned by the superclass method.

        Parameters
        ----------

        initial_vertex : float or int or None or string

            The beginning point of the search. The default is None, case in which the first vertex of self.vertices
            will be used as starting-point.

        technique : str

            The technique to be employed when finding the minimum spanning tree. Prim's algorithm is used in
            Graph.__prim_minimum_spanning_tree(), while Kruskal's algorithm can be found under
            Graph.__kruskal_minimum_spanning_tree(). Can be "prim" or "kruskal".

        Returns
        -------

        ListGraph

            A ListGraph object containing the minimum spanning tree edges and vertices.
        """
        vertices, edges = super().get_minimum_spanning_tree(initial_vertex, technique)

        graph = ListGraph(vertices, self.is_directed, self.is_pondered)

        for edge in edges:
            graph.add_edge(*edge)

        return graph
