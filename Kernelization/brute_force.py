import networkx as nx 
import itertools

def brute_force(G, k=-1):
    if k == -1:
        k = len(list(G.nodes))
    vertex_covers = []
    vertices      = list(G.nodes)
    for i in range(k + 1):
        _vertices = list(itertools.combinations(vertices, i))
        for each in _vertices:
            covered = []
            for v in each:
                for edge in G.edges(v):
                    covered.append((min(edge), max(edge)))
            covered = list(set(covered))
            if len(covered) == len(G.edges):
                vertex_covers.append(list(each))
        if len(vertex_covers) > 0:
            return vertex_covers