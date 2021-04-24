import networkx as nx 
import kernelization
from   test     import get_graph 

if __name__ == "__main__":
    G = get_graph(code=93)
    print("Beginning with graph:")
    print("\t |V|: ", len(G.nodes))
    print("\t |E|: ", len(G.edges))
    for k in range(20, 30):
        print("k: ", k)
        vertex_covers = kernelization.get_vertex_cover(G, k, reduction_rules = [1, 2, 3, 4, 5, 6, 7])