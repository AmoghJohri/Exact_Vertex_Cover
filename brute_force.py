import itertools

from Graph.util  import draw_graph
from Graph.node  import Node
from Graph.graph import Graph 

def brute_force(G, k=-1):
    if k == -1:
        k = G.N()
    vertex_covers = []
    vertices      = G.V()
    for i in range(k + 1):
        _vertices = list(itertools.combinations(vertices, i))
        for each in _vertices:
            covered = []
            for v in each:
                _node = G.get_node_by_value(v)
                for _ in _node.edgeList:
                    covered.append((_.value, v))
                    covered.append((v, _.value))
            covered = list(set(covered))
            if len(covered) == 2*G.M():
                vertex_covers.append(list(each))
        if len(vertex_covers) > 0:
            return vertex_covers

if __name__ == "__main__":
    n0 = Node(0)
    n1 = Node(1)
    n2 = Node(2)
    n3 = Node(3)
    n4 = Node(4)
    n5 = Node(5)
    n0.add_edge(n1)
    n0.add_edge(n3)
    n2.add_edge(n3)
    n4.add_edge(n1)
    G  = Graph([n0, n1, n2, n3, n4])
    draw_graph(G)
    vertex_cover = brute_force(G)
    for each in vertex_cover:
        draw_graph(G, cover=each)