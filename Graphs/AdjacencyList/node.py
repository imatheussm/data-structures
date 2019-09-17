class Node:
    def __init__(self, value):
        self.value = value
        self.adjacents = []

    def __str__(self):
        return self.value 

    def getAdjacents(self):
            return ', '.join(x for x in self.adjacents)

    def addAdj(self, node):
        self.adjacents.append(node)

    def removeAdj(self, node):
        self.adjacents.remove(node)

    def isAdj(self, node):
        return True if node in self.adjacents else False
