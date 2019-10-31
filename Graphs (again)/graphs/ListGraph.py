import scipy as sp

from graphs import Graph


class ListGraph(Graph):
    def __init__(self, vertices, is_directed, is_pondered):
        super().__init__(vertices, is_directed, is_pondered)

        self.vertices_list = {str(vertex): {} for vertex in vertices}

    def __getitem__(self, item):
        return self.vertices_list.__getitem__(str(item))

    def __repr__(self):
        max_length = sp.fromiter((len(str(vertex)) for vertex in self.vertices), int, len(self)).max()

        representation = "<ListGraph object>\n"

        for vertex in self.vertices:
            representation += str(vertex).ljust(max_length, " ") + " -> " + ", ".join(self[vertex].keys()) + "\n"

        return representation

    def is_edge(self, origin, destination):
        origin, destination = str(origin), str(destination)

        try:
            if self.vertices_list[origin][destination]:
                return True
            else:
                return False
        except KeyError:
            return False

    def add_edge(self, origin, destination, weight=1):
        if self.is_edge(origin, destination):
            raise ValueError("This edge already exists.")

        origin, destination = str(origin), str(destination)

        if origin not in self.vertices or destination not in self.vertices:
            raise KeyError("Non-existent vertex. Add it first and try again.")

        if self.is_pondered:
            if weight == 0:
                raise ValueError("The weight must be a non-null number.")

            self.vertices_list[origin][destination] = weight

            if not self.is_directed:
                self.vertices_list[destination][origin] = weight
        else:
            self.vertices_list[origin][destination] = 1

            if not self.is_directed:
                self.vertices_list[destination][origin] = 1

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

    def adjacency_of(self, vertex):
        vertex = str(vertex)

        return sorted(list(self.vertices_list[vertex].keys()))