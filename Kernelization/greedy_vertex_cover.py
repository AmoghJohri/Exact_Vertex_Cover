import math
import random
import networkx   as nx 
from   util       import generateRandomGraph 
from   util       import drawCustomGraph
from   branching  import get_max_degree_vertex
from   branching  import branching

def greedyVertexCover(G):
    G            = G.copy()
    vertex_cover = []
    while list(G.edges):
        node = get_max_degree_vertex(G)
        vertex_cover.append(node)
        G.remove_node(node)
    return [vertex_cover]

if __name__ == "__main__":
    for i in range(1000):
        G             = generateRandomGraph(25, 0.1)
        cover         = greedyVertexCover(G)[0]
        optimum_cover = branching(G)[0]
        if len(optimum_cover)*math.log(len(optimum_cover)) + 2 < len(cover) or len(cover) < len(optimum_cover):
            print("Something went wrong!")
            print("Cover: ", cover)
            print("Optimum Cover: ", optimum_cover)
            drawCustomGraph(G, cover=cover)
    