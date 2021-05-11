import itertools
import progressbar
import networkx as nx 

def brute_force(G, k=-1, one_cover=True):
    G = G.copy() # get a copy of G
    # get kernel size
    if k == -1:
        k = len(list(G.nodes))
    vertex_covers = []
    vertices      = list(G.nodes)
    # bar = progressbar.ProgressBar(maxval=k+1, \
    # widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
    # bar.start()
    # get all possible combination of vertices ranging from a size of 0 to k + 1
    for i in range(k + 1):
        # bar.update(i+1)
        _vertices = list(itertools.combinations(vertices, i)) # get all possible combination of vertices of size i
        # for each vertex we add the edges in it to the set covered
        for each in _vertices:
            covered = []
            for v in each:
                for edge in G.edges(v):
                    covered.append((min(edge), max(edge)))
            covered = list(set(covered))
            # if the set covered is equal in size to the set of total edges, we have the vertex cover
            if len(covered) == len(G.edges):
                vertex_covers.append(list(each))
                # if we only need one minimum cover
                if one_cover:
                    # bar.finish()
                    return vertex_covers
        if len(vertex_covers) > 0:
            # bar.finish()
            return vertex_covers
    # bar.finish()