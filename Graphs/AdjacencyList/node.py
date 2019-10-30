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
        self.color = None
        self.found = None # the time the node was found.
        self.finished = None # the time the discovery is finished.
        self.predecessor = None
        self.distance = None

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
        return str(self.value) 

    def __repr__(self):
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
        return str(self.value) + " -> " + self.get_adjacents()

    def get_adjacents(self):
        """Gets the adjacent nodes of the respective Node object.

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

        This method converts each item in the list of adjacent nodes to string in order to use the join()method to
        finally show them.

        """
        return self.adjacents

    def add_adjacent(self, node):
        """Adds an adjacent node to the respective Node.

        Parameters
        ----------

        self : Node
            A Node object.

        node : int or str
            The identification value of the adjacent node to be added. 

        Methodology
        -----------

        This method inserts the given node into the list of adjacent nodes of the respective Node.
        """
        self.adjacents.append(node)

    def remove_adjacent(self, node):
        """Removes an adjacent node from the respective Node.

        Parameters
        ----------

        self : Node
            A Node object.

        node : int or str
            The identification value of the adjacent node to be removed. 

        Methodology
        -----------

        This method removes the given node from the list of adjacent nodes of the respective Node.
        """
        self.adjacents.remove(node)

    def is_adjacent(self, node):
        """Checks if a given node is adjacent of the respective Node.

        Parameters
        ----------

        self : Node
            A Node object.

        node : int or str
            The identification value of the Node to be checked. 

        Returns
        -----------

        bool 
            Whether the given node is part of the list of adjacent nodes or not.


        Methodology
        -----------

        This method checks if the given node is in the list of adjacent nodes of the respective Node.
        """
        return True if node in self.adjacents else False
