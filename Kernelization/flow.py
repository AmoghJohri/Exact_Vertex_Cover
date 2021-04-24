import networkx as nx 
from networkx.algorithms.flow import dinitz
from util import drawGraph
from util import drawCustomGraph

def makeBipartiteGraph(G):
    H = nx.DiGraph()
    H.add_nodes_from([-(i+1) for i in list(G.nodes)], bipartite=0)
    H.add_nodes_from([(i+1) for i in list(G.nodes)], bipartite=1)
    s = min(list(H.nodes))-1
    t = max(list(H.nodes))+1
    H.add_node(s, bipartite=1)
    H.add_node(t, bipartite=0)
    for each in list(G.edges):
        node1, node2 = each 
        node1 += 1
        node2 += 1
        H.add_edge(-node1, node2, capacity=1)
        H.add_edge(-node2, node1, capacity=1)
    for each in list(H.nodes):
        if each < 0 and each != s:
            H.add_edge(s, each, capacity=1)
        elif each > 0 and each != t:
            H.add_edge(each, t, capacity=1)
    return H

def getMaximumMatching(H):
    source = min(list(H.nodes))
    sink = max(list(H.nodes))
    flow_value, flow_dict = nx.maximum_flow(H, source, sink, flow_func=dinitz)
    M = nx.Graph()
    M.add_nodes_from(list(H.nodes))
    for each in list(H.edges):
        u, v = each 
        if flow_dict[u][v]  == 1:
            M.add_edge(u, v)
    M.remove_node(source)
    M.remove_node(sink)
    return M

def getBipartiteVertexCover(H, M):
    H.remove_node(min(list(H.nodes)))
    H.remove_node(max(list(H.nodes)))
    A = []
    B = []
    S = []
    for each in list(H.nodes):
        if M.degree(each) == 0:
            if each < 0:
                S.append(each)   
        else:
            if each < 0:
                A.append(each)
            else:
                B.append(each)
    if len(S) == 0:
        return A
    else:
        H_ = nx.DiGraph()
        H_.add_nodes_from(list(H.nodes))
        for each in list(H.edges):
            H_.add_edge(min(each), max(each))
        for each in list(M.edges):
            H_.add_edge(max(each), min(each))
            H_.remove_edge(min(each), max(each))
        Z = []
        for each in list(H.nodes):
            for node in S:
                if nx.has_path(H_, node, each):
                    Z.append(each)
                    break 
    X = []
    Y = []
    for each in list(H.nodes):
        if each < 0:
            X.append(each)
        else:
            Y.append(each)
    X = set(X)
    Y = set(Y)
    Z = set(Z).union(set(S))
    return list((X.difference(Z)).union(Y.intersection(Z)))

def reduction_rule_6_helper(G):
    H = makeBipartiteGraph(G)
    M = getMaximumMatching(H)
    return getBipartiteVertexCover(H, M)

if __name__ == "__main__":
    G = nx.Graph()
    G.add_nodes_from([0, 1, 2])
    G.add_edges_from([(0, 1), (1, 2)])
    H = makeBipartiteGraph(G)
    H = nx.DiGraph()
    H.add_nodes_from([-(i+1) for i in range(5)])
    H.add_nodes_from([(i+1) for i in range(5)])
    source = min(list(H.nodes)) - 1
    sink = max(list(H.nodes)) + 1
    H.add_node(source)
    H.add_node(sink)
    H.add_edge(-1, 1, capcity=1)
    H.add_edge(-1, 3, capcity=1)
    H.add_edge(-2, 3, capcity=1)
    H.add_edge(-3, 2, capcity=1)
    H.add_edge(-3, 3, capcity=1)
    H.add_edge(-3, 4, capcity=1)
    H.add_edge(-4, 3, capcity=1)
    H.add_edge(-5, 2, capcity=1)
    H.add_edge(-5, 3, capcity=1)
    H.add_edge(-5, 5, capcity=1)
    for each in list(H.nodes):
        if each < 0 and each != source:
            H.add_edge(source, each, capacity=1)
        elif each > 0 and each != sink:
            H.add_edge(each, sink, capacity=1)
    M = getMaximumMatching(H)
    cover = getBipartiteVertexCover(H, M)
    for each in cover:
        H.remove_node(each)
    print(cover)
    if len(list(H.edges)) != 0:
        print("Test Case Failed!")