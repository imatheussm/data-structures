from warnings import warn

import numpy as np

from graphs.AdjacencyMatrix.Edge import Edge
from graphs.Graph import Graph


class AdjMatrixGraph(Graph):
    """The Adjacency Matrix Graph object."""

    def __init__(self, number_of_nodes, directed, pondered):
        """The Adjacency Matrix Graph class constructor.

        Parameters
        ----------

        self : AdjMatrixGraph
            
            An Adjacency Matrix Graph object.

        number_of_nodes : int
            
            The number of nodes of the graph.

       directed: bool
            The direction of the graph. If directed=True, graph is directed. If directed=False, graph is undirected.

        pondered: bool
            The graph classification by edge weight. If pondered=True, graph is pondered. If pondered=False, graph is not pondered.

        Returns
        -------

        AdjMatrixGraph

            An Adjacency Matrix Graph object containing the attributes number of nodes, matrix representation and graph type (directed/undirected, pondered/not pondered).

        Methodology
        -----------

        This constructor initializes the AdjMatrixGraph object. 

        """
        super().__init__()

        if number_of_nodes < 1:
            warn("Graphs must have at least one node. A single node graph was automatically created :)")
            self.number_of_nodes = 1
        else:
            self.number_of_nodes = number_of_nodes
        self.matrix = np.zeros((self.number_of_nodes, self.number_of_nodes))
        self.directed = directed
        self.pondered = pondered

    def __getitem__(self, *args, **kwargs):
        """Allows the object to use the [] notation.
        
        Arguments
        ---------
        
        self : AdjMatrixGraph
        
            An Adjacency Matrix Graph object.
        
        *args : list
        
            A list of arguments.
            
        **kwargs : dict
        
            A list of keyworded arguments.
            
        Returns
        -------
        
        Object
        
            The object contained in the provided index.
            
        Methodology
        -----------
        
        This is just a wrapper to use NumPy Array's __getitem__() method.
        
        """
        return self.matrix.__getitem__(*args, **kwargs)

    def __iter__(self, *args, **kwargs):
        """Allows the object to be iterable.
        
        Arguments
        ---------
        
        self : AdjMatrixGraph
        
            An AdjMatrixGraph object.
        
        *args : list
        
            A list of arguments.
            
        **kwargs : dict
        
            A list of keyworded arguments.
            
        Returns
        -------
        
        iterator
        
            An iterator for the items of the object.
            
        Methodology
        -----------
        
        This is just a wrapper to use NumPy Array's __iter__() method.
        """
        return self.matrix.__iter__(*args, **kwargs)

    def __contains__(self, edge):
        """Allows the usage of the 'in' operator.
        
        Arguments
        ---------
        
        self : AdjMatrixGraph
        
            An AdjMatrixGraph object.
        
        edge : tuple(int, int)
        
            The edge origin and destination indexes.
            
        Returns
        -------
        
        bool
        
            The result of the verification.
            
        Methodology
        -----------
        
        This method verifies if a given pair of (origin, destination) vertices exists in the adjacency matrix.
        """
        try:
            return self[edge[0]][edge[1]] == 1
        except:
            return False

    def __len__(self):
        """Allows the usage of the built-in len() function.
        
        Arguments
        ---------
        
        self : AdjMatrixGraph
        
            An AdjMatrixGraph object.
            
        Returns
        -------
        
        int
        
            The number of nodes in the current graph.
            
        Methodology
        -----------
        
        This method just returns self.nNodes.
        """
        return self.number_of_nodes

    def add_edge(self, origin, destination, weight=1):
        """Adds an edge between two given nodes of the graph.

        Parameters
        ----------

        self : AdjMatrixGraph
            An Adjacency Matrix Graph object.

        origin : int
            The origin node of the edge.

        destination : int
            The destination node of the edge.

        Methodology
        -----------

        This method adds an edge between two given nodes by replacing, in the respective pair(origin, destination), number 0 with number 1. If graph_type is 'n-direcionado', a double way edge is added. If not, a one-way edge is added.

        """
        try:
            if self[origin][destination] == 1:
                raise ValueError("This edge already exists.")

            if not self.directed:
                if origin == destination:
                    raise ValueError("Self-loops in an undirected graph? No sense")
                self[destination][origin] = weight

            self[origin][destination] = weight

        except IndexError:
            raise ValueError("Oh-oh. You must provide existing nodes.")

    def remove_edge(self, origin, destination):
        """Removes the edge between two given nodes from the graph.

        Parameters
        ----------

        self : AdjMatrixGraph
            An Adjacency Matrix Graph object.

        origin : int 
            The origin node of the edge.

        destination : int 
            The destination node of the edge.

        Methodology
        -----------

        This method removes the edge between the given nodes by replacing, in the respective pair(origin, destination) number 1 with number 0. If edge or node doesn't exist, an error occurs. If not, the edge is removed.

        """
        try:
            if self[origin][destination] == 0:
                raise ValueError("How do you want to remove something that does not even exist? lol")

            self[origin][destination] = 0

            if not self.directed:
                self[destination][origin] = 0

        except IndexError:
            raise ValueError("Oh-oh. You must provide existing nodes.")

    def is_edge(self, origin, destination):
        """Checks if there's an edge between two given nodes.

        Parameters
        ----------

        self : AdjMatrixGraph
            An Adjacency Matrix Graph object.

        origin : int
            The origin node of the edge.

        destination : int 
            The destination node of the edge.

        Methodology
        -----------

        This method looks for number 1 in the respective pair(origin, destination) in the adjacency matrix in order to check the existence of an edge.
        """
        try:
            if self[origin][destination] > 0: return True
            return False

        except IndexError:
            raise ValueError("Oh-oh. You must provide existing nodes.")

    def get_adjacency(self, node):
        """Gets the list of adjacent nodes of the given node.

        Parameters
        ----------

        self : AdjMatrixGraph
            An Adjacency Matrix Graph object.

        node : int
            The node wanted.


        Methodology
        -----------

        This method goes to the respective line (node) and goes through the columns looking for number 1,which indicates an adjacent node. In the end, a list of all adjacent nodes of the given node is shown.

        """
        try:
            adjacency = [x for x in range(self.number_of_nodes) if self[node][x] == 1]

            print(node, "-> ", end='')
            print(", ".join(str(x) for x in adjacency))

        except IndexError:
            raise ValueError("Oh-oh. You must provide existing nodes.")

    def __repr__(self):
        """Prints Graph with the respective representation (Adjancency Matrix).

        Parameters
        ----------

        self : AdjMatrixGraph
            An Adjacency Matrix Graph object.

        Methodology
        -----------

        This method prints the graph in a matrix format with lines and columns identification.

        """
        max_length = len(str(self.number_of_nodes))
        representation = "<AdjMatrixGraph object>\n"
        representation += (max_length + 2) * " " + " ".join(
            [str(x).ljust(max_length, " ") for x in range(len(self))]) + "\n\n"

        for i, x in enumerate(self):
            representation += str(i).ljust(max_length + 2, " ") + " ".join(
                [str(int(y)).ljust(max_length, " ") for y in x]) + "\n"

        return representation[:-1]

    def number_of_edges(self):
        """Provides the number of edges of the graph.

        Parameters
        ----------

        self : AdjMatrixGraph
            An Adjacency Matrix Graph object.

        Methodology
        -----------

        This method goes through the matrix looking for number 1. Every time number 1 is found, the counter is increased. If graph_type is 'n-direcionado', the counter is halved.

        """
        return self.matrix.sum() if self.directed else int(self.matrix.sum() / 2)

    def number_of_nodes(self):
        """Provides the number of nodes of the graph.
        
        Parameters
        ----------

        self : AdjMatrixGraph
            An Adjacency Matrix Graph object.

        Methodology
        -----------

        This method just uses the attribute nNodes to inform the number of nodes of the graph.

        """
        return self.number_of_nodes

    def node_degree(self, node):
        """Provides the degree of a given node.

        Parameters
        ----------

        self : AdjMatrixGraph
            An Adjacency Matrix Graph object.

        node : int 
            The node wanted.

        Methodology
        -----------

       This method goes through the matrix looking for input and output edges in order to provide the respective node's degree.

        """
        try:
            outDegree = 0
            for x in range(self.number_of_nodes):
                if self[node][x]:
                    outDegree += 1

            inDegree = 0
            for x in range(self.number_of_nodes):
                if self[x][node]:
                    inDegree += 1

            return inDegree if not self.directed else (inDegree, outDegree)

        except IndexError:
            raise ValueError("Oh-oh. You must provide existing nodes.")

    def remove_from_edges(self, origin, destination):
        for edge in self.edges:
            if edge.origin == origin and edge.destination == destination:
                self.edges.remove(edge)
