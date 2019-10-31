from os import getcwd
from sys import path as sys_path

sys_path.append(getcwd())

from AdjacencyList import *
from AdjacencyMatrix import *


y = AdjListGraph([0, 1, 2, 3, 4, 5], True, False)
B = ((0,1), (1, 2), (2, 3), (3,1), (1, 4), (0,4), (5,0), (5,4), (4,3))

for (origin, destination) in B:
    y.add_edge(origin, destination)

y.strongly_connected()
y.depth_search()
y.breadth_search(4)
print(y.edges)
print(y)
print(y.acyclic())
print(y.topological())
y.shortest_path(4, 2)
y.strongly_connected()