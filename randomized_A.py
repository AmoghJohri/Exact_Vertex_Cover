import random
import itertools
from copy import deepcopy

from make_test_case import get_test_case
from Graph.util  import draw_graph
from Graph.node  import Node
from Graph.graph import Graph 

def randomized_step(G, k):
    while True:
        removed_nodes = []
        removed_edges = {}
        vertex_cover = []
        k_ = k
        while True:
            edges = G.get_edge_list()
            if k_ >= 0 and len(edges) == 0:
                break
            elif k_ < 0:
                break 
            vertex_cover.append(edges[0][random.randint(0, 1)])
            removed_edges[vertex_cover[-1]] = vertex_cover[-1].edgeList
            G.remove_node(vertex_cover[-1])
            removed_nodes.append(vertex_cover[-1])
            k_ = k_ - 1
        if len(vertex_cover) > 0 and k_ >= 0:
            return vertex_cover
        for each in removed_nodes:
            G.add_node(each)
            for e in removed_edges[each]:
                G.add_edge((e, each))
            
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

def randomized(G, k):
    if k < 0:
        return None
    k, cover = reduction(G, k)
    if k < 0:
        return None
    vertex_cover = randomized_step(G, k)
    vertex_cover = [each.value for each in vertex_cover]
    vertex_cover.extend([_.value for _ in cover])
    return vertex_cover
    
if __name__ == "__main__":
    # n0 = Node(0)
    # n1 = Node(1)
    # n2 = Node(2)
    # n3 = Node(3)
    # n4 = Node(4)
    # n0.add_edge(n1)
    # n0.add_edge(n2)
    # n1.add_edge(n2)
    # n2.add_edge(n3)
    # n2.add_edge(n4)
    # n3.add_edge(n4)
    # G  = Graph([n0, n1, n2, n3, n4])
    n = 5
    G = get_test_case(5)
    G_copy = deepcopy(G)
    k = 2
    draw_graph(G)
    vertex_cover = randomized(G, k)
    draw_graph(G_copy, cover=vertex_cover)