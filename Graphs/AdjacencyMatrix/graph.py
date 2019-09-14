from AdjacencyMatrix.node import Node
import numpy as np 
from Graphs.errors import limitError

class AdjMatrixGraph:
    def __init__(self, nNodes, type):
        self.nNodes = nNodes
        self.matrix = np.zeros((self.nNodes, self.nNodes))
        self.type = type

    def addEdge(self, source, destination):
        if (limitError(source, destination, self.nNodes)):
            return
        
        if self.matrix[source][destination] == 1:
            print("This edge already exists.")
            return

        if self.type == 'n-direcionado':
            if source == destination:
                print("Self-loops in an undirected graph? No sense.")
                return

            self.matrix[destination][source] = 1

        self.matrix[source][destination] = 1

    def removeEdge(self, source, destination):
        if (limitError(source, destination, self.nNodes)):
            return

        if self.matrix[source][destination] == 0:
            print("How do you want to remove something that does not even exist? lol")
            return

        self.matrix[source][destination] = 0

        if self.type == 'n-direcionado':
            self.matrix[destination][source] = 0

    def existsEdge(self, source, destination):
        if self.matrix[source][destination] == 1:
            print("Yes, there's an edge.")
        else:
            print("No, there's no edge.")

    def AdjListNode(self, node):
        if node not in range(0, self.nNodes):
            print("It seems this node doesn't exist. :(")
            return
        
        print(node, "-> ", end='')
        list = []
        for x in range(0, self.nNodes):
            if self.matrix[node][x] == 1:
                list.append(x)

        print(", ".join(str(x) for x in list))

    def showGraph(self):
        print("Adjacency Matrix:")
        print (" ", "  ".join([str(x) for x in range(len(self.matrix))]))
        for i, x in enumerate(self.matrix):
            print (i, "  ".join([str(int(y)) for y in x]))

    def numberNodes(self):
        print("There are ", self.nNodes, " nodes.")

    def numberEdges(self):
        n = 0
        for x in range(self.nNodes):
            for y in range(self.nNodes):
                if self.matrix[x][y] == 1:
                    n += 1

        if self.type == "n-direcionado":
            n /= 2
        
        print("This graph has {:.0f} edges.". format(n))

    def nodeDegree(self, node):
        if node not in range(self.nNodes):
            print("This node doesn't exist.")
            return
        
        outDegree = 0
        for x in range(self.nNodes):
            if self.matrix[node][x] == 1:
                outDegree += 1
            
        inDegree = 0
        for x in range(self.nNodes):
            if self.matrix[x][node]:
                inDegree += 1

        print("Grau de entrada: ", inDegree)
        print("Grau de saída: ", outDegree)