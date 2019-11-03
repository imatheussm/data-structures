from graphs.helper import flatten


class Graph:
    """The generic superclass into which the Graph algorithms and general properties shall be implemented."""

    def __init__(self, is_directed, is_pondered):
        """Initializes the Graph superclass.

        This object must not be directly initialized. For that, use MatrixGraph() or ListGraph().

        Parameters
        ----------

        is_directed : bool

            Whether the Graph object being initialized is directed. This can be changed later on through the
            Graph.is_directed setter.

        is_pondered : bool

            Whether the Graph object being initialized is pondered.This can be changed later on through the
            Graph.is_pondered setter.

        Returns
        -------

        Graph

            A Graph object.
        """
        self._directed = is_directed
        self._pondered = is_pondered
        self.__cyclic = False

        self.vertices_list = {}

        self.__current_time = None

    @property
    def is_directed(self):
        """Returns whether the Graph object is directed."""
        return self._directed

    @is_directed.setter
    def is_directed(self, directed):
        """Changes the directed property of the Graph, performing the required operations if needed.

        Parameters
        ----------

        directed : bool

            Whether the Graph will be directed.

        Raises
        ------

        TypeError

            When the object attributed is not of type bool.
        """
        if type(directed) is not bool:
            raise TypeError("This property should receive a boolean value.")

        if self._directed != directed:
            self._directed = directed

            if not directed:
                for edge in self.edges:
                    if not self.is_edge(edge[1], edge[0]):
                        if self.is_pondered:
                            self.add_edge(edge[1], edge[0], edge[2])
                        else:
                            self.add_edge(edge[1], edge[0])

    @property
    def is_pondered(self):
        """Returns whether the Graph object is pondered.

        This method is overridden by the Graph subclasses.

        Returns
        -------

        bool

            Whether the Graph object is pondered.
        """
        return self._pondered

    @property
    def is_cyclic(self):
        """Returns whether the Graph object is cyclic.

        Returns
        -------

        bool

            Whether the Graph object is cyclic."""
        self.__cyclic = False
        self.depth_first_search(self.vertices[0])
        return self.__cyclic

    @property
    def vertices(self):
        """Returns the vertices contained in the Graph object.

        Returns
        -------

        tuple

            The vertices contained in the Graph object.
        """
        return tuple(sorted(list(self.vertices_list.keys())))

    def is_vertex(self, vertex):
        """Returns whether the vertex parameter is a vertex in the Graph object.

        Parameters
        ----------

        vertex : float, int, str

            The vertex to be checked. Given that all vertices labels are treated as strings, this parameter will be
            casted to string prior to the verification.

        Returns
        -------

        bool

            Whether the vertex is part of the Graph object.
        """
        if str(vertex) in self.vertices:
            return True
        else:
            return False

    def describe(self):
        """Describes the main characteristics of the Graph object."""
        print(
            f"<{str(type(self)).split('.')[-1][:-2]} object>\n"
            f"Vertices: {', '.join(self.vertices)}\n"
            f"Edges: {', '.join(('(' + ', '.join((str(item) for item in edge)) + ')' for edge in self.edges))}\n"
            f"Directed: {self.is_directed} | Pondered: {self.is_pondered}"
        )

    @property
    def linked_components(self):
        """Returns the linked (and not necessarily strongly linked) components of the Graph object.

        Returns
        -------

        tuple

            The linked components of the Graph object.

        """
        search_times = self.depth_first_search(self.vertices[0])
        biggest_times = sorted(
            list(search_times.items()), key=lambda x: x[1][1], reverse=True
        )
        search_times_again = {vertex: [-1, -1, None] for vertex in self.vertices}

        for vertex, _ in biggest_times:
            if search_times_again[vertex][0] == -1:
                self.__current_time = 0
                self.__depth_search(vertex, search_times_again)

        self.__current_time = None
        linked_components = {
            vertex: [vertex]
            for vertex in search_times_again.keys()
            if search_times_again[vertex][0] == 0
        }

        for origin in linked_components.keys():
            for destination in self.vertices:
                if (
                    origin != destination
                    and self.get_shortest_path_between(origin, destination)[0]
                    is not None
                ):
                    linked_components[origin].append(destination)

        return tuple(
            tuple(sorted(list(component))) for component in linked_components.values()
        )

    @property
    def number_of_linked_components(self):
        """Returns the number of linked components in the Graph object.

        Returns
        -------

        int

            The number of linked components in the Graph object.
        """
        return len(self.linked_components)

    @property
    def strongly_linked_components(self):
        """Returns the strongly linked components of the Graph object.

        Returns
        -------

        tuple

            The strongly linked components of the Graph object.
        """
        if not self.is_directed:
            transposed_graph = self
        else:
            transposed_graph = self.transpose()

        search_times = self.depth_first_search(self.vertices[0])
        biggest_times = sorted(
            list(search_times.items()), key=lambda x: x[1][1], reverse=True
        )
        strongly_linked_components = []

        for vertex, _ in biggest_times:
            if vertex not in flatten(strongly_linked_components):
                search_times_transposed = {
                    vertex: [-1, -1, None] for vertex in self.vertices
                }
                transposed_graph.__current_time = 0
                transposed_graph.__depth_search(vertex, search_times_transposed)
                component = tuple(
                    vertex
                    for vertex in search_times_transposed.keys()
                    if search_times_transposed[vertex][0] != -1
                    and vertex not in flatten(strongly_linked_components)
                )
                strongly_linked_components.append(component)

        self.__current_time = None

        return tuple(sorted(strongly_linked_components))

    @property
    def number_of_strongly_linked_components(self):
        """Returns the number of strongly linked components in the Graph object.

        Returns
        -------

        int

            The number of strongly linked components in the Graph object.
        """
        return len(self.strongly_linked_components)

    @property
    def edges(self):
        """Returns the edges (and their weights, if appropriate) of the Graph object.

        Returns
        -------

        tuple of (str, float)

            The edges (and their weights, if applicable) of the Graph object.
        """
        edges = []

        if self.is_pondered:
            for origin in self.vertices:
                for destination, weight in self.adjacency_of(origin):
                    if (
                        not self.is_directed
                        and (destination, origin, weight) not in edges
                    ):
                        edges.append((origin, destination, weight))
                    elif self.is_directed:
                        edges.append((origin, destination, weight))
        else:
            for origin in self.vertices:
                for destination in self.adjacency_of(origin):
                    if not self.is_directed and (destination, origin) not in edges:
                        edges.append((origin, destination))
                    elif self.is_directed:
                        edges.append((origin, destination))

        return tuple(edges)

    def __len__(self):
        """Returns the number of vertices of the Graph object.

        Returns
        -------

        int

            The number of vertices contained in the Graph object.
        """
        return self.number_of_vertices

    @property
    def number_of_vertices(self):
        """Returns the number of vertices of the Graph object.

        Returns
        -------

        int

            The number of vertices contained in the Graph object.
        """
        return len(self.vertices)

    def depth_first_search(self, initial_vertex=None):
        """Performs a depth-first search in the Graph object from a given vertex.

        This implementation was inspired by Gabriela's previous implementation, although with some changes. Since the
        author did not look after any pseudo-code prior to this implementation, its performance asymptotically might
        be sub-optimal.

        This method takes advantage of the private method Graph.__depth_search(), which performs the depth-first
        search per se. This function might execute Graph.__depth_search() more than once for different initial
        vertices if it detects that there are vertices that has not been visited yet.

        Parameters
        ----------

        initial_vertex : float or int or None or string

            The beginning point of the depth-first search. The default is None, case in which the first vertex of
            self.vertices will be used as starting-point.

        Raises
        ------

        ValueError

            If the vertex is not contained in the Graph object.

        Returns
        -------

        dict of {str: list of int, str}

            The discovery and completion times and the predecessor vertex for each vertex of the Graph object.
        """
        search_times = {vertex: [-1, -1, None] for vertex in self.vertices}

        if initial_vertex is None:
            initial_vertex = self.vertices[0]
        else:
            initial_vertex = str(initial_vertex)

            if not self.is_vertex(initial_vertex):
                raise ValueError("Non-existent vertex. Add it first and try again.")

        self.__current_time = 0

        self.__depth_search(initial_vertex, search_times)

        for vertex in self.vertices:
            if search_times[vertex][0] == -1:
                self.__current_time += 1

                self.__depth_search(vertex, search_times)

        self.__current_time = None

        for vertex in search_times.keys():
            search_times[vertex] = tuple(search_times[vertex])

        return search_times

    def __depth_search(self, vertex, search_times):
        """Performs a depth-search from the vertex provided.

        This method is not meant to be used directly; use Graph.depth_first_search() instead.

        Parameters
        ----------

        vertex : float or int or str

            The vertex on which the search shall begin. Given that all vertices labels are treated as strings,
            this parameter will be casted to string prior to the verification.

        search_times : dict of {str: list of [int, None]}

            The dictionary in which the search times and the predecessor vertex will be added. This dictionary is
            created and managed by Graph.depth_first_search().
        """
        search_times[vertex][0] = self.__current_time
        vertex = str(vertex)

        for v in self.adjacency_of(vertex, False):
            if search_times[v][0] == -1:
                search_times[v][-1] = vertex
                self.__current_time += 1

                self.__depth_search(v, search_times)
            elif search_times[v][1] == -1 and v != search_times[vertex][2]:
                # print(f"({vertex}, {v}) is cyclic! Origin of {vertex}: {search_times[vertex][2]}; "
                #       f"origin of {v}: {search_times[v][2]}.")
                self.__cyclic = True

        self.__current_time += 1
        search_times[vertex][1] = self.__current_time

    def breadth_first_search(self, initial_vertex=None):
        """Performs a breadth-first search in the Graph object from a given vertex.

        This implementation was inspired by Gabriela's previous implementation, although with some changes. Since the
        author did not look after any pseudo-code prior to this implementation, its performance asymptotically might
        be sub-optimal.

        This method takes advantage of the private method Graph.__breadth_search(), which performs the depth-first
        search per se. This function might execute Graph.__breadth_search() more than once for different initial
        vertices if it detects that there are vertices that has not been visited yet.

        Parameters
        ----------

        initial_vertex : float or int or None or string

            The beginning point of the depth-first search. The default is None, case in which the first vertex of
            self.vertices will be used as starting-point.

        Raises
        ------

        ValueError

            If the vertex is not contained in the Graph object.

        Returns
        -------

        dict of {str: list of int}

            The discovery times and predecessor vertices for each vertex of the Graph object.
        """
        search_times = {vertex: [-1, None] for vertex in self.vertices}

        if initial_vertex is None:
            initial_vertex = self.vertices[0]
        else:
            initial_vertex = str(initial_vertex)

            if not self.is_vertex(initial_vertex):
                raise ValueError("Non-existent vertex. Add it first and try again.")

        self.__current_time, stack = 0, []

        self.__breadth_search(initial_vertex, search_times, stack)

        for vertex in self.vertices:
            if search_times[vertex][0] == -1:
                self.__current_time += 1
                self.__breadth_search(vertex, search_times, stack)

        self.__current_time = None

        for vertex in search_times.keys():
            search_times[vertex] = tuple(search_times[vertex])

        return search_times

    def __breadth_search(self, vertex, search_times, stack):
        """Performs a breadth-search from the vertex provided.

        This method is not meant to be used directly; use Graph.breadth_first_search() instead.

        Parameters
        ----------

        vertex : float or int or str

            The vertex on which the search shall begin. Given that all vertices labels are treated as strings,
            this parameter will be casted to string prior to the verification.

        search_times : dict of {str: list of [int, None]}

            The dictionary in which the search times and the predecessor vertex will be added. This dictionary is
            created and managed by Graph.breadth_first_search().

        stack : list of [str]

            The stack in which the adjacent, non-visited vertices shall be put to be visited later. This stack is
            created and managed by Graph.breadth_first_search().
        """
        if search_times[vertex][0] == -1:
            search_times[vertex][0] = self.__current_time

        for v in self.adjacency_of(vertex, False):
            if v not in stack and search_times[v][0] == -1:
                self.__current_time = search_times[vertex][0] + 1
                search_times[v][0] = self.__current_time
                search_times[v][1] = vertex

                stack.append(v)

        while len(stack) > 0:
            self.__breadth_search(stack.pop(0), search_times, stack)

    def get_shortest_path_between(self, origin, destination):
        """Finds the shortest path (if any) between two vertices of the Graph object.

        Depending on the Graph object properties, this method might take advantage either of the breadth-first search
        or the Dijkstra algorithm.

        Parameters
        ----------

        origin : float or int or str

            The origin vertex. Given that all vertices labels are treated as strings, this parameter will be casted
            to string prior to the verification.

        destination : float or int or str

            The destination vertex. Given that all vertices labels are treated as strings, this parameter will be
            casted to string prior to the verification.

        Raises
        ------

        ValueError

            If either origin or destination vertex is not contained in the Graph object.

        Returns
        -------

        tuple of (str, int) or None

            The a path of vertices linking the origin to the destination and its length.
        """
        origin, destination = str(origin), str(destination)

        if not self.is_vertex(origin) or not self.is_vertex(destination):
            raise ValueError("Non-existent vertex. Add it first and try again.")

        if not self.is_pondered:
            distances = self.breadth_first_search(origin)
        else:
            distances = self.dijkstra_search(origin)

        path = [destination]
        vertex = distances[destination][1]

        while vertex is not None:
            path.insert(0, vertex)
            vertex = distances[vertex][1]

        if path[0] != origin or path[-1] != destination:
            return None, -1

        if not self.is_pondered:
            length = len(path)
        else:
            length = distances[destination][0]

        return path, length

    def topological_sort(self, initial_vertex=None):
        """Performs the topological sorting in the vertices of the Graph object.

        This method takes advantage of Graph.depth_first_search() to sort the vertices of the Graph object.

        Parameters
        ----------

        initial_vertex : float or int or None or string

            The beginning point of the depth-first search. The default is None, case in which the first vertex of
            self.vertices will be used as starting-point.

        Raises
        ------

        ValueError

            If the vertex is not contained in the Graph object.

        Returns
        -------

        list of str

            A list of the vertices contained in the Graph object, topologically ordered.
        """
        if initial_vertex is None:
            initial_vertex = self.vertices[0]
        else:
            initial_vertex = str(initial_vertex)

            if not self.is_vertex(initial_vertex):
                raise ValueError("Non-existent vertex. Add it first and try again.")

        search_times = list(self.depth_first_search(initial_vertex).items())
        search_times.sort(key=lambda x: x[1][1], reverse=True)

        vertices = [vertex[0] for vertex in search_times]

        return vertices

    def get_minimum_spanning_tree(self, initial_vertex=None, technique="prim"):
        """Provides the vertices and edges to build a Graph containing the Minimum Spanning Tree (MST) of the Graph
        object.

        This method is overridden by the ListGraph and MatrixGraph subclasses; however, they both take advantage of
        this code to find the vertices and edges. Their implementation of this method is responsible only for the
        creation of the new ListGraph/MatrixGraph object containing the vertices and edges returned by this method.

        This scenario has not been tested; however, the idea is that this algorithm could be used in non-connected
        graphs. This is why, similar to the breadth- and depth-first search implementations, there are two methods (a
        public and a private) for the same task: this method might perform the algorithm more than once if the first
        attempt result in a graph with less vertices than the original.

        Parameters
        ----------

        initial_vertex : float or int or None or string

            The beginning point of the search. The default is None, case in which the first vertex of self.vertices
            will be used as starting-point.

        technique : str

            The technique to be employed when finding the minimum spanning tree. Prim's algorithm is used in
            Graph.__prim_minimum_spanning_tree(), while Kruskal's algorithm can be found under
            Graph.__kruskal_minimum_spanning_tree(). Can be "prim" or "kruskal".

        Raises
        ------

        TypeError

            When the Graph object is not pondered or when it is directed.

        ValueError

            When the technique provided is neither "prim" nor "kruskal", or when the initial vertex is not contained
            in the Graph object.

        ArithmeticError

            When the cycle rank of the Graph object is 0, which means that it is already a minimum spanning tree.

        Returns
        -------

        tuple of (tuple of str, tuple of (str, str, float))

            The edges and vertices of the minimum spanning tree.
        """
        if not self.is_pondered:
            raise TypeError("This algorithm can be applied only to pondered graphs.")
        if self.is_directed:
            raise TypeError("This algorithm can be applied only to undirected graphs.")
        if self.cycle_rank == 0:
            raise ArithmeticError(
                "This Graph object is already a minimum spanning tree."
            )

        technique = technique.lower()

        if technique == "prim":
            technique = self.__prim_minimum_spanning_tree
        elif technique == "kruskal":
            technique = self.__kruskal_minimum_spanning_tree
        else:
            raise ValueError(
                f"{technique} is an unknown technique. Supported techniques: 'prim', 'kruskal'."
            )

        if initial_vertex is None:
            initial_vertex = self.vertices[0]
        else:
            initial_vertex = str(initial_vertex)

            if not self.is_vertex(initial_vertex):
                raise ValueError("Non-existent vertex. Add it first and try again.")

        vertices, edges = technique(initial_vertex)

        while len(vertices) < self.number_of_vertices:
            for vertex in self.vertices:
                if vertex not in vertices:
                    other_vertices, other_edges = technique(vertex)

                    vertices.extend(other_vertices)
                    edges.extend(other_edges)

        return sorted(vertices), sorted(edges)

    def __prim_minimum_spanning_tree(self, initial_vertex=None):
        """Prim's minimum spanning tree algorithm.

        This implementation was inspired by Gabriela's previous implementation of the depth- and breadth-first
        searches. Since the author did not look after any pseudo-code prior to this implementation, its performance
        asymptotically might be sub-optimal. I have to check with Gabriela if it is acceptable.

        This method is not meant to be used directly; use Graph.get_minimum_spanning_tree(technique="prim") instead.

        Parameters
        ----------

        initial_vertex : float or int or None or string

            The beginning point of the search. The default is None, case in which the first vertex of self.vertices
            will be used as starting-point.

        Raises
        ------

        ValueError

            If the vertex is not contained in the Graph object.

        Returns
        -------

        tuple of (tuple of str, tuple of (str, str, float))

            The edges and vertices of the minimum spanning tree.
        """
        if initial_vertex is None:
            initial_vertex = self.vertices[0]
        else:
            initial_vertex = str(initial_vertex)

            if not self.is_vertex(initial_vertex):
                raise ValueError("Non-existent vertex. Add it first and try again.")

        vertices, edges = [initial_vertex], []

        graph = self.copy()
        graph.is_directed = True

        while True:
            adjacency = sorted(
                (
                    edge
                    for edge in graph.edges
                    if edge[0] in vertices
                    and edge[1] in graph.adjacency_of(vertices, False)
                ),
                key=lambda x: x[-1],
            )

            if not adjacency:
                break

            edges.append(adjacency[0])

            if adjacency[0][0] not in vertices:
                vertices.append(adjacency[0][0])
            if adjacency[0][1] not in vertices:
                vertices.append(adjacency[0][1])

        return vertices, edges

    def __kruskal_minimum_spanning_tree(self, initial_vertex=None):
        """Prim's minimum spanning tree algorithm.

        This implementation was inspired by Gabriela's previous implementation of the depth- and breadth-first
        searches. Since the author did not look after any pseudo-code prior to this implementation, its performance
        asymptotically might be sub-optimal. I have to check with Gabriela if it is acceptable.

        This method is not meant to be used directly; use Graph.get_minimum_spanning_tree(technique="kruskal") instead.

        Parameters
        ----------

        initial_vertex : float or int or None or string

            The beginning point of the search. The default is None, case in which the first vertex of self.vertices
            will be used as starting-point.

        Raises
        ------

        ValueError

            If the vertex is not contained in the Graph object.

        Returns
        -------

        tuple of (tuple of str, tuple of (str, str, float))

            The edges and vertices of the minimum spanning tree.
        """
        if initial_vertex is None:
            initial_vertex = self.vertices[0]
        else:
            initial_vertex = str(initial_vertex)

            if not self.is_vertex(initial_vertex):
                raise ValueError("Non-existent vertex. Add it first and try again.")

        vertices, edges, discarded_edges = [initial_vertex], [], []
        graph = self.copy(False)

        while graph.number_of_linked_components > self.number_of_linked_components:
            adjacency = sorted(
                (
                    edge
                    for edge in self.edges
                    if edge not in graph.edges and edge not in discarded_edges
                ),
                key=lambda x: x[-1],
            )

            if not adjacency:
                break

            graph.add_edge(*adjacency[0])

            if graph.is_cyclic:
                graph.remove_edge(*adjacency[0][:2])
                discarded_edges.append(adjacency[0])
            else:
                edges.append(adjacency[0])

                if adjacency[0][0] not in vertices:
                    vertices.append(adjacency[0][0])
                if adjacency[0][1] not in vertices:
                    vertices.append(adjacency[0][1])

        return vertices, edges

    def dijkstra_search(self, initial_vertex=None):
        """Perform Dijkstra's shortest path algorithm on the Graph object.

        This implementation was inspired by Gabriela's previous implementation of the depth- and breadth-first
        searches. Since the author did not look after any pseudo-code prior to this implementation, its performance
        asymptotically might be sub-optimal. I have to check with Gabriela if it is acceptable.

        This algorithm is used in pondered graphs by Graph.get_shortest_path_between() to find the shortest path
        between two vertices.

        In cases where the graph in question contains more than one linked component, ideally (this case has not been
        tested) this public method could perform more than one Dijkstra search (Graph.__dijkstra_search()) in each
        component, until all vertices are visited. However, the usefulness of this particularity in the problems
        solved by this algorithm is left to be seen. This is why the test of this case has been left aside for now.

        Parameters
        ----------

        initial_vertex : float or int or None or string

            The beginning point of the search. The default is None, case in which the first vertex of self.vertices
            will be used as starting-point.

        Raises
        ------

        TypeError

            If the Graph object is not pondered, case in which the breadth-first search is employed.

        ValueError

            If the vertex is not contained in the Graph object.

        Returns
        -------

        dict of {str: list of [int, str]}

            The results of the search, containing the distance between the initial vertex and the vertices of the
            Graph objects, as well as the predecessor vertex of each vertex.
        """
        if not self.is_pondered:
            raise TypeError(
                "The Dijkstra Algorithm was meant to be used in pondered graphs."
            )

        if initial_vertex is None:
            initial_vertex = self.vertices[0]
        else:
            initial_vertex = str(initial_vertex)

            if not self.is_vertex(initial_vertex):
                raise ValueError("Non-existent vertex. Add it first and try again.")

        results = {vertex: [-1, None, False] for vertex in self.vertices}

        self.__dijkstra_search(initial_vertex, results)

        for vertex in self.vertices:
            if not results[vertex][-1]:
                print(f"Beginning another Dijkstra Search in {vertex}...")
                self.__dijkstra_search(vertex, results)

        return {vertex: results[vertex][:2] for vertex in results.keys()}

    def __dijkstra_search(self, vertex, results):
        """Performs a Dijkstra search from the vertex provided.

        This method is not meant to be used directly; use Graph.dijkstra_search() instead.

        Parameters
        ----------

        vertex : float or int or str

            The vertex on which the search shall begin. Given that all vertices labels are treated as strings,
            this parameter will be casted to string prior to the verification.

        results : dict of {str: list of [int, None]}

            The dictionary in which the search times and the predecessor vertex will be added. This dictionary is
            created and managed by Graph.dijkstra_search().
        """
        if results[vertex][0] == -1:
            results[vertex][0] = 0
        results[vertex][-1] = True

        adjacency = self.adjacency_of(vertex)

        for v, weight in adjacency:
            if (results[v][1] is None and results[v][0] == -1) or (
                results[v][0] > results[vertex][0] + weight
            ):
                results[v][0] = results[vertex][0] + weight
                results[v][1] = vertex

        possible_adjacency = sorted(
            [
                item
                for item in results.items()
                if item[-1][-1] is False and item[-1][0] != -1
            ],
            key=lambda x: x[-1][0],
        )

        for v, value in possible_adjacency:
            if value[-1] is False:
                self.__dijkstra_search(v, results)

    @property
    def cycle_rank(self):
        """Returns the cycle rank (elo/posto, in Portuguese literature) of the Graph object.

        This is used to know how many edges have to be cut in order to obtain a minimum spanning tree of the Graph
        object in question. It is used by Graph.get_minimum_spanning_tree() to check if the Graph object already is a
        minimum spanning tree prior to performing any operation.

        Raises
        ------

        TypeError

            When the Graph object is directed.

        Returns
        -------

        int

            The cycle rank of the Graph object.
        """
        if self.is_directed:
            raise TypeError(
                "The cycle rank metric has been implemented only for undirected graphs."
            )

        return (
            self.number_of_edges
            - self.number_of_vertices
            + self.number_of_linked_components
        )

    @property
    def number_of_edges(self):
        """Returns the number of edges of the Graph object.

        This method is currently overridden by specific implementations in the Graph subclasses. This could change in
        the future, however, for simplicity's sake.

        Returns
        -------

        int

            The number of edges contained in the Graph object.
        """
        return len(self.edges)

    def copy(self, with_edges=True):
        """Returns a copy of the Graph object.

        This is just a placeholder to suppress any IDE warnings about methods that are only implemented in Graph
        subclasses.

        Parameters
        ----------

        with_edges : bool

            Whether the Graph object copy shall have its edges inserted or not.

        Raises
        ------

        NotImplementedError

            This code should be unreachable. If that is not the case, something is wrongfully implemented.

        Returns
        -------

        Graph

            A copy of the Graph object.
        """
        raise NotImplementedError("You shouldn't have reached this part of the code.")

    def is_edge(self, origin, destination):
        """Returns whether a given edge is contained in the Graph object.

        This is just a placeholder to suppress any IDE warnings about methods that are only implemented in Graph
        subclasses.

        Parameters
        ----------

        origin : float or int or str

            The origin vertex. Given that all vertices labels are treated as strings, this parameter will be casted
            to string prior to the verification.

        destination : float or int or str

            The destination vertex. Given that all vertices labels are treated as strings, this parameter will be
            casted to string prior to the verification.

        Raises
        ------

        NotImplementedError

            This code should be unreachable. If that is not the case, something is wrongfully implemented.

        Returns
        -------

        bool

            Whether there is an edge that links the provided vertices in the Graph object.
        """
        raise NotImplementedError("You shouldn't have reached this part of the code.")

    def add_edge(self, origin, destination, weight=1):
        """Adds an edge to the Graph object.

        This is just a placeholder to suppress any IDE warnings about methods that are only implemented in Graph
        subclasses.

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

        NotImplementedError

            This code should be unreachable. If that is not the case, something is wrongfully implemented.
        """
        raise NotImplementedError("You shouldn't have reached this part of the code.")

    def remove_edge(self, origin, destination):
        """Removes an edge of the Graph object.

        This is just a placeholder to suppress any IDE warnings about methods that are only implemented in Graph
        subclasses.

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

        NotImplementedError

            This code should be unreachable. If that is not the case, something is wrongfully implemented.
        """
        raise NotImplementedError("You shouldn't have reached this part of the code.")

    def transpose(self):
        """Returns a transposed copy of the Graph object.

        This is just a placeholder to suppress any IDE warnings about methods that are only implemented in Graph
        subclasses.

        Raises
        ------

        NotImplementedError

            This code should be unreachable. If that is not the case, something is wrongfully implemented.

        Returns
        -------

        Graph

            A Graph object with its edges transposed.
        """
        raise NotImplementedError("You shouldn't have reached this part of the code.")

    def adjacency_of(self, vertex, with_weight=True):
        """Returns the adjacency of a given vertex.

        This is just a placeholder to suppress any IDE warnings about methods that are only implemented in Graph
        subclasses.

        Parameters
        ----------

        vertex : float or int or str

            The vertex on which the search shall begin. Given that all vertices labels are treated as strings,
            this parameter will be casted to string prior to the verification.

        with_weight : bool

            Whether to return, if applicable, the edge weights of the Graph object that link the vertex to its
            adjacency.

        Raises
        ------

        NotImplementedError

            This code should be unreachable. If that is not the case, something is wrongfully implemented.

        Returns
        -------

        tuple(tuple of (str, int) or str)

            The adjacency of the vertex with the weights (if applicable) contained in the Graph object.
        """
        raise NotImplementedError("You shouldn't have reached this part of the code.")

    @property
    def is_list(self):
        """Returns whether the Graph object is a ListGraph.

        This is just a placeholder to suppress any IDE warnings about methods that are only implemented in Graph
        subclasses.

        Raises
        ------

        NotImplementedError

            This code should be unreachable. If that is not the case, something is wrongfully implemented.

        Returns
        -------

        bool

            Whether the Graph object is a ListGraph.
        """
        raise NotImplementedError("You shouldn't have reached this part of the code.")

    @property
    def is_matrix(self):
        """Returns whether the Graph object is a MatrixGraph.

        This is just a placeholder to suppress any IDE warnings about methods that are only implemented in Graph
        subclasses.

        Raises
        ------

        NotImplementedError

            This code should be unreachable. If that is not the case, something is wrongfully implemented.

        Returns
        -------

        bool

            Whether the Graph object is a MatrixGraph.
        """
        raise NotImplementedError("You shouldn't have reached this part of the code.")
