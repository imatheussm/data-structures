import scipy as sp

from graphs import Graph


class MatrixGraph(Graph):
    """The Graph abstract data structure, implemented via adjacency matrix. Extends the Graph superclass."""

    def __init__(self, vertices, is_directed, is_pondered):
        """Initializes the MatrixGraph class.

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

        MatrixGraph

            A MatrixGraph object.
        """
        vertices = sorted(vertices)

        super().__init__(is_directed, is_pondered)

        self.vertices_list = {
            str(vertex): index for index, vertex in enumerate(vertices)
        }

        if self.is_pondered:
            self.__graph = sp.zeros((len(self), len(self)))
        else:
            self.__graph = sp.zeros((len(self), len(self)), dtype=int)

    def __getitem__(self, index):
        """Returns the adjacency of a given vertex using the [] syntax.

        This is a safe implementation, given that MatrixGraph.__setitem__() is not defined. As such, any attempts of
        assignment of new values would result in a TypeError.

        Parameters
        ----------

        index : float or int or str

            The vertex whose adjacency is to be obtained.

        Returns
        -------

        sp.ndarray

            The adjacency of a given vertex in a MatrixGraph object.
        """
        if type(index) is tuple:
            for vertex in index:
                if type(vertex) is not slice and not self.is_vertex(vertex):
                    raise ValueError("Non-existent vertex. Add it first and try again.")

            index = tuple(
                (
                    self.vertices_list[str(item)] if type(item) is not slice else item
                    for item in index
                )
            )
        else:
            if not self.is_vertex(index):
                raise ValueError("Non-existent vertex. Add it first and try again.")

            index = self.vertices_list[str(index)]

        return self.__graph.__getitem__(index)

    @property
    def is_matrix(self):
        """Returns whether the Graph object is a MatrixGraph.

        Returns
        -------

        bool

            Whether the Graph object is a MatrixGraph.
        """
        return True

    @property
    def is_list(self):
        """Returns whether the Graph object is a ListGraph.

        Returns
        -------

        bool

            Whether the Graph object is a ListGraph.
        """
        return False

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

            if pondered:
                self.__graph = self.__graph.astype(float)
            else:
                self.__graph = self.__graph.astype(int)
                for origin in range(self.__graph.shape[0]):
                    for destination in range(self.__graph.shape[1]):
                        if self.__graph[origin, destination] != 0:
                            self.__graph[origin, destination] = 1

    @property
    def label_to_index_mapping(self):
        """Returns the mapping between the vertices labels and their corresponding indices in the MatrixGraph object.

        Returns
        -------

        list of [str, int]

            A list containing the labels and their corresponding indices in the MatrixGraph object.

        """
        return sorted(list(self.vertices_list.items()), key=lambda x: x[1])

    def __repr__(self):
        """Returns a representation of the MatrixGraph object.

        Returns
        -------

        str

            The string representation of the object to be printed by the Python interpreter.
        """
        max_vertex_length = sp.fromiter(
            (len(str(vertex)) for vertex in self.vertices), int, len(self)
        ).max()
        max_value_length = len(str(self.__graph.max()))
        max_length = max([max_vertex_length, max_value_length])

        representation = "<MatrixGraph object>\n"
        representation += (
            (max_length + 2) * " "
            + " ".join(
                [str(x).ljust(max_length + 1, " ") for x in self.vertices_list.keys()]
            )
            + "\n\n"
        )

        for label, index in self.label_to_index_mapping:
            representation += (
                str(label).ljust(max_length + 2, " ")
                + " ".join(
                    [
                        str(n).ljust(max_length + 1, " ")
                        for n in self.__graph[int(index)]
                    ]
                )
                + "\n"
            )

        return representation[:-1]

    def is_edge(self, origin, destination):
        """Returns whether a given edge is contained in the MatrixGraph object.

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

            Whether there is an edge that links the provided vertices in the MatrixGraph object.
        """
        try:
            origin, destination = (
                self.vertices_list[str(origin)],
                self.vertices_list[str(destination)],
            )
            if self.__graph[origin, destination]:
                return True
            else:
                return False
        except KeyError:
            return False

    def add_edge(self, origin, destination, weight=1):
        """Adds an edge to the MatrixGraph object.

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
            multigraphs are not supported currently), or either of the vertices is not contained in the MatrixGraph
            object, or when the weight is 0.
        """
        origin, destination = str(origin), str(destination)

        if not self.is_directed and origin == destination:
            raise ValueError("Non-directed graphs cannot have loops.")
        if self.is_edge(origin, destination):
            raise ValueError("This edge already exists.")
        if not self.is_vertex(origin) or not self.is_vertex(destination):
            raise ValueError("Non-existent vertex. Add it first and try again.")

        origin, destination = (
            self.vertices_list[origin],
            self.vertices_list[destination],
        )

        if self.is_pondered:
            if weight == 0:
                raise ValueError("The weight must be a non-null number.")

            self.__graph[origin, destination] = weight

            if not self.is_directed:
                self.__graph[destination, origin] = weight
        else:
            self.__graph[origin, destination] = 1

            if not self.is_directed:
                self.__graph[destination, origin] = 1

    def remove_edge(self, origin, destination):
        """Removes an edge of the MatrixGraph object.

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

        try:
            origin, destination = (
                self.vertices_list[str(origin)],
                self.vertices_list[str(destination)],
            )

            self.__graph[origin, destination] = 0

            if not self.is_directed:
                self.__graph[destination, origin] = 0
        except KeyError:
            raise ValueError("Non-existent vertex. Add it first and try again.")

    @property
    def number_of_edges(self):
        """Returns the number of edges of the MatrixGraph object.

        Returns
        -------

        int

            The number of edges contained in the MatrixGraph object.
        """
        edge_counter = int(self.__graph[self.__graph != 0].sum())

        if not self.is_directed:
            return int(edge_counter / 2)
        return edge_counter

    def transpose(self):
        """Returns a transposed copy of the MatrixGraph object.

        Raises
        ------

        TypeError

            When the MatrixGraph object is non-directed, its transposed version is equal to itself. This implementation
            opted to raise an error instead of just returning itself, although this could change in the future.

        Returns
        -------

        MatrixGraph

            A MatrixGraph object with its edges transposed.
        """
        if not self.is_directed:
            raise TypeError("Non-directed graphs can't be transposed.")

        transposed_edges = tuple(((edge[1], edge[0], edge[2:]) for edge in self.edges))

        transposed_graph = MatrixGraph(
            self.vertices, self.is_directed, self.is_pondered
        )

        for edge in transposed_edges:
            transposed_graph.add_edge(*edge)

        return transposed_graph

    def degree_of(self, vertex):
        """Returns the degree of a given vertex the MatrixGraph object.

        Parameters
        ----------

        vertex : float or int or str

            The vertex. Given that all vertices labels are treated as strings, this parameter will be casted to
            string prior to the verification.

        Raises
        ------

        ValueError

            When the vertex is not contained in the MatrixGraph object.

        Returns
        -------

        int or tuple of int

            The degree or (in-degree, out-degree) of the vertex in the MatrixGraph object.
        """
        vertex = self.vertices_list[str(vertex)]

        if not self.is_vertex(vertex):
            raise ValueError("Non-existent vertex. Add it first and try again.")

        out_degree = int(self.__graph[vertex, :][self.__graph[vertex, :] != 0].sum())

        if self.is_directed:
            in_degree = int(self.__graph[:, vertex][self.__graph[:, vertex] != 0].sum())

            return in_degree, out_degree

        return out_degree

    def adjacency_of(self, vertex, with_weight=True):
        """Returns the adjacency of a given vertex in a MatrixGraph object.

        Parameters
        ----------

        vertex : float or int or str

            The vertex on which the search shall begin. Given that all vertices labels are treated as strings,
            this parameter will be casted to string prior to the verification.

        with_weight : bool

            Whether to return, if applicable, the edge weights of the MatrixGraph object that link the vertex to its
            adjacency.

        Raises
        ------

        ValueError

            When the vertex is not contained in the MatrixGraph object.

        Returns
        -------

        tuple(tuple of (str, int) or str)

            The adjacency of the vertex with the weights (if applicable) contained in the MatrixGraph object.
        """
        if (
            type(vertex) is not list
            and type(vertex) is not tuple
            and type(vertex) is not set
        ):
            if not self.is_vertex(vertex):
                raise ValueError("Non-existent vertex. Add it first and try again.")

            occurrences = self[vertex, :]

            if self.is_pondered and with_weight:
                return tuple(
                    (self.vertices[i], occurrences[i])
                    for i in range(self.number_of_vertices)
                    if occurrences[i] != 0
                )

            return tuple(
                self.vertices[i]
                for i in range(self.number_of_vertices)
                if occurrences[i] != 0
            )
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
        """Returns a copy of the MatrixGraph object.

        Parameters
        ----------

        with_edges : bool

            Whether the MatrixGraph object copy shall have its edges inserted or not.

        Returns
        -------

        MatrixGraph

            A copy of the MatrixGraph object.
        """
        copy = MatrixGraph(self.vertices, self.is_directed, self.is_pondered)

        if with_edges:
            for edge in self.edges:
                copy.add_edge(*edge)

        return copy

    def get_minimum_spanning_tree(self, initial_vertex=None, technique="prim"):
        """Provides the vertices and edges to build a MatrixGraph containing the Minimum Spanning Tree (MST) of the
        ListGraph object.

        This method overrides the implementation seen in the Graph superclass; however, it takes advantage of the
        superclass method to find the vertices and edges. Their implementation of this method is responsible only for
        the creation of the new MatrixGraph object containing the vertices and edges returned by the superclass method.

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

        MatrixGraph

            A MatrixGraph object containing the minimum spanning tree edges and vertices.
        """
        vertices, edges = super().get_minimum_spanning_tree(initial_vertex, technique)

        graph = MatrixGraph(vertices, self.is_directed, self.is_pondered)

        for edge in edges:
            graph.add_edge(*edge)

        return graph
