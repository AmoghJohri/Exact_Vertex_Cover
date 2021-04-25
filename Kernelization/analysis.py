import time 
import progressbar
import networkx          as nx 
import matplotlib.pyplot as plt 
from   kernelization import get_vertex_cover
from   branching     import run_bnb
from   brute_force   import brute_force
from   util          import generateRandomGraph
from   test          import get_graph 

if __name__ == "__main__":
    number_of_testcases = 50
    p = .05
    min_nodes = 0
    max_nodes = 30
    list_of_kernels = [1, 3, 4, 5, 7]
    time_crown_reduction = [0 for i in range((max_nodes - min_nodes) + 1)]
    time_branch_and_bound = [0 for i in range((max_nodes - min_nodes) + 1)]
    bar = progressbar.ProgressBar(maxval=((max_nodes - min_nodes) + 1)*number_of_testcases, \
    widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
    print("Beginning Analysis...")
    bar.start()
    for i in range(min_nodes, max_nodes+1):
        for j in range(number_of_testcases):
            G = generateRandomGraph(i, p)
            start = time.time()
            get_vertex_cover(G, i, run_bnb, reduction_rules = [])
            duration = time.time() - start 
            time_branch_and_bound[i-min_nodes] += duration 
            start = time.time()
            get_vertex_cover(G, i, run_bnb, reduction_rules = list_of_kernels)
            duration = time.time() - start 
            time_crown_reduction[i-min_nodes] += duration
            bar.update((i-min_nodes)*j + 1)
        time_branch_and_bound[i-min_nodes] /= number_of_testcases
        time_crown_reduction[i-min_nodes] /= number_of_testcases
    bar.finish()
    print("Analysis Completed!")
    nodes = [i for i in range(min_nodes, max_nodes + 1)]
    plt.plot(nodes, time_crown_reduction)
    plt.plot(nodes, time_branch_and_bound)
    plt.ylabel("Time (s)")
    plt.xlabel("Nodes")
    plt.title("Time vs Nodes - " + str(list_of_kernels) + " - Method: Branch and Bound \nEdge Proability: " + str(p))
    plt.legend(['Kernel', 'Without Kernel'])
    plt.grid()
    plt.show()