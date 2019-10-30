from os import getcwd
from sys import path as sys_path

sys_path.append(getcwd())

from AdjacencyList import *
from AdjacencyMatrix import *

x = AdjListGraph([0, 1, 2, 3, 4, 5], True, False)
A = ((0, 1), (1, 2), (2, 3), (3, 1), (1, 4), (4, 3), (0, 4), (5, 4), (5, 0))

for (origin, destination) in A:
    x.add_edge(origin, destination)

x.depth_search()
x.breadth_search(4)
print(x.acyclic())
print(x.topological())
x.shortest_path(4, 2)
print(x.edges)
x.remove_edge(0, 1)
print(x.edges)
x.add_edge(5, 3)
print(x.edges)