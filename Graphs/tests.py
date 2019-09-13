from graph import AdjListGraph

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