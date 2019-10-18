from AdjacencyList.node import Node
from warnings import warn


class AdjListGraph:
    """The Adjacency List Graph object."""

    def __init__(self, nodes, graph_type):
        """The Adjacency List Graph class constructor.

        Parameters
        ----------

        self : AdjListGraph
            An Adjacency List Graph object.

        nodes : list 
            The list containing graph nodes.

        graph_type : str
            The direction graph_type of the graph. It can be 'n-direcionado' or 'direcionado'.

        Returns
        -------

        AdjListGraph

            An Adjacency List Graph object containing dictionary of Node objects, graph_type and initial number of
            edges (0) attributes.

        Methodology
        -----------

        This constructor initializes the AdjListGraph object. 

        """
        if len(nodes) == 0:
            warn("Graphs must have at least one node. A single node graph was automatically created :)")
            self.nodes = {"A": Node('A')}
        else:
            self.nodes = {node: Node(node) for node in nodes}

        self.graph_type = graph_type
        self.nEdges = 0

    def __getitem__(self, key):
        return self.nodes.__getitem__(key)

    def add_edge(self, source, destination):
        """Adds an edge between two given nodes to the graph.

        Parameters
        ----------

        self : AdjListGraph
            An Adjacency List Graph object.

        source : int or str 
            The origin node of the edge.

        destination : int or str
            The destination node of the edge.

        Methodology
        -----------

        This method adds an edge between the given nodes by inserting the identification value of destination node
        into the list of adjacent nodes of origin node. If graph_type is 'n-direcionado', a double way edge is added.
        If not, a one-way edge is added.

        """
        try:
            if self[source].is_adjacent(destination):
                raise ValueError("Edge already exists.")

            if self.graph_type == 'n-direcionado' and source == destination:
                raise ValueError("Self-loops in an undirected graph? No sense.")

            if destination in self.keys():
                self[source].add_adjacent(destination)
                self.nEdges += 1
            else:
                raise ValueError("Destination doesn't exist.")

            if self.graph_type == "n-direcionado" and source != destination:
                self[destination].add_adjacent(source)

        except KeyError:
            raise ValueError("Source node doesn't exist.")

    def remove_edge(self, source, destination):
        """Removes the edge between two given nodes from the graph.

        Parameters
        ----------

        self : AdjListGraph
            An Adjacency List Graph object.

        source : int or str 
            The origin node of the edge.

        destination : int or str
            The destination node of the edge.

        Methodology
        -----------

        This method removes the edge between the given nodes by removing the identification value of destination node
        from the list of adjacent nodes of origin node. If edge or node doesn't exist, an error occurs. If not,
        the edge is removed. If graph_type is 'n-direcionado', origin node is also removed from destination node's
        list of adjacent nodes.

        """
        try:
            self[source].remove_adjacent(destination)

            if self.graph_type == "n-direcionado":
                self[destination].remove_adjacent(source)

            self.nEdges -= 1

        except KeyError:
            raise ValueError("Oh-oh. You must provide existing nodes.")

        except ValueError:
            raise ValueError("How do you want to remove something that does not even exist? lol")

    def is_edge(self, source, destination):
        """Checks if there's an edge between two given nodes.

        Parameters
        ----------

        self : AdjListGraph
            An Adjacency List Graph object.

        source : int or str 
            The origin node of the edge.

        destination : int or str
            The destination node of the edge.

        Methodology
        -----------

        This method checks the list of adjacent nodes of the origin node to confirm if destination node is there.

        """
        try:
            if self[source].is_adjacent(destination):
                print("An edge was found :)")
                return True

            else:
                print("No edges found :(")
                return False

        except KeyError:
            raise ValueError("Oh-oh. You must provide existing nodes.")

    def get_adjacency(self, node):
        """Gets the list of adjacent nodes of the given node.

        Parameters
        ----------

        self : AdjListGraph
            An Adjacency List Graph object.

        node : int or str 
            The identification value of the node wanted.


        Methodology
        -----------

        This method uses the Node object method getAdjacents() to get the list of adjacent nodes of given node and
        print it. If given node doesn't exist, an error occurs.

        """
        try:
            print(node, "->", self[node].get_adjacents())

        except KeyError:
            raise ValueError("Oh-oh. You must provide an existing node.")

    def __repr__(self):
        """Prints Graph with the respective representation (Adjancency List).

        Parameters
        ----------

        self : AdjListGraph
            An Adjacency List Graph object.

        Methodology
        -----------

        For each node, this method calls the Node object method getAdjacents() to get the list of adjacent nodes and
        print it.

        """
        representation = "<AdjListGraph object>\n"
        for node in self.keys():
            representation += str(node) + " -> " + self[node].get_adjacents() + "\n"
        return representation[:-1]

    def number_of_edges(self):
        """Provides the number of edges of the graph.

        Parameters
        ----------

        self : AdjListGraph
            An Adjacency List Graph object.

        Methodology
        -----------

        This method uses nEdges attribute to provide the number of edges of the graph. If graph_type is
        'n-direcionado', the number of edges duplicates.

        """
        print("Number of edges:", self.nEdges)

    def number_of_nodes(self):
        """Provides the number of nodes of the graph.

        Parameters
        ----------

        self : AdjListGraph
            An Adjacency List Graph object.

        Methodology
        -----------

        This method calculates the length of the dictionary nodes, which is the number of nodes of the graph.

        """
        print("Number of nodes:", len(self.nodes))

    def node_degree(self, node):
        """Provides the degree of a given node.

        Parameters
        ----------

        self : AdjListGraph
            An Adjacency List Graph object.

        node : int or str 
            The identification value of the node wanted to be checked.

        Methodology
        -----------

       This method searches the list of adjacent nodes of each node for input and output edges in order to provide
       the respective node's degree.

        """
        if node in self.keys():
            n = 0

            for node2 in self.keys():
                if self[node2].is_adjacent(node):
                    n += 1

            if self.graph_type == "n-direcionado":
                print("Degree:", n)
            else:
                print("Degree:", n + len(self[node].adjacents))
                print("In-Degree:", n)
                print("Out-Degree:", len(self[node].adjacents))
        else:
            raise ValueError("Oh-oh. You must provide an existing node.")

    def keys(self):
        return self.nodes.keys()

    def values(self):
        return self.nodes.values()
