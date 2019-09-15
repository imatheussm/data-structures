from AdjacencyList.node import Node

class AdjListGraph:
    def __init__(self, nodes, type):
        self.nodes = {node: Node(node) for node in nodes}
        self.type = type
        self.nEdges = 0

    def addEdge(self, source, destination):
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
        try:
            if self.nodes[source].isAdj(destination):
                print("An edge was found :)")
                
            else:
                print("No edges found :(")
                
        except KeyError:
            print("Oh-oh. You must provide existing nodes.")

    def getAdjacents(self, node):
        try:
            print(node, "->", self.nodes[node].getAdjacents())
            
        except KeyError:
            print("Oh-oh. You must provide an existing node.")

    def showGraph(self):
        for node in self.nodes:
            print(node + " -> " + self.nodes[node].getAdjacents())    

    def edgesNumber(self):
        print("Number of edges:", self.nEdges*2 if self.type == "n-direcionado" else self.nEdges)

    def nodesNumber(self):
        print("Number of nodes: ", len(self.nodes))

    def nodeDegree(self, node):
        try:
            n = 0
            
            for node2 in self.nodes.keys():
                if self.nodes[node2].isAdj(node):
                    n += 1
                    
            print("In-Degree:", n)
            print("Out-Degree:", len(self.nodes[node].adjacents))
            
        except KeyError:
            print("Oh-oh. You must provide an existing node.")
