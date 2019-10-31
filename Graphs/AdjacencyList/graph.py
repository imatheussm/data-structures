from AdjacencyList.node import Node
from edge import Edge
from warnings import warn
import math
from operator import itemgetter

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
        self.edges = {}

        for node in self.nodes:
            self.edges[node] = {}

        self.t = 0 # time

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

            if destination in self.keys():
                if not self.directed:
                    if origin == destination:
                        raise ValueError("Self-loops in an undirected graph? No sense.")
                    else:
                        self[destination].add_adjacent(origin)
                        self.edges[destination][origin] = Edge(weight)

                self.edges[origin][destination] = Edge(weight)
                self[origin].add_adjacent(destination)
                self.nEdges += 1
            else:
                raise ValueError("Destination doesn't exist.")

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
            del self.edges[origin][destination]

            if not self.directed:
                self[destination].remove_adjacent(origin)
                del self.edges[destination][origin]

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

            return n if not self.directed else (n, len(self[node].adjacents)) 
            # Return tuple (in-degree, out-degree) for directed graphs

        else:
            raise ValueError("Oh-oh. You must provide an existing node.")

    def keys(self):
        return self.nodes.keys()

    def values(self):
        return self.nodes.values()

    def depth_search(self):
        def visit(node):
            self.t += 1
            self[node].found, self[node].color = self.t, 'c'
            
            for adjacent in self[node].adjacents:
                if self[adjacent].color == 'b':
                    self.edges[node][adjacent].tipo = "árvore" # classifying for acyclic algorithm
                    visit(adjacent)

                if self[adjacent].color == 'c':
                    self.edges[node][adjacent].tipo = "retorno" # classifying for acyclic algorithm

            self.t += 1
            self[node].color, self[node].finished = 'p', self.t

        for node in self.nodes:
            self[node].color = 'b'

        for node in self.nodes:
            if self[node].color == 'b':
                visit(node)

        self.t = 0 # time restarted at the end of the algorithm

        # displaying the time each node was found and finished.
        for node in self.nodes:
            print("Nó: ", self[node], "Descoberta: ", self[node].found, "Término: ", self[node].finished)

        # check if classification is right. note: just 'árvore' and 'retorno' classifications are implemented.
        for origem in self.edges:
            for destino in self.edges[origem]:
                print("Aresta ", origem, "-", destino, "~ Tipo: ", self.edges[origem][destino].tipo)

    def breadth_search(self, origin):
        for node in self.nodes:
            if node == origin:
                continue

            self[node].color, self[node].distance = 'b', math.inf
           
        self[origin].color, self[origin].distance = 'c', 0
    
        queue = []
        queue.append(origin)

        while len(queue) != 0:
            node = queue.pop(0)
            for adjacent in self[node].adjacents:
                if self[adjacent].color == 'b':
                    self[adjacent].color = 'c'
                    self[adjacent].distance = self[node].distance + 1
                    self[adjacent].predecessor = node
                    queue.append(adjacent)
            self[node].color = 'p'

        # checking
        for node in self.nodes:
            print("Nó: ", node, "Distância do nó de origem da busca: ", self[node].distance)

    def acyclic(self):
        self.depth_search() # a depth search is a requirement for the acyclic algorithm. idk if we should call this method here, since it's printing something. we can take this out but don't forget to CALL DEPTH_SEARCH BEFORE ACYCLIC!!

        for origin in self.edges:
            for destination in self.edges[origin]:
                if self.edges[origin][destination].tipo == 'retorno':
                    return True
        return False

    def topological(self):
        self.depth_search()

        if self.directed: # i think topological sorting is only for directed graphs. am i wrong?
            list = []
            for node in self.nodes:
                list.append([node, self[node].finished])
            
            list = sorted(list, key=itemgetter(1), reverse=True)
            
            return [l.pop(0) for l in list]
        else:
            warn("O grafo não é direcionado.")

    def shortest_path(self, origin, destination):
        if origin == destination:
            print(origin)

        elif self[destination].predecessor == None:
            print("Não existe caminho de", origin, "para ", destination)

        else:
            self.shortest_path(origin, self[destination].predecessor)
            print(destination)

    def strongly_connected_alg(self, node, low, disc, stackMember, st):
        disc[node] = self.t  # array to store the time each node was found. 
        low[node] = self.t 
        self.t += 1
        stackMember[node] = True
        st.append(node)

        for adjacent in self[node].adjacents:
            if disc[adjacent] == -1:
                self.strongly_connected_alg(adjacent, low, disc, stackMember, st)

                low[node] = min(low[node], low[adjacent])

            elif stackMember[adjacent] == True:
                low[node] = min(low[node], disc[adjacent])
        
        w = -1
        if low[node] == disc[node]:
            while w != node:
                w = st.pop()
                print (w, end=' ')
                stackMember[w] = False
            print("")

    def strongly_connected(self):
        if self.directed:
            disc = [-1] * len(self.nodes)
            low = [-1] * len(self.nodes)
            stackMember = [False] * len(self.nodes)
            st = []

            for i in range(len(self.nodes)):
                if disc[i] == -1:
                    self.strongly_connected_alg(i, low, disc, stackMember, st) 

            self.t = 0  # time restarted. 
        else:
            warn("O grafo não é direcionado!")