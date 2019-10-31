import math

from operator import itemgetter


class Graph:
    def __init__(self):
        pass

    def depth_search(self):
        def visit(node):
            self.t += 1
            self[node].found, self[node].color = self.t, 'c'

            for adjacent in self[node].adjacents:
                if self[adjacent].color == 'b':
                    self.edges[node][adjacent].tipo = "árvore"  # classifying for acyclic algorithm
                    visit(adjacent)

                if self[adjacent].color == 'c':
                    self.edges[node][adjacent].tipo = "retorno"  # classifying for acyclic algorithm

            self.t += 1
            self[node].color, self[node].finished = 'p', self.t

        for node in self.nodes:
            self[node].color = 'b'

        for node in self.nodes:
            if self[node].color == 'b':
                visit(node)

        self.t = 0  # time restarted at the end of the algorithm

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

        queue = [origin]

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
        self.depth_search()  # a depth search is a requirement for the acyclic algorithm. idk if we should call this method here, since it's printing something. we can take this out but don't forget to CALL DEPTH_SEARCH BEFORE ACYCLIC!!

        for origin in self.edges:
            for destination in self.edges[origin]:
                if self.edges[origin][destination].tipo == 'retorno':
                    return True
        return False

    def topological(self):
        self.depth_search()

        if self.directed:  # i think topological sorting is only for directed graphs. am i wrong?
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
                print(w, end=' ')
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