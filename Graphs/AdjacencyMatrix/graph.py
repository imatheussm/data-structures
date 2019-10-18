import numpy as np
from warnings import warn

class AdjMatrixGraph:
    """The Adjacency Matrix Graph object."""

    def __init__(self, number_of_nodes, graph_type):
        """The Adjacency Matrix Graph class constructor.

        Parameters
        ----------

        self : AdjMatrixGraph
            
            An Adjacency Matrix Graph object.

        number_of_nodes : int
            
            The number of nodes of the graph.

        graph_type : str
            
            The direction graph_type of the graph. It can be 'n-direcionado' or 'direcionado'.

        Returns
        -------

        AdjMatrixGraph

            An Adjacency Matrix Graph object containing the attributes number of nodes, matrix representation and graph_type.

        Methodology
        -----------

        This constructor initializes the AdjMatrixGraph object. 

        """
        if number_of_nodes < 1:
            warn("Graphs must have at least one node. It appears you don't care about it, so a single node graph was automatically created :)")
            self.nNodes = 1
        else:
            self.nNodes = number_of_nodes
        self.matrix = np.zeros((self.nNodes, self.nNodes))
        self.graph_type = graph_type
        
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
        
        This method verifies if a given pair of (source, destination) vertices exists in the adjacency matrix.
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
        return self.nNodes

    def add_edge(self, source, destination):
        """Adds an edge between two given nodes of the graph.

        Parameters
        ----------

        self : AdjMatrixGraph
            An Adjacency Matrix Graph object.

        source : int 
            The origin node of the edge.

        destination : int 
            The destination node of the edge.

        Methodology
        -----------

        This method adds an edge between two given nodes by replacing, in the respective pair(source, destination), number 0 with number 1. If graph_type is 'n-direcionado', a double way edge is added. If not, a one-way edge is added.

        """
        try:
            if self[source][destination] == 1:
                raise ValueError("This edge already exists.")

            if self.graph_type == 'n-direcionado':
                if source == destination:
                    raise ValueError("Self-loops in an undirected graph? No sense")
                self[destination][source] = 1

            self[source][destination] = 1

        except IndexError:
            raise ValueError("Oh-oh. You must provide existing nodes.")

    def remove_edge(self, source, destination):
        """Removes the edge between two given nodes from the graph.

        Parameters
        ----------

        self : AdjMatrixGraph
            An Adjacency Matrix Graph object.

        source : int 
            The origin node of the edge.

        destination : int 
            The destination node of the edge.

        Methodology
        -----------

        This method removes the edge between the given nodes by replacing, in the respective pair(source, destination) number 1 with number 0. If edge or node doesn't exist, an error occurs. If not, the edge is removed.

        """
        try:
            if self[source][destination] == 0:
                raise ValueError("How do you want to remove something that does not even exist? lol")
            
            self[source][destination] = 0
            
            if self.graph_type == 'n-direcionado':
                self[destination][source] = 0
                
        except IndexError:
            raise ValueError("Oh-oh. You must provide existing nodes.")

    def is_edge(self, source, destination):
        """Checks if there's an edge between two given nodes.

        Parameters
        ----------

        self : AdjMatrixGraph
            An Adjacency Matrix Graph object.

        source : int
            The origin node of the edge.

        destination : int 
            The destination node of the edge.

        Methodology
        -----------

        This method looks for number 1 in the respective pair(source, destination) in the adjacency matrix in order to check the existence of an edge.
        """
        try:
            if self[source][destination] == 1:
                print("An edge was found. :)")
                return True
            print("No edges found. :(")
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
            adjacency = [x for x in range(self.nNodes) if self[node][x] == 1]
                    
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
        max_length = len(str(self.nNodes))
        representation = "<AdjMatrixGraph object>\n"
        representation += (max_length + 3) * " " + " ".join([str(x).ljust(max_length, " ") for x in range(len(self))]) + "\n\n"
        
        for i, x in enumerate(self):
            representation += str(i).ljust(max_length + 2, " ") + " ".join([str(int(y)).rjust(max_length, " ") for y in x]) + "\n"
        
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
        n = self.matrix.sum()
        nEdges = n if self.graph_type == "direcionado" else int(n/2) 
        print("Number of edges:", nEdges)

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
        print("Number of nodes:", self.nNodes) 

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
            for x in range(self.nNodes):
                if self[node][x]:
                    outDegree += 1

            inDegree = 0
            for x in range(self.nNodes):
                if self[x][node]:
                    inDegree += 1

            if self.graph_type == "n-direcionado":
                print("Degree:", inDegree)
            else:
                print("Degree:", inDegree+outDegree)        
                print("In-Degree: ", inDegree)
                print("Out-Degree: ", outDegree)
                
        except IndexError:
            raise ValueError("Oh-oh. You must provide existing nodes.")
