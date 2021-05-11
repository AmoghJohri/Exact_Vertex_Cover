import networkx    as nx 
from   util        import drawGraph
from   util        import getCustomGraph
from   util        import drawCustomGraph
from   util        import generateRandomGraph

def crownDecomposition(G):
    M1 = nx.maximal_matching(G) # get a maximual matching of G
    O  = list(G.nodes) # Get all nodes of the graph
    # keep only the nodes that are not the part of matching N1
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
    NO = [] # array to store all the neighbors of O
    # get all neighbors for all the nodes in O
    for each in O:
        NO.extend(list(G.neighbors(each)))
    # buid the auxillary graphs with only the edges from O and NO (and the corresponding nodes)
    S = nx.Graph()
    for each in G.edges:
        u, v = each 
        if (u in O and v in NO) or (u in NO and v in O):
            S.add_edge(u, v)
    M2    = nx.max_weight_matching(S, maxcardinality=True) # find a maximum auxillary matching  
    I0    = O # to store set of vertices in O that are unmatched by M2
    G_aux = nx.Graph()
    # get all the vertices that are unmatched by M2
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
    # iterative step
    Iprev = I0 
    # repeat till I(n-1) == I(n)
    while True:
        Hprev = []
        # include all the neighbors of I(n) in H(n)
        for each in Iprev:
            Hprev.extend(list(G.neighbors(each)))
        Hprev = list(set(Hprev))
        I_    = []
        # I(n+1) contains the union of I(n) and H(n)'s neighbors under M2
        for each in Hprev:
            if G_aux.has_node(each):
                I_.extend(list(G_aux.neighbors(each)))
        Inext = list(set(Iprev).union(set(I_)))
        # if I(n-1) == I(n), return the crown decomposition
        if len(Iprev) == len(Inext):
            return Hprev, Inext
        else:
            Iprev = Inext

if __name__ == "__main__":
    for i in range(10000):
        G    = generateRandomGraph(15, 0.1)
        H, I = crownDecomposition(G)
        if len(list(set(H).intersection(set(I)))) != 0:
            print("Test Case Failed!")
