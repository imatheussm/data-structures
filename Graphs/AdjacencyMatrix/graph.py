import numpy as np

class AdjMatrixGraph:
    """The Adjacency Matrix Graph object."""

    def __init__(self, nNodes, type):
        """The Adjacency Matrix Graph class constructor.

        Parameters
        ----------

        self : AdjMatrixGraph
            An Adjacency Matrix Graph object.

        nNodes : int 
            The number of nodes of the graph.

        type : str
            The direction type of the graph. It can be 'n-direcionado' or 'direcionado'.

        Returns
        -------

        AdjMatrixGraph

            An Adjacency Matrix Graph object containing the attributes number of nodes, matrix representation and type.

        Methodology
        -----------

        This constructor initializes the AdjMatrixGraph object. 

        """
        if nNodes < 1:
            print("Graphs must have at least one node. It appears you don't care about it, so a single node graph was automatically created :)")
            self.nNodes = 1
        else:
            self.nNodes = nNodes
        self.matrix = np.zeros((self.nNodes, self.nNodes))
        self.type = type

    def addEdge(self, source, destination):
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

        This method adds an edge between two given nodes by replacing, in the respective pair(source, destination), number 0 with number 1. If type is 'n-direcionado', a double way edge is added. If not, a one-way edge is added.

        """
        try:
            if self.matrix[source][destination] == 1:
                print("This edge already exists.")
                
            else:
                if self.type == 'n-direcionado':
                    if source == destination:
                        print("Self-loops in an undirected graph? No sense")
                        
                    else:
                        self.matrix[source][destination] = 1
                        self.matrix[destination][source] = 1
                        print("Edge added.")
                        
                else:
                    self.matrix[source][destination] = 1
                    print("Edge added.")
                    
        except IndexError:
            print("Oh-oh. You must provide existing nodes.")

    def removeEdge(self, source, destination):
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
            if self.matrix[source][destination] == 0:
                print("How do you want to remove something that does not even exist? lol")
                
            else:
                self.matrix[source][destination] = 0
                
                if self.type == 'n-direcionado':
                    self.matrix[destination][source] = 0
                    
                print("Edge removed.")
                
        except IndexError:
            print("Oh-oh. You must provide existing nodes.")

    def existsEdge(self, source, destination):
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
            if self.matrix[source][destination] == 1:
                print("An edge was found. :)")
                
            else:
                print("No edges found. :(")
                
        except IndexError:
            print("Oh-oh. You must provide existing nodes.")

    def getAdjacents(self, node):
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
            list = []
            
            for x in range(self.nNodes):
                if self.matrix[node][x] == 1:
                    list.append(x)
                    
            print(node, "-> ", end='')
            print(", ".join(str(x) for x in list))
            
        except IndexError:
            print("Oh-oh. You must provide existing nodes.")

    def showGraph(self):
        """Prints Graph with the respective representation (Adjancency Matrix).

        Parameters
        ----------

        self : AdjMatrixGraph
            An Adjacency Matrix Graph object.

        Methodology
        -----------

        This method prints the graph in a matrix format with lines and columns identification.

        """
        print(" ", "  ".join([str(x) for x in range(len(self.matrix))]))
        
        for i, x in enumerate(self.matrix):
            print(i, "  ".join([str(int(y)) for y in x]))

    def edgesNumber(self):
        """Provides the number of edges of the graph.

        Parameters
        ----------

        self : AdjMatrixGraph
            An Adjacency Matrix Graph object.

        Methodology
        -----------

        This method goes through the matrix looking for number 1. Every time number 1 is found, the counter is increased. If type is 'n-direcionado', the counter is halved.

        """
        n = 0
           
        for x in range(self.nNodes):
            for y in range(self.nNodes):
                if self.matrix[x][y] == 1:
                    n += 1
                        
        if self.type == "n-direcionado":
           n /= 2
                
        print("This graph has {:.0f} edges.". format(n))

    def nodesNumber(self):
        """Provides the number of nodes of the graph.
        
        Parameters
        ----------

        self : AdjMatrixGraph
            An Adjacency Matrix Graph object.

        Methodology
        -----------

        This method just uses the attribute nNodes to inform the number of nodes of the graph.

        """
        print("There are ", self.nNodes, " nodes.") 

    def nodeDegree(self, node):
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
                if self.matrix[node][x] == 1:
                    outDegree += 1
                    
            inDegree = 0
            for x in range(self.nNodes):
                if self.matrix[x][node]:
                    inDegree += 1

            if self.type == "n-direcionado":
                print("Grau:", inDegree)
            else:
                print("Grau:", inDegree+outDegree)        
                print("In-Degree: ", inDegree)
                print("Out-Degree: ", outDegree)
                
        except IndexError:
            print("Oh-oh. You must provide existing nodes.")
