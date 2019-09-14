from os import getcwd
from sys import path as sys_path

sys_path.append(getcwd())

from AdjacencyList import *
from AdjacencyMatrix import *

print ("# ---- POR MATRIZ DE ADJACÊNCIA -----")
x = AdjMatrixGraph(6, 'n-direcionado')
x.addEdge(3, 4)
x.addEdge(3, 2)
x.addEdge(7, 1)
x.AdjListNode(3)
x.removeEdge(3, 5)
x.showGraph()
x.numberEdges()
x.nodeDegree(3)

print ("# ---- POR LISTAS DE ADJACÊNCIA -----")
t1 = AdjListGraph(['A', 'B', '7'], 'direcionado')
t1.showGraph()
t1.addEdge('B', '7')
t1.showGraph()
t1.addEdge('C', 'B')
t1.addEdge('A', '7')
t1.showGraph()

t1.addEdge('7', 'B')
t1.showGraph()

t1.existsEdge('B', 'A')

t1.edgesNumber()
t1.nodesNumber()
t1.nodeDegree('A')