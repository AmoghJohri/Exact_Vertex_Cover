import time
import random
import statistics
import networkx   as nx
from   util       import generateRandomGraph 
from   util       import drawCustomGraph
from   branching  import branching

def getParent(G):
    G = G.copy()
    P = []
    while list(G.edges):
        node = list(G.nodes)[random.randint(0, len(list(G.nodes))-1)]
        if G.degree(node):
            P.append(node)
            G.remove_node(node)
    return P

def fitness_score(G, cover, vertex_penalty = 1, edge_penalty = 2):
    uncovered_edges   = len(list(G.edges)) - len(list(G.edges(cover)))
    required_vertices = len(cover)
    return -1*(vertex_penalty*required_vertices + edge_penalty*uncovered_edges)

def tournament(G, covers):
    score     = [fitness_score(G, each) for each in covers]
    max_score = max(score)
    return covers[score.index(max_score)]

def crossover(G, cover1, cover2):
    nodes1             = set(cover1)
    nodes2             = set(cover2)
    diff1              = list(nodes1.difference(nodes2))
    diff2              = list(nodes2.difference(nodes1))
    remove_from_cover1 = random.sample(diff1, len(diff1))
    remove_from_cover2 = random.sample(diff2, len(diff2))
    for each in remove_from_cover1:
        cover1.remove(each)
        cover2.append(each)
    for each in remove_from_cover2:
        cover2.remove(each)
        cover1.append(each)
    if random.randint(0, 1):
        return cover1 
    else:
        return cover2

def mutate(G, cover, mutation_percent = 10):
    mutation_vertices = int(len(cover)*mutation_percent/100)
    nodes_to_add      = list(set(list(G.nodes)).difference(set(cover)))
    nodes_to_remove   = random.sample(cover, mutation_vertices)
    for each in nodes_to_remove:
        cover.remove(each)
        node = random.choice(nodes_to_add)
        cover.append(node)
        nodes_to_add.remove(node)
    return cover

def geneticAlgorithm(G, first_gen_solutions = 16, window = 4, max_iterations = 5):
    G         = G.copy()
    solutions = [getParent(G) for i in range(first_gen_solutions)]
    for i in range(max_iterations):
        new_generation = []
        for j in range(int(len(solutions)/2)):
            new_generation.append(tournament(G, random.sample(solutions, window)))
        for j in range(0, int(len(solutions)/2), 2):
            cover1 = new_generation[j]
            cover2 = new_generation[j+1]
            new_generation.append(crossover(G, cover1, cover2))
        mutated = []
        for j in range(int(len(solutions)/4)):
            mutated.append(mutate(G, random.choice(new_generation)))
        new_generation.extend(mutated)
        solutions = new_generation
    return [tournament(G, solutions)]

def heuristicVertexCover(G, max_iterations = 5):
    G  = G.copy()
    P1 = getParent(G)
    P2 = getParent(G)
    for i in range(max_iterations):
        G_preserve   = G.copy()
        vertex_cover = []
        VT           = {}
        for node in P1:
            try:
                VT[node] += 1
            except:
                VT[node] = 1
        for node in P2:
            try:
                VT[node] += 1
            except:
                VT[node] = 1
        while list(G.edges):
            tag = 0
            for key in list(VT.keys()):
                if tag == 0:
                    node  = (key, G.degree(key), VT[key])
                else:
                    if node[1] < G.degree(key):
                        node = (key, G.degree(key), VT[key])
                    elif node[1] == G.degree(key) and node[2] < VT[key]:
                        node = (key, G.degree(key), VT[key])
                    else:
                        continue 
            vertex_cover.append(node[0])
            G.remove_node(node[0])
            del VT[node[0]]
        if i%2 == 1:
            P1 = vertex_cover
        else:
            P2 = vertex_cover
        G = G_preserve 
    return [vertex_cover]

if __name__ == "__main__":
    test_cases = 100
    n          = 40
    p          = 0.02
    count      = 0
    size_diff  = []
    time_bb    = []
    time_ga    = []
    for i in range(test_cases):
        G = generateRandomGraph(n, p)
        start    = time.time()
        cover    = geneticAlgorithm(G)[0]
        duration = time.time() - start 
        time_ga.append(duration)
        start         = time.time()
        optimum_cover = branching(G)[0]
        duration      = time.time() - start 
        time_bb.append(duration)
        if len(cover) > len(optimum_cover):
            # print("Something went wrong!")
            # print("Cover: ", cover)
            # print("Optimum Cover: ", optimum_cover)
            # drawCustomGraph(G, cover=cover)
            count += 1
        if len(optimum_cover):
            size_diff.append(len(cover)/len(optimum_cover))
    print(statistics.mean(size_diff))
    print("Time taken for bb: ", statistics.mean(time_bb))
    print("Time taken for ga: ", statistics.mean(time_ga))