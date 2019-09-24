from AdjacencyList.node import Node

class AdjListGraph:
    """The Adjacency List Graph object."""

    def __init__(self, nodes, type):
        """The Adjacency List Graph class constructor.

        Parameters
        ----------

        self : AdjListGraph
            An Adjacency List Graph object.

        nodes : list 
            The list containing graph nodes.

        type : str
            The direction type of the graph. It can be 'n-direcionado' or 'direcionado'.

        Returns
        -------

        AdjListGraph

            An Adjacency List Graph object containing dictionary of Node objects, type and initial number of edges (0) attributes.

        Methodology
        -----------

        This constructor initializes the AdjListGraph object. 

        """
        if len(nodes) == 0:
            print("Graphs must have at least one node. A single node graph was automatically created :)")
            self.nodes = {"A": Node('A')}
        else:
            self.nodes = {node: Node(node) for node in nodes}

        self.type = type
        self.nEdges = 0

    def addEdge(self, source, destination):
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

        This method adds an edge between the given nodes by inserting the identification value of destination node into the list of adjacent nodes of origin node. If type is 'n-direcionado', a double way edge is added. If not, a one-way edge is added.

        """
        try:
            if self.nodes[source].isAdj(destination):
                print("Edge already exists.")
                
            elif self.type == 'n-direcionado' and source == destination:
                print("Self-loops in an undirected graph? No sense.")
                
            else:
                self.nodes[source].addAdj(destination)
                
                if self.type == "n-direcionado" and source != destination:
                    self.nodes[destination].addAdj(source)
                    
                self.nEdges += 1
                print("Edge added.")
                
        except KeyError:
            print("This node doesn't exist.")

    def removeEdge(self, source, destination):
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

        This method removes the edge between the given nodes by removing the identification value of destination node from the list of adjacent nodes of origin node. If edge or node doesn't exist, an error occurs. If not, the edge is removed. If type is 'n-direcionado', origin node is also removed from destination node's list of adjacent nodes.

        """
        try:
            self.nodes[source].removeAdj(destination)
            
            if self.type == "n-direcionado":
                self.nodes[destination].removeAdj(source)
                
            self.nEdges -= 1
            print("Edge removed.")
            
        except KeyError:
            print("Oh-oh. You must provide existing nodes.")
            
        except ValueError:
            print("How do you want to remove something that does not even exist? lol")

    def existsEdge(self, source, destination):
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
            if self.nodes[source].isAdj(destination):
                print("An edge was found :)")
                
            else:
                print("No edges found :(")
                
        except KeyError:
            print("Oh-oh. You must provide existing nodes.")

    def getAdjacents(self, node):
        """Gets the list of adjacent nodes of the given node.

        Parameters
        ----------

        self : AdjListGraph
            An Adjacency List Graph object.

        node : int or str 
            The identification value of the node wanted.


        Methodology
        -----------

        This method uses the Node object method getAdjacents() to get the list of adjacent nodes of given node and print it. If given node doesn't exist, an error occurs.

        """
        try:
            print(node, "->", self.nodes[node].getAdjacents())
            
        except KeyError:
            print("Oh-oh. You must provide an existing node.")

    def showGraph(self):
        """Prints Graph with the respective representation (Adjancency List).

        Parameters
        ----------

        self : AdjListGraph
            An Adjacency List Graph object.

        Methodology
        -----------

        For each node, this method calls the Node object method getAdjacents() to get the list of adjacent nodes and print it.

        """
        for node in self.nodes:
            print(node, "->", self.nodes[node].getAdjacents())    

    def edgesNumber(self):
        """Provides the number of edges of the graph.

        Parameters
        ----------

        self : AdjListGraph
            An Adjacency List Graph object.

        Methodology
        -----------

        This method uses nEdges attribute to provide the number of edges of the graph. If type is 'n-direcionado', the number of edges duplicates.

        """
        print("Number of edges:", self.nEdges*2 if self.type == "n-direcionado" else self.nEdges)

    def nodesNumber(self):
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

    def nodeDegree(self, node):
        """Provides the degree of a given node.

        Parameters
        ----------

        self : AdjListGraph
            An Adjacency List Graph object.

        node : int or str 
            The identification value of the node wanted to be checked.

        Methodology
        -----------

       This method searches the list of adjacent nodes of each node for input and output edges in order to provide the respective node's degree.

        """
        try:
            n = 0
            
            for node2 in self.nodes.keys():
                if self.nodes[node2].isAdj(node):
                    n += 1

            if self.type == "n-direcionado":
                print("Degree:", n)
            else:        
                print("Degree:", n+len(self.nodes[node].adjacents))
                print("In-Degree:", n)
                print("Out-Degree:", len(self.nodes[node].adjacents))
            
        except KeyError:
            print("Oh-oh. You must provide an existing node.")
