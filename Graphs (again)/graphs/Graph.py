def depth_search(vertex, search_times):
    pass


class Graph:
    def __init__(self, vertices, is_directed, is_pondered):
        self.__directed = is_directed
        self.__pondered = is_pondered
        self.__cyclic = False

        self.vertices_list = {}

        self.__current_time = None

    @property
    def is_directed(self):
        return self.__directed

    @property
    def is_pondered(self):
        return self.__pondered

    @property
    def is_cyclic(self):
        self.depth_first_search(self.vertices[0])
        return self.__cyclic

    @property
    def vertices(self):
        return sorted(list(self.vertices_list.keys()))

    def is_vertex(self, vertex):
        if str(vertex) in self.vertices:
            return True
        else:
            return False

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

        self.__current_time = 1

        self.__depth_search(initial_vertex, search_times)

        for vertex in self.vertices:
            if search_times[vertex][0] == -1:
                self.__current_time += 1
                self.__depth_search(vertex, search_times)

        return search_times

    def __depth_search(self, vertex, search_times):
        search_times[vertex][0] = self.__current_time
        vertex = str(vertex)

        for v in self.adjacency_of(vertex):
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

        self.__current_time, stack = 0, []

        self.__breadth_search(initial_vertex, search_times, stack)

        for vertex in self.vertices:
            if search_times[vertex] == -1:
                self.__breadth_search(vertex, search_times, stack)

        return search_times

    def __breadth_search(self, vertex, search_times, stack):
        if search_times[vertex][0] == -1:
            search_times[vertex][0] = self.__current_time
        self.__current_time += 1

        for v in self.adjacency_of(vertex):
            if search_times[v][0] == -1:
                search_times[v][0] = self.__current_time
                search_times[v][1] = vertex
                stack.append(v)

        while len(stack) > 0:
            self.__breadth_search(stack.pop(0), search_times, stack)

    def shortest_path_between(self, origin, destination):
        search_times = self.breadth_first_search(origin)
        origin, destination = str(origin), str(destination)
        path = [destination]
        vertex = search_times[destination][1]
        while vertex is not None:
            path.insert(0, vertex)
            vertex = search_times[vertex][1]

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

