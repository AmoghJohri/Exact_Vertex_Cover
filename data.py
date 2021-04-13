import os 
from Graph.node  import Node
from Graph.graph import Graph 

def get_graph(code=5):
    if code < 10:
        code = "00" + str(code)
    elif code < 100:
        code = "0" + str(code)
    else:
        code = str(code)
    file_name = os.getcwd() + "/public/" + "vc-exact_" + code + ".gr"
    f = open(file_name, 'r')
    i = 0
    for line in f:
        if i == 0:
            var = line.split()
            vertices = int(var[-2])
            edges = int(var[-1])
            nodes = [Node(i) for i in range(1, vertices+1)]
        else:
            var = line.split()
            n1 = int(var[0])
            n2 = int(var[1])
            nodes[n1-1].add_edge(nodes[n2-1])
        i = i + 1
    G = Graph(nodes)
    return G