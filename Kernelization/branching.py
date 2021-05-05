import networkx as nx 
from brute_force import brute_force
from util import test
from util import generateRandomGraph
from util import drawGraph
from util import drawCustomGraph

class ExecutionState:
    def __init__(self, G, removed_edges = [], vertex_cover = []):
        self.G              = G 
        self.removed_edges  = removed_edges
        self.vertex_cover   = vertex_cover

def get_max_degree_vertex(G):
    nodes = list(G.nodes)
    if nodes:
        max_degree_node = nodes[0]
        for each in nodes:
            if G.degree(max_degree_node) < G.degree(each):
                max_degree_node = each 
        return max_degree_node
    return None

def remove_isolated_vertices(G):
    for each in list(G.nodes):
        if G.degree(each) == 0:
            G.remove_node(each)

def branching(G):
    G               = G.copy()
    G_copy          = G.copy()
    current_best    = (len(list(G.nodes)), tuple(list(G.nodes)))
    if current_best[0] == 0:
        return [list(current_best[1])]
    stack           = []
    max_degree_node = get_max_degree_vertex(G) # get the maximum degree vertex
    removed_edges   = list(G.edges(max_degree_node)) # list of all the edges adjacent to the maximum degree vertex
    vertex_cover    = [max_degree_node] # add the maximum degree vertex in the vertex-cover
    G.remove_edges_from(removed_edges) # remove all edges adjacent to the maximum degree vertex
    # remove all isolated vertices
    remove_isolated_vertices(G)
    stack.append(ExecutionState(G, removed_edges, vertex_cover)) # append this state to stack
    neighbors       = list(G_copy.neighbors(max_degree_node)) # get all neighbors of the maximum degree vertex
    vertex_cover_   = list(neighbors) # the vertex cover has all the neighbors of the vertex
    removed_edges_  = [] 
    # list of all the edges adjacent to the neighbors of the maximum degree vertex
    for each in neighbors:
        removed_edges_.extend(G_copy.edges(each))
    G_copy.remove_edges_from(removed_edges_) # removing the equired edges
    # removing all isolated vertices
    remove_isolated_vertices(G_copy)
    stack.append(ExecutionState(G_copy, removed_edges_, vertex_cover_)) # append this state to stack
    # while stack is non-empty
    while stack:
        eState        = stack.pop(-1)
        G             = eState.G 
        removed_edges = eState.removed_edges
        vertex_cover  = eState.vertex_cover
        if not list(G.edges):
            if len(vertex_cover) < current_best[0]:
                current_best = (len(vertex_cover), tuple(vertex_cover))
        else:
            G_copy = G.copy()
            max_degree_node = get_max_degree_vertex(G)
            removed_edges   = list(G.edges(max_degree_node))
            vertex_cover.append(max_degree_node)
            G.remove_edges_from(removed_edges)
            remove_isolated_vertices(G)
            stack.append(ExecutionState(G, removed_edges, vertex_cover))
            neighbors       = list(G_copy.neighbors(max_degree_node))
            if len(vertex_cover) + len(neighbors) - 1 < current_best[0]:
                vertex_cover_   = list(vertex_cover)
                vertex_cover_.remove(max_degree_node)
                vertex_cover_.extend(neighbors)
                removed_edges_  = []
                for each in neighbors:
                    removed_edges_.extend(G_copy.edges(each))
                G_copy.remove_edges_from(removed_edges_)
                remove_isolated_vertices(G_copy)
                stack.append(ExecutionState(G_copy, removed_edges_, vertex_cover_))
    return [list(current_best[1])]

if __name__ == "__main__":
    G = nx.Graph()
    G.add_node(1)
    check = 0
    for i in range(100):
        G = generateRandomGraph(30, 0.1)
        cover1 = branching(G)[0]
        if check:
            cover2 = brute_force(G)[0]
            if len(cover1) != len(cover2):
                print("Something Went Wrong")
                print("Branching: ", cover1)
                print("Brute-Force: ", cover2)
        test(G, cover1)