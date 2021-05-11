import progressbar
import networkx            as nx 
from   util                import test
from   util                import drawGraph
from   util                import getCustomGraph
from   util                import drawCustomGraph
from   util                import generateRandomGraph
from   flow                import reduction_rule_6_helper
from   crown_decomposition import crownDecomposition
from   brute_force         import brute_force
from   branching           import branching

pivot = 10000000

def reduction_rule_1(G):
    """ remove isolated vertices """
    nodes = list(G.nodes)
    for each in nodes:
        if G.degree(each) == 0:
            G.remove_node(each)

def reduction_rule_2(G, k, vertex_cover):
    """ remove vertices with degree greater than k """
    nodes = list(G.nodes)
    i     = 0
    while i < len(nodes):
        node = nodes[i]
        if G.degree(node) > k:
            vertex_cover.append(node)
            G.remove_node(node)
            nodes.remove(node)
            k = k - 1
            if k < 0:
                return k
            i = 0
        else:
            i = i + 1
    return k

def reduction_rule_3(G, k, vertex_cover):
    """ remove pendant vertices' neighbor """
    nodes = list(G.nodes)
    i     = 0
    while i < len(nodes):
        node = nodes[i]
        if G.degree(node) == 1:
            node_to_delete = list(G.neighbors(node))[0]
            vertex_cover.append(node_to_delete)
            G.remove_node(node)
            G.remove_node(node_to_delete)
            nodes.remove(node)
            nodes.remove(node_to_delete)
            k = k - 1
            if k < 0:
                return k 
            i = 0 
        else:
            i = i + 1
    return k

def reduction_rule_4(G, k, vertex_cover):
    """ include adjacent neighbors for vertex of degree 2 """
    nodes = list(G.nodes)
    i     = 0
    while i < len(nodes):
        node = nodes[i]
        if G.degree(node) == 2:
            node1, node2 = tuple(G.neighbors(node))
            if G.has_edge(node1, node2):
                vertex_cover.append(node1)
                vertex_cover.append(node2)
                G.remove_node(node1)
                G.remove_node(node2)
                nodes.remove(node1)
                nodes.remove(node2)
                k = k - 2
                if k < 0:
                    return k 
                i = 0 
            else:
                i = i + 1
        else:
            i = i + 1
    return k

def reduction_rule_5(G, k, vertex_cover, folded_vertices):
    """ Vertex Folding """
    nodes = list(G.nodes)
    i     = 0
    while i < len(nodes):
        node = nodes[i]
        if G.degree(node) == 2:
            node1, node2 = tuple(G.neighbors(node))
            if G.degree(node1) == 1 and G.degree(node2) == 1:
                G.remove_node(node1)
                G.remove_node(node2)
                G.remove_node(node)
                nodes.remove(node1)
                nodes.remove(node2)
                nodes.remove(node)
                vertex_cover.append(node)
                k = k - 1
                if k < 0:
                    return k 
                i = 0 
            elif not G.has_edge(node1, node2):
                neighbors = list(G.neighbors(node1))
                neighbors.extend(list(G.neighbors(node2)))
                neighbors = list(set(neighbors))
                G.remove_node(node1)
                G.remove_node(node2)
                G.remove_node(node)
                nodes.remove(node1)
                nodes.remove(node2)
                nodes.remove(node)
                nodes.append(node+pivot)
                G.add_node(node+pivot)
                for each in neighbors:
                    if node != each:
                        G.add_edge(node+pivot, each)
                folded_vertices.append((node+pivot, node1, node2))
                k = k - 1
                if k < 0:
                    return k 
                i = 0 
            else:
                i = i + 1
        else:
            i = i + 1
    return k

def reduction_rule_6(G, k, vertex_cover):
    """ Network Flow """
    cover = reduction_rule_6_helper(G)
    if max(cover) < 0:
        for each in list(G.nodes):
            G.nodes[each]['weight'] = 0.5
    else:
        for each in list(G.nodes):
            G.nodes[each]['weight'] = 0
        for each in cover:
            G.nodes[abs(each)-1]['weight'] += 0.5
    x     = 0
    nodes = list(G.nodes)
    for each in nodes:
        if G.nodes[each]['weight'] == 1:
            vertex_cover.append(each)
            x += 1
        if G.nodes[each]['weight'] != 0.5:
            G.remove_node(each)
    return k - x

def reduction_rule_7(G, k, vertex_cover):
    """ Crown Decomposition """
    reduction_rule_1(G)
    H, I = crownDecomposition(G)
    x    = 0
    for each in H:
        G.remove_node(each)
        vertex_cover.append(each)
        x += 1
    for each in I:
        G.remove_node(each)
    return k - x

def kernelization(G, k, vertex_cover, folded_vertices, reduction_rules = [1, 2, 3, 4, 5, 6, 7]):
    """ Apply all the reduction rules """
    _k = k
    while True:
        if 1 in reduction_rules:
            reduction_rule_1(G)
        if 2 in reduction_rules:
            _k = reduction_rule_2(G, k, vertex_cover)
            if _k < 0:
                return None
        if 3 in reduction_rules:
            _k = reduction_rule_3(G, _k, vertex_cover)
            if _k < 0:
                return None
        if 4 in reduction_rules:
            _k = reduction_rule_4(G, _k, vertex_cover)
            if _k < 0:
                return None
        if 5 in reduction_rules:
            _k = reduction_rule_5(G, _k, vertex_cover, folded_vertices)
            if _k < 0:
                return None
        if 6 in reduction_rules:
            if len(list(G.edges)) > 0:
                _k = reduction_rule_6(G, _k, vertex_cover)
            if _k < 0:
                return None
        if 7 in reduction_rules:
            _k = reduction_rule_7(G, _k, vertex_cover)
            if _k < 0:
                return None
        if _k < 0:
            return None
        elif _k == k:
            return _k
        else:
            k = _k

def get_vertex_cover(G, k, f, reduction_rules  = [1, 2, 3, 4, 5, 6, 7]):
    """ Get the vertex cover """
    G = G.copy()
    def unfold(cover, folded_vertices):
        i = 0
        while i < len(folded_vertices):
            node, node1, node2 = folded_vertices[-(i+1)]
            if node in cover:
                cover.remove(node)
                cover.append(node1)
                cover.append(node2)
            else:
                _node = str(node)
                if len(_node) == 1:
                    cover.append(int(_node[-1]))
                elif int(_node[0]) > 1:
                    cover.append(node - pivot)
                else:
                    cover.append(int(_node[-(len(_node)-1):]))
            i = i + 1
    vertex_cover    = []
    folded_vertices = []
    k               = kernelization(G, k, vertex_cover, folded_vertices, reduction_rules=reduction_rules)
    if k == None:
        # print("NO INSTANCE (after reduction rules)")
        return 
    else:
        vertex_covers = f(G)
        if vertex_covers == None:
            # print("NO INSTANCE (after brute-force)")
            return 
        else:
            covers = []
            for i in range(len(vertex_covers)):
                covers.append(vertex_covers[i])
                covers[-1].extend(vertex_cover)
                unfold(covers[-1], folded_vertices)
            return covers

def customTest():
    """ Generate a custom graph to test the algorithms """
    G      = getCustomGraph()
    G_copy = G.copy()
    cover  = reduction_rule_6_helper(G)
    exit(0)

if __name__ == "__main__":
    # customTest()
    number_of_tests = 50
    bar             = progressbar.ProgressBar(maxval=number_of_tests, \
    widgets         = [progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
    print("Beginning Analysis...")
    bar.start()
    for i in range(number_of_tests):
        G      = generateRandomGraph(30, 0.1)
        G_copy = G.copy()
        k      = len(list(G.nodes))
        # drawCustomGraph(G)
        vertex_covers = get_vertex_cover(G, k, branching, reduction_rules = [1, 2, 3, 4, 5, 6, 7])
        if vertex_covers:
            for each in vertex_covers:
                test(G_copy.copy(), each)
        else:
            vertex_covers = brute_force(G_copy, k)
            if vertex_covers:
                print("Test-case failed!")
                # drawCustomGraph(G_copy, cover=each)
        bar.update(i+1)
    bar.finish()
    print("Analysis Completed!")
