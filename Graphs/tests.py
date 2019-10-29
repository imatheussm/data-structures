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