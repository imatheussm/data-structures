import numpy as np

class AdjMatrixGraph:
    def __init__(self, nNodes, type):
        if nNodes < 1:
            print("Graphs must have at least one node. It appears you don't care about it so a single node graph was automatically created :)")
            self.nNodes = 1
        else:
            self.nNodes = nNodes
        self.matrix = np.zeros((self.nNodes, self.nNodes))
        self.type = type

    def addEdge(self, source, destination):
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
        try:
            if self.matrix[source][destination] == 1 or (self.type == 'n-direcionado' and self.matrix[destination][source] == 1):
                print("An edge was found. :)")
                
            else:
                print("No edges found. :(")
                
        except IndexError:
            print("Oh-oh. You must provide existing nodes.")

    def AdjListNode(self, node):
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
        print("Adjacency Matrix:")
        print(" ", "  ".join([str(x) for x in range(len(self.matrix))]))
        
        for i, x in enumerate(self.matrix):
            print(i, "  ".join([str(int(y)) for y in x]))

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
        try:
            outDegree = 0
            for x in range(self.nNodes):
                if self.matrix[node][x] == 1:
                    outDegree += 1
                    
            inDegree = 0
            for x in range(self.nNodes):
                if self.matrix[x][node]:
                    inDegree += 1
                    
            print("In-Degree: ", inDegree)
            print("Out-Degree: ", outDegree)
            
        except IndexError:
            print("Oh-oh. You must provide existing nodes.")
