import random 

from Graph.node  import Node
from Graph.graph import Graph 
from Graph.util  import draw_graph

def get_test_case(n):
    nodes = [Node(i) for i in range(0, n)]
    m = random.randint(0, int((n*n)/2))
    for i in range(m):
        s = random.randint(0, n-1)
        f = random.randint(0, n-1)
        if s != f:
            nodes[s].add_edge(nodes[f])
        else:
            i = i - 1
    G = Graph(nodes)
    return G

if __name__ == "__main__":
    G = get_test_case(5, k=2)
    draw_graph(G)