import time 
import networkx    as nx 
from   util        import test
from   util        import generateRandomGraph
from   util        import drawGraph
from   util        import drawCustomGraph
from   brute_force import brute_force

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
    # stack based DFS to perform branching
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
        eState        = stack.pop(-1) # current statae
        G             = eState.G # get the current graph
        removed_edges = eState.removed_edges # get the edges that had been removed in the last step
        vertex_cover  = eState.vertex_cover # get the current vertex cover
        # if we have a vertex cover
        if not list(G.edges):
            # if the vertex cover is smaller than the current best, then make it the current best
            if len(vertex_cover) < current_best[0]:
                current_best = (len(vertex_cover), tuple(vertex_cover))
        else:
            G_copy          = G.copy() # get a copy of G
            max_degree_node = get_max_degree_vertex(G) # get the max. degree node
            removed_edges   = list(G.edges(max_degree_node)) # get the list of edges from the max. degree node (these shall be removed)
            vertex_cover.append(max_degree_node) # append the max. degree node in the vertex cover
            G.remove_edges_from(removed_edges) # remove all the edges (all neighbors from the max. degree node)
            remove_isolated_vertices(G) # remove all isolated vertices (it messes up the implementation if there are any of these present)
            stack.append(ExecutionState(G, removed_edges, vertex_cover)) # append this state to the stack
            neighbors       = list(G_copy.neighbors(max_degree_node)) # get the neighbors of the max. degree node
            if len(vertex_cover) + len(neighbors) - 1 < current_best[0]: # if we can afford to remove all the neighbors, and be better than current best, we procede
                vertex_cover_   = list(vertex_cover) 
                vertex_cover_.remove(max_degree_node) # remove the max. degree node from the cover
                vertex_cover_.extend(neighbors) # add all its neighbors in the vertex cover instead
                removed_edges_  = []
                # remove all the edges stemming from the neighbors of the max. degree node
                for each in neighbors:
                    removed_edges_.extend(G_copy.edges(each))
                G_copy.remove_edges_from(removed_edges_) # get the new graph by removing these edges
                remove_isolated_vertices(G_copy) # remove all isolated nodes
                stack.append(ExecutionState(G_copy, removed_edges_, vertex_cover_)) # add this state to the stack
    return [list(current_best[1])] # when the stack is empty, we return the best vertex cover found

if __name__ == "__main__":
    n     = 10
    check = 1
    draw  = 1
    for i in range(10):
        G        = generateRandomGraph(n, 0.1)
        start    = time.time()
        cover1   = branching(G)[0]
        duration = time.time() - start
        if check:
            cover2 = brute_force(G)[0]
            if len(cover1) != len(cover2):
                print("Something Went Wrong")
                print("Branching: ", cover1)
                print("Brute-Force: ", cover2)
        if draw:
            drawCustomGraph(G, cover=cover1)
        test(G, cover1)
        print("Time taken for " + str(n) + " nodes: " + str(duration) + " seconds!")