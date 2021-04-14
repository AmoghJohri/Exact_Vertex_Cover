import itertools
from copy import deepcopy

from Graph.util  import draw_graph
from Graph.node  import Node
from Graph.graph import Graph 

def brute_force(G, k):
    vertex_covers = []
    vertices      = G.V()
    for i in range(k + 1):
        _vertices = list(itertools.combinations(vertices, i))
        for each in _vertices:
            cover   = []
            covered = []
            for v in each:
                _node = G.get_node_by_value(v)
                for _ in _node.edgeList:
                    cover.append(v)
                    covered.append((_.value, v))
                    covered.append((v, _.value))
            covered = list(set(covered))
            if len(covered) == 2*G.M():
                vertex_covers.append(list(set(cover)))
        if len(vertex_covers) > 0:
            return vertex_covers

def reduction_rule_1(G):
    """ If there are any isolated vertices, remove them """
    for each in G.nodes:
        if each.get_degree() == 0:
            G.remove_node(each)

def reduction_rule_2(G, k, cover=[]):
    """ If there are any vertices with degree > k, remove them"""
    tag = 0
    for each in G.nodes:
        if each.get_degree() > k:
            cover.append(each)
            G.remove_node(each)
            k = k - 1
            tag = 1
        if k < 0:
            return -1, tag
        reduction_rule_1(G)
    return k, tag

def reduction(G, k):
    cover = []
    while True:
        k, tag = reduction_rule_2(G, k, cover)
        if k < 0:
            return -1, cover
        elif tag == 0:
            break 
    return k, cover

def kernelization(G, k):
    if k < 0:
        return None
    k, cover = reduction(G, k)
    if k < 0:
        return None
    vertex_cover = brute_force(G, k)
    return vertex_cover
    
if __name__ == "__main__":
    n0 = Node(0)
    n1 = Node(1)
    n2 = Node(2)
    n0.add_edge(n1)
    n1.add_edge(n2)
    G  = Graph([n0, n1, n2])
    G_copy = deepcopy(G)
    k = 2
    draw_graph(G)
    vertex_cover = kernelization(G, k)
    for each in vertex_cover:
        draw_graph(G_copy, cover=each)