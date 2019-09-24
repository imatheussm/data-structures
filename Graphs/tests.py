from os import getcwd
from sys import path as sys_path

sys_path.append(getcwd())

from AdjacencyList import *
from AdjacencyMatrix import *

print("OLA isso e um teste")
print ("# ---- POR MATRIZ DE ADJACÊNCIA -----")
x = AdjMatrixGraph(4, 'n-direcionado')
x.addEdge(2, 1)
x.addEdge(2, 0)

print('teste:')
x.showGraph()
x.existsEdge(2, 1)
x.AdjListNode(2)
y = AdjMatrixGraph(-2, 'n-direcionado')
y.numberEdges()
y.nodeDegree('iai')
y.showGraph()
print ("# ---- POR LISTAS DE ADJACÊNCIA -----")
t1 = AdjListGraph(['A', 'B', '7'], 'direcionado')
t1.addEdge('A', 'A')
t1.showGraph()
t1.showGraph()
t1.addEdge('B', '7')
t1.showGraph()
t1.addEdge('B', '7')
t1.addEdge('B', 'A')
t1.addEdge('B', 'B')
t1.existsEdge('C', '7')
print("teste aki: ")
t1.showGraph()
t1.edgesNumber()
t1.nodeDegree('B')

print("TESTE 2")
xx = AdjListGraph([0, 2, 4, 3], 'n-direcionado')
xx.addEdge(0, 4)
xx.showGraph()
xx.addEdge(4, 2)
xx.addEdge(4, 4)
xx.showGraph()
xx.edgesNumber()
xx.getAdjacents(4)
xx.nodeDegree(4)
print("-------------")
y = AdjMatrixGraph(8, 'n-direcionado')
y.showGraph()
y.addEdge(4,2)
y.existsEdge(2,4)
y.showGraph()