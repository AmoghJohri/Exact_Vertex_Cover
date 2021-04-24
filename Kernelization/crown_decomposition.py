import networkx    as nx 
from   copy        import deepcopy

from   util        import drawGraph
from   util        import getCustomGraph
from   util        import drawCustomGraph
from   util        import generateRandomGraph

def crownDecomposition(G):
    M1 = nx.maximal_matching(G)
    O = list(G.nodes)
    for each in M1:
        u, v = each 
        try:
            O.remove(u)
        except:
            pass 
        try:
            O.remove(v)
        except:
            pass 
    NO = []
    for each in O:
        NO.extend(list(G.neighbors(each)))
    S = nx.Graph()
    S.add_nodes_from(O)
    S.add_nodes_from(NO)
    for each in G.edges:
        u, v = each 
        if (u in O and v in NO) or (u in NO and v in O):
            S.add_edge(u, v)
    M2 = nx.max_weight_matching(S, maxcardinality=True)
    I0 = O 
    G_aux = nx.Graph()
    for each in M2:
        u, v = each 
        G_aux.add_edge(u, v)
        try:
            I0.remove(u)
        except:
            pass 
        try:
            I0.remove(v)
        except:
            pass 
    Iprev = I0 
    # check = G.subgraph(Iprev)
    # drawGraph(check)
    while True:
        Hprev = []
        for each in Iprev:
            Hprev.extend(list(G.neighbors(each)))
        Hprev = list(set(Hprev))
        I_ = []
        for each in Hprev:
            if G_aux.has_node(each):
                I_.extend(list(G_aux.neighbors(each)))
        Inext = list(set(Iprev).union(set(I_)))
        if len(Iprev) == len(Inext):
            return Hprev, Inext
        else:
            Iprev = Inext

if __name__ == "__main__":
    for i in range(10000):
        G = generateRandomGraph(15, 0.1)
        H, I = crownDecomposition(G)
        if len(list(set(H).intersection(set(I)))) != 0:
            print("Test Case Failed!")
