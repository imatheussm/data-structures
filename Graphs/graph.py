from node import Node
from errors import contains_Error

class AdjListGraph:
    def __init__(self, nodes, type):
        self.nodes = {node: Node(node) for node in nodes}
        self.type = type

    def addEdge(self, source, destination):
        if (contains_Error(source, destination, self.nodes)):
            return

        if self.nodes[source].isAdj(destination):
            print("Edge already exists.")
            return

        self.nodes[source].addAdj(destination)

        if self.type == "n-direcionado":
            self.nodes[destination].addAdj(source)

        print ("Edge added.")
    
    def removeEdge(self, source, destination):
        if (contains_Error(source, destination, self.nodes)):
            return
        
        if not self.nodes[source].isAdj(destination):
            print("How do you want to remove something that does not even exist? lol")
            return
        
        self.nodes[source].removeAdj(destination)

        if self.type == "n-direcionado":
            self.nodes[destination].removeAdj(source)

        print("Edge removed.")

    def existsEdge(self, source, destination):
        if (contains_Error(source, destination, self.nodes)):
            return

        if self.nodes[source].isAdj(destination):
            print("Yes, there's an edge.")
        else:
            print("No, it doesn't exist.")

    def getAdjacents(self, node):
        print(node.getAdjacents())

    def showGraph(self):
        for node in self.nodes:
            print(node + " -> " + self.nodes[node].getAdjacents())    

    def edgesNumber(self):
        n = 0
        for node in self.nodes.keys():
            n += len(self.nodes[node].adjacents)
        
        if self.type == "n-direcionado":
            n /= 2

        print("Number of edges: ", n)

    def nodesNumber(self):
        print ("Number of nodes: ", len(self.nodes))

    def nodeDegree(self, node):
        n = 0

        for node2 in self.nodes.keys():
            if self.nodes[node2].isAdj(node):
                n += 1

        print("Grau de entrada: ", n)
        print("Grau de saída: ", len(self.nodes[node].adjacents))
