from AdjacencyList.node import Node
from edge import Edge
from warnings import warn


class AdjListGraph:
    """The Adjacency List Graph object."""

    def __init__(self, nodes, directed, pondered):
        """The Adjacency List Graph class constructor.

        Parameters
        ----------

        self : AdjListGraph
            An Adjacency List Graph object.

        nodes : list 
            The list containing graph nodes.

        directed: bool
            The direction of the graph. If directed=True, graph is directed. If directed=False, graph is undirected.

        pondered: bool
            The graph classification by edge weight. If pondered=True, graph is pondered. If pondered=False, graph is not pondered.

        Returns
        -------

        AdjListGraph

            An Adjacency List Graph object containing dictionary of Node objects, graph type (directed/undirected, pondered/not pondered) and initial number of
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

        self.directed = directed
        self.pondered = pondered
        self.nEdges = 0
        self.edges = []
        self.t = 0

    def __getitem__(self, key):
        return self.nodes.__getitem__(key)

    def add_edge(self, origin, destination, weight=1):
        """Adds an edge between two given nodes to the graph.

        Parameters
        ----------

        self : AdjListGraph
            An Adjacency List Graph object.

        origin : int or str 
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
            if self[origin].is_adjacent(destination):
                raise ValueError("Edge already exists.")

            if not self.directed and origin == destination:
                raise ValueError("Self-loops in an undirected graph? No sense.")

            if destination in self.keys():
                self.edges.append(Edge(origin, destination, weight))    
                self[origin].add_adjacent(destination)
                self.nEdges += 1
            else:
                raise ValueError("Destination doesn't exist.")

            if not self.directed and origin != destination:
                self[destination].add_adjacent(origin)
                #self.edges += Edge(destination, origin, weight)

        except KeyError:
            raise ValueError("There's something wrong with the nodes.")


    def remove_edge(self, origin, destination):
        """Removes the edge between two given nodes from the graph.

        Parameters
        ----------

        self : AdjListGraph
            An Adjacency List Graph object.

        origin : int or str 
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
            self[origin].remove_adjacent(destination)
            self.remove_from_edges(origin, destination)

            if not self.directed:
                self[destination].remove_adjacent(origin)
                self.remove_from_edges(destination, origin)

            self.nEdges -= 1

        except KeyError:
            raise ValueError("Oh-oh. You must provide existing nodes.")

        except ValueError:
            raise ValueError("How do you want to remove something that does not even exist? lol")

    def is_edge(self, origin, destination):
        """Checks if there's an edge between two given nodes.

        Parameters
        ----------

        self : AdjListGraph
            An Adjacency List Graph object.

        origin : int or str 
            The origin node of the edge.

        destination : int or str
            The destination node of the edge.

        Methodology
        -----------

        This method checks the list of adjacent nodes of the origin node to confirm if destination node is there.

        """
        try:
            return True if self[origin].is_adjacent(destination) else False

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
            #print(node, "->", self[node].get_adjacents())
            return self[node].get_adjacents()

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
            representation += str(node) + " -> " + ", ".join(str(item) for item in self[node].get_adjacents()) + "\n"
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
        return self.nEdges

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
        return len(self.nodes)

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

            return n if not self.directed else (n, len(self[node].adjacents)) # If directed, the degree is the sum of n + self[node]...
            # Return tuple (in-degree, out-degree)

        else:
            raise ValueError("Oh-oh. You must provide an existing node.")

    def keys(self):
        return self.nodes.keys()

    def values(self):
        return self.nodes.values()

    def remove_from_edges(self, origin, destination):
        for edge in self.edges:
            if edge.origin == origin and edge.destination == destination:
                self.edges.remove(edge)

    def depth_search(self):
        def visit(node):
            self.t += 1
            self[node].found, self[node].color = self.t, 'c'
            
            for adjacent in self[node].adjacents:
                if self[adjacent].color == 'b':
                    self.get_edge(node, adjacent).tipo = "árvore" # Só pra saber se tá classificando direito
                    self[adjacent].predecessor = node
                    visit(adjacent)
                if self[adjacent].color == 'c':
                    self.get_edge(node, adjacent).tipo = "retorno" # Necessário pro algoritmo de grafo acíclico
            
            self[node].color = 'p'
            self.t += 1
            self[node].finished = self.t

        # Os nós já inicializam com a cor branca, logo não precisa fazer esse procedimento
        for node in self.nodes:
            if self[node].color == 'b':
                visit(node)

        # Só p saber se tá certo
        for node in self.nodes:
            print("Nó: ", self[node], "Descoberta: ", self[node].found, "Término: ", self[node].finished)

        self.t = 0

        # Só p checar se táokei
        for edge in self.edges:
            print("Origem: ", edge.origin, "Destino: ", edge.destination, "Tipo: ", edge.tipo)

    # Pegar o objeto aresta correspondente
    def get_edge(self, origin, destination):
        for edge in self.edges:
            if edge.origin == origin and edge.destination == destination:
                return edge


        