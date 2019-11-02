import scipy as sp

from graphs import Graph


class ListGraph(Graph):
    def __init__(self, vertices, is_directed, is_pondered):
        super().__init__(is_directed, is_pondered)

        self.vertices_list = {str(vertex): {} for vertex in vertices}

    def __getitem__(self, item):
        return self.vertices_list.__getitem__(str(item))

    def __repr__(self):
        max_length = sp.fromiter((len(str(vertex)) for vertex in self.vertices), int, len(self)).max()

        representation = "<ListGraph object>\n"

        for vertex in self.vertices:
            if self.is_pondered:
                adjacency = [f"{destination}: {weight}" for destination, weight in self[vertex].items()]
            else:
                adjacency = [f"{destination}" for destination in self[vertex].keys()]
            representation += str(vertex).ljust(max_length, " ") + " -> " + ", ".join(adjacency) + "\n"

        return representation

    @property
    def is_matrix(self):
        return False

    @property
    def is_list(self):
        return True

    @property
    def is_pondered(self):
        return self._pondered

    @is_pondered.setter
    def is_pondered(self, pondered):
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
        origin, destination = str(origin), str(destination)

        try:
            if self.vertices_list[origin][destination]:
                return True
            else:
                return False
        except KeyError:
            return False

    def transpose(self):
        if not self.is_directed:
            raise TypeError("Non-directed graphs can't be transposed.")

        transposed_edges = tuple(((edge[1], edge[0], edge[2:]) for edge in self.edges))

        transposed_graph = ListGraph(self.vertices, self.is_directed, self.is_pondered)

        for edge in transposed_edges:
            transposed_graph.add_edge(*edge)

        return transposed_graph

    def add_edge(self, origin, destination, weight=1):
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
        if not self.is_edge(origin, destination):
            raise ValueError("This edge does not exist.")

        origin, destination = str(origin), str(destination)

        if origin not in self.vertices or destination not in self.vertices:
            raise KeyError("Non-existent vertex. Add it first and try again.")

        del(self.vertices_list[origin][destination])

        if not self.is_directed:
            del(self.vertices_list[destination][origin])

    @property
    def number_of_edges(self):
        edge_counter = 0

        for vertex in self.vertices:
            edge_counter += len(self.vertices_list[vertex].keys())

        if not self.is_directed:
            return int(edge_counter / 2)
        return int(edge_counter)

    def degree_of(self, vertex):
        vertex = str(vertex)

        out_degree = len(self.vertices_list[vertex].keys())

        if self.is_directed:
            in_degree = 0

            for v in self.vertices:
                if vertex in self.vertices_list[v].keys():
                    in_degree += 1

            return in_degree, out_degree

        return out_degree

    def adjacency_of(self, vertex, with_weight=True):
        if self.is_pondered and with_weight:
            return tuple(sorted(list(self[vertex].items())))

        return tuple(sorted(list(self[vertex].keys())))