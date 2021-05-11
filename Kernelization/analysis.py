import time 
import statistics
import progressbar
import networkx              as nx 
import matplotlib.pyplot     as plt 
from   kernelization         import kernelization
from   kernelization         import get_vertex_cover
from   util                  import generateRandomGraph
from   test                  import get_graph 
from   branching             import branching
from   approx_vertex_cover   import approxVertexCover
from   greedy_vertex_cover   import greedyVertexCover
from   genetic_algorithm     import heuristicVertexCover, geneticAlgorithm

if __name__ == "__main__":
    reduction_rules      = [1, 3, 4, 5, 6, 7] # reduction rules to apply
    min_number_of_nodes  = 5 # minimum nodes in a graph
    max_number_of_nodes  = 50 # maximum nodes in a graph
    min_probability      = 0.001 # minimum edge probability
    max_probability      = 0.05 # maximum edge probability
    number_of_test_cases = 50 # number of test-cases
    maxval_nodes         = (max_number_of_nodes - min_number_of_nodes)*(number_of_test_cases) # maximum iteration value (when expiement is over different number of nodes)
    maxval_probab        = int((max_probability - min_probability)/min_probability)*(number_of_test_cases) # maximum iteration value (when expiement is over different edge probability)
    p                    = .1 # constant edge probability
    offset               = 0 # to remove the starting few results from the plot
    # time taken by different algorithms
    time_array           = []
    time_array_2         = []
    time_array_3         = []
    time_array_4         = []
    time_array_5         = []
    # ratio of nodes removed by different algorithms
    ratio_array_2        = []
    ratio_array_3        = []
    ratio_array_4        = []
    ratio_array_5        = []
    # progress bar
    bar                  = progressbar.ProgressBar(maxval=maxval_nodes, \
    widgets              = [progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
    bar.start()
    # for i in range(1, int(max_probability/min_probability)):
    for i in range(min_number_of_nodes, max_number_of_nodes):
        time_taken   = 0
        time_taken_2 = 0
        time_taken_3 = 0
        time_taken_4 = 0
        time_taken_5 = 0
        ratio_2      = 0
        ratio_3      = 0
        ratio_4      = 0
        ratio_5      = 0
        for j in range(number_of_test_cases):
            # G           = generateRandomGraph(max_number_of_nodes, i*min_probability)
            G             = generateRandomGraph(i, p)
            start         = time.time()
            cover         = get_vertex_cover(G, len(list(G.nodes)), branching, reduction_rules=reduction_rules)[0] # branching with all reduction rules
            duration      = time.time() - start
            time_taken   += duration
            start         = time.time()
            cover_2       = approxVertexCover(G)[0] # 2-approximate algorithm for vertex cover
            duration      = time.time() - start
            time_taken_2 += duration
            start         = time.time()
            cover_3       = greedyVertexCover(G)[0] # greedy vertex cover algorithm
            duration      = time.time() - start
            time_taken_3 += duration
            start         = time.time()
            cover_4       = heuristicVertexCover(G)[0] # heuristic genetic algorithm
            duration      = time.time() - start
            time_taken_4 += duration
            start         = time.time()
            cover_5       = geneticAlgorithm(G)[0] # custom genetic algorithm
            duration      = time.time() - start
            time_taken_5 += duration
            ratio_2      += (len(cover_2)+1)/(len(cover)+1)
            ratio_3      += (len(cover_3)+1)/(len(cover)+1)
            ratio_4      += (len(cover_4)+1)/(len(cover)+1)
            ratio_5      += (len(cover_5)+1)/(len(cover)+1)
            bar.update((i-min_number_of_nodes)*j+1)
        time_array.append(time_taken/number_of_test_cases)
        time_array_2.append(time_taken_2/number_of_test_cases)
        time_array_3.append(time_taken_3/number_of_test_cases)
        time_array_4.append(time_taken_4/number_of_test_cases)
        time_array_5.append(time_taken_5/number_of_test_cases)
        ratio_array_2.append(ratio_2/number_of_test_cases)
        ratio_array_3.append(ratio_3/number_of_test_cases)
        ratio_array_4.append(ratio_4/number_of_test_cases)
        ratio_array_5.append(ratio_5/number_of_test_cases)
    bar.finish()
    # plotting the graphs
    # plt.plot([i for i in range(min_number_of_nodes, max_number_of_nodes)][offset:], time_array[offset:])
    plt.plot([i for i in range(min_number_of_nodes, max_number_of_nodes)][offset:], ratio_array_2[offset:])
    plt.plot([i for i in range(min_number_of_nodes, max_number_of_nodes)][offset:], ratio_array_3[offset:])
    plt.plot([i for i in range(min_number_of_nodes, max_number_of_nodes)][offset:], ratio_array_4[offset:])
    plt.plot([i for i in range(min_number_of_nodes, max_number_of_nodes)][offset:], ratio_array_5[offset:])
    plt.xlabel("Nodes")
    plt.ylabel("Ratio")
    plt.title("Approximate Algorithms: Ratio vs Nodes\np: " + str(p))
    plt.legend(['2-Approximate Algorithm', 'Greedy Approximate', 'Genetic Algorithm - 1', 'Genetic Algorithm - 2'])
    plt.grid()
    plt.show()
    