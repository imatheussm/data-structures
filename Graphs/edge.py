class Edge:
    def __init__(self, origin, destination, weight=1):
        self.origin = origin
        self.destination = destination
        self.weight = weight
        self.tipo = None

    def __repr__(self):
        return "(" + str(self.origin) + ", " + str(self.destination) + ", " + str(self.weight) + ")"
