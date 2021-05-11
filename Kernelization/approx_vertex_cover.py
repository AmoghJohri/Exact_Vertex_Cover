import random
import networkx  as nx 
from   util      import generateRandomGraph 
from   util      import drawCustomGraph
from   branching import branching

def approxVertexCover(G):
    # 2-approximate algorithm for obtaining the vertex cover
    G            = G.copy()
    vertex_cover = []
    while list(G.edges):
        node1, node2 = tuple(G.edges)[0]
        vertex_cover.append(node1)
        vertex_cover.append(node2)
        G.remove_node(node1)
        G.remove_node(node2)
    return [vertex_cover]

if __name__ == "__main__":
    for i in range(1000):
        G             = generateRandomGraph(10, 0.1)
        cover         = approxVertexCover(G)[0]
        optimum_cover = branching(G)[0]
        if 2*len(optimum_cover) < len(cover) or len(cover) < len(optimum_cover):
            print("Something went wrong!")
            print("Cover: ", cover)
            print("Optimum Cover: ", optimum_cover)
            drawCustomGraph(G, cover=cover)
    