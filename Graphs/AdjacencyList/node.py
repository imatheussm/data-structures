class Node:
    """The Node object."""

    def __init__(self, value):
        """The Node class constructor.

        Parameters
        ----------

        self : Node
            A Node object.

        value : int or str
            The value used to identify the Node.

        Returns
        -------

        Node

            A Node object containing the identification value and an empty start list of adjacent nodes.

        Methodology
        -----------

        This constructor initializes the Node object.

        """
        self.value = value
        self.adjacents = []

    def __str__(self):
        """Node representation.

        Parameters
        ----------

        self : Node
            A Node object.

        Returns
        -------

        str

            The identification value of the Node.

        Methodology
        -----------

        This method represents the Node based on its value.

        """
        return self.value 

    def getAdjacents(self):
        """Get adjacent nodes of the respective Node object.

        Parameters
        ----------

        self : Node
            A Node object.

        Returns
        -------

        str

            Adjacent nodes of the respective Node joined by join() method.

        Methodology
        -----------

        This method converts each item in the adjacent nodes list to string in order to use the join() method to join them.

        """
        return ', '.join(str(x) for x in self.adjacents)

    def addAdj(self, node):
        """Adds an adjacent node to the respective Node.

        Parameters
        ----------

        self : Node
            A Node object.

        node : int or str
            The identification value of the adjacent Node to be added. 

        Methodology
        -----------

        This method adds the given node to the adjacent nodes list of the respective node.
        """
        self.adjacents.append(node)

    def removeAdj(self, node):
        """Removes an adjacent node from the respective Node.

        Parameters
        ----------

        self : Node
            A Node object.

        node : int or str
            The identification value of the adjacent Node to be removed. 

        Methodology
        -----------

        This method removes the given node from the adjacent nodes list of the respective node.
        """
        self.adjacents.remove(node)

    def isAdj(self, node):
        """Check if a given node is adjacent of the respective Node.

        Parameters
        ----------

        self : Node
            A Node object.

        node : int or str
            The identification value of the Node to be checked. 

        Returns
        -----------

        bool 
            Whether the given node is part of adjacent nodes list or not.


        Methodology
        -----------

        This method checks if the given node is in the adjacent nodes list of the respective Node.
        """
        return True if node in self.adjacents else False
