import scipy as sp

from graphs import Graph


class MatrixGraph(Graph):
    def __init__(self, vertices, is_directed, is_pondered):
        super().__init__(vertices, is_directed, is_pondered)

        self.vertices_list = {str(vertex): index for index, vertex in enumerate(vertices)}
        self.__graph = sp.zeros((len(self), len(self)))

    @property
    def label_to_index_mapping(self):
        return sorted(list(self.vertices_list.items()), key=lambda x: x[1])

    def __repr__(self):
        max_length = sp.fromiter((len(str(vertex)) for vertex in self.vertices), int, len(self)).max()

        representation = "<MatrixGraph object>\n"
        representation += (max_length + 2) * " " + " ".join(
            [str(x).ljust(max_length, " ") for x in self.vertices_list.keys()]) + "\n\n"

        for label, index in self.label_to_index_mapping:
            representation += str(label).ljust(max_length + 2, " ") + " ".join(
                [str(int(n)).ljust(max_length, " ") for n in self.__graph[int(index)]]) + "\n"

        return representation[:-1]

    def is_edge(self, origin, destination):
        try:
            origin, destination = self.vertices_list[str(origin)], self.vertices_list[str(destination)]
            if self.__graph[origin, destination]:
                return True
            else:
                return False
        except KeyError:
            False

    def add_edge(self, origin, destination, weight=1):
        if self.is_edge(origin, destination):
            raise ValueError("This edge already exists.")

        try:
            origin, destination = self.vertices_list[str(origin)], self.vertices_list[str(destination)]

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
        except KeyError:
            raise KeyError("Non-existent vertex. Add it first and try again.")

    def remove_edge(self, origin, destination):
        if not self.is_edge(origin, destination):
            raise ValueError("This edge does not exist.")

        try:
            origin, destination = self.vertices_list[str(origin)], self.vertices_list[str(destination)]

            self.__graph[origin, destination] = 0

            if not self.is_directed:
                self.__graph[destination, origin] = 0
        except KeyError:
            raise KeyError("Non-existent vertex. Add it first and try again.")

    @property
    def number_of_edges(self):
        edge_counter = int(self.__graph[self.__graph != 0].sum())

        if not self.is_directed:
            return int(edge_counter / 2)
        return edge_counter

    def degree_of(self, vertex):
        vertex = self.vertices_list[str(vertex)]

        out_degree = int(self.__graph[vertex, :][self.__graph[vertex, :] != 0].sum())

        if self.is_directed:
            in_degree = int(self.__graph[:, vertex][self.__graph[:, vertex] != 0].sum())

            return in_degree, out_degree

        return out_degree

    def adjacency_of(self, vertex):
        vertex = self.vertices_list[str(vertex)]
        occurrences = self.__graph[vertex, :]

        return [self.vertices[i] for i in range(self.number_of_vertices) if occurrences[i] != 0]