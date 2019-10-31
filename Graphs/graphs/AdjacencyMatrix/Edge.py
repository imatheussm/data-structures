class Edge:
    def __init__(self, weight=1):
        self.weight = weight
        self.type = None

    def __repr__(self):
        return str(self.weight)