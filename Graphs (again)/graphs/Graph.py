class Graph:
    def __init__(self, is_directed, is_pondered):
        self._directed = is_directed
        self._pondered = is_pondered
        self.__cyclic = False

        self.vertices_list = {}

        self.__current_time = None

    @property
    def is_directed(self):
        return self._directed

    @is_directed.setter
    def is_directed(self, directed):
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
        return self._pondered

    @property
    def is_cyclic(self):
        self.depth_first_search(self.vertices[0])
        return self.__cyclic

    @property
    def vertices(self):
        return tuple(sorted(list(self.vertices_list.keys())))

    def is_vertex(self, vertex):
        if str(vertex) in self.vertices:
            return True
        else:
            return False

    # @property
    # def linked_components(self):
    #     search_times = self.breadth_first_search(self.vertices[0])
    #     linked_components = {vertex: [vertex] for vertex in search_times.keys() if search_times[vertex][1] is None}
    #
    #     for origin in linked_components.keys():
    #         for destination in self.vertices:
    #             if origin != destination and self.shortest_path_between(origin, destination) is not None:
    #                 linked_components[origin].append(destination)
    #
    #     return tuple(tuple(component) for component in linked_components.values())

    @property
    def edges(self):
        edges = []

        if self.is_pondered:
            for origin in self.vertices:
                for destination, weight in self.adjacency_of(origin):
                    if not self.is_directed and (destination, origin, weight) not in edges:
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
        return len(self.vertices)

    @property
    def number_of_vertices(self):
        return len(self.vertices)

    def depth_first_search(self, initial_vertex=None):
        search_times = {vertex: [-1, -1] for vertex in self.vertices}

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
        search_times[vertex][0] = self.__current_time
        vertex = str(vertex)

        for v in self.adjacency_of(vertex, False):
            if search_times[v][0] == -1:
                self.__current_time += 1
                self.__depth_search(v, search_times)
            elif search_times[v][1] == -1:
                self.__cyclic = True

        self.__current_time += 1
        search_times[vertex][1] = self.__current_time

    def breadth_first_search(self, initial_vertex=None):
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

    def shortest_path_between(self, origin, destination):
        origin, destination = str(origin), str(destination)

        if not self.is_vertex(origin) or not self.is_vertex(destination):
            raise ValueError("Non-existent vertex. Add it first and try again.")

        search_times = self.breadth_first_search(origin)
        path = [destination]

        vertex = search_times[destination][1]
        while vertex is not None:
            path.insert(0, vertex)
            vertex = search_times[vertex][1]

        if path[0] != origin or path[-1] != destination:
            return None

        return path

    def topological_sorting(self, initial_vertex=None):
        if initial_vertex is None:
            initial_vertex = self.vertices[0]
        else:
            initial_vertex = str(initial_vertex)

        search_times = list(self.depth_first_search(initial_vertex).items())
        search_times.sort(key=lambda x: x[1][1], reverse=True)
        search_times = [vertex[0] for vertex in search_times]

        return search_times

