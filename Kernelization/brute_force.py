import networkx as nx 
import progressbar
import itertools

def brute_force(G, k=-1, one_cover=True):
    if k == -1:
        k = len(list(G.nodes))
    vertex_covers = []
    vertices      = list(G.nodes)
    bar = progressbar.ProgressBar(maxval=k+1, \
    widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
    bar.start()
    for i in range(k + 1):
        bar.update(i+1)
        _vertices = list(itertools.combinations(vertices, i))
        for each in _vertices:
            covered = []
            for v in each:
                for edge in G.edges(v):
                    covered.append((min(edge), max(edge)))
            covered = list(set(covered))
            if len(covered) == len(G.edges):
                vertex_covers.append(list(each))
                if one_cover:
                    bar.finish()
                    return vertex_covers
        if len(vertex_covers) > 0:
            bar.finish()
            return vertex_covers
    bar.finish()