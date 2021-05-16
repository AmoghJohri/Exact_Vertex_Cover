# Exact and Parameterized Algorithms Project - Exact Vertex Cover

## Implementation 
* Brute-force for exact vertex-cover
* Brute-force for parameterized vertex-cover
* Branching algorithm for exact vertex-cover
* 7 Reduction Rules
  * Isolated Vertex Removal
  * Pendant Vertex Removal
  * High-degree Vertex Removal
  * Degree-2 Vertex's Neighbor Inclusion
  * Vertex Folding
  * Network Flow Based Reduction
  * Crown Decomposition Based Reduction
* 2-Approximate Algorithm for Approximate vertex-cover
* Greedy Algorithm for Approximate vertex-cover
* Genetic Algorithms for Approximate vertex-cover

## Observation and Conclusion
1. Brute force is way too slow, even for the purpose of bare-minimum analysis (it takes an unusually long time to deal with graphs with mere 20 nodes or so)
2. The efficiency of reduction rules (apart from high-degree vertex removal) decreases as the probability of edge increases.
This makes sense as if we analyze the entire PACE dataset (2019), we get the following:
* Min   :  2.381614667858874e-05
* Max   :  0.17610864197530865
* Mean  :  0.01887090304564615
* Median:  0.00023000940504558766 <br> suggesting that the average probability of an edge for most real examples is rather small.
3. Based on the results, to find exact vertex cover, it is a good ideas to preprocess using the following reduction rules (in all scenarios):
   1. Isolated vertex removal
   2. Pendant vertex removal
   3. Degree-2 Vertex's Neighbor removal
   4. Vertex folding
4. If the edge density for the graph is low (after the 4 reduction rules are applied exhaustively), we should first use crown decomposition based reduction, and then if the edge density is still low, we should use network flow based reduction.
5. Genetic algorithms provide an intersing way to look at the problem, and conceptually relate it to Darwin's theory of evolution. Their performance is also decent (especially considering the crude implementation of the same.)

## Results
1. Brute force is much-much worse than branching (Brute_Force_vs_Branching)
2. Reductions used in isolated provide little benefit when combined with brute-force (for moderately high edge probability), however, they never perform visibly worse than not having them at all (probably because of how bad brute force in itself is.) (Brute_Force_Single_Kernel)
3. Using all the reduction rules together results in a huge reduction in running-time. This efficiency however, goes down with the increase in number of probabiliy of edges. For brute force however, it never becomes visibly worse than the case when no reduction rules are applied(Brute_Force_All_Reduction).
4. The reduction rules 3, 4 and 5 (removal of pendent vertices, inclusion of neighbors of vertices of degree 2 and vertex folding) require a few edges to be useful. Hence, there efficiency increases for a little while as edge probability increases, and then decreases sharply. For all other reduction, it just starts at a maximum and then decreases sharply (Reduction_Rules_vs_Probability).
5. As noted in previous literature, strictly in terms of the percentage of nodes removed (or the size of the resulting kernel), the best reduction rule is the one with network-flow/linear-programming(Reduction_Rules_vs_Probability).
6. With the high-probability of nodes removed, crown decomposition and network flow algorithms are capable of often rendenring a graph edge-free, all by themselves. (Reduction_Rules_vs_Probability). Also, when used together, we the reduction rules remove a much larger percentage of nodes, and the efficiency also plummets at a much slower pace.
7. Network Flow based reduction is the most expensive reduction (by a margin - across edge probabilities). It is followed by crown decomposition, vertex folding, pendant vertex removal, degree-2 vertex removal and isolated vertex removal. Also, run-time of network flow and crown decomposition is not significantly affected by the edge probability, but for the pendant vertex removal, degree-2  vertex removal and vertex folding, it increases a little as edge-probability increases from 0 (as more nodes fall in this category now), and then sharply decreases. Hence, these reduction rules do not "waste" time (that is, if they are not able to decrease the kernel size, their run-time is also low.) (Reduction_Rules_Time_vs_Edge_Probability)
8. Like with brute-force, the efficiency of reduction rules decreases with increase in probability, with branching as well. However, here after a certain probability, it can actually become worse than using only-branching. However, it does not become worse by any significant amount (Branching_All_Kernel). This also holds if we omit network flow (Branching_without_network_flow)
9. All approximate algorithms are significantly faster than branching, even with all the reduction rules used, and low probability. As the probability increases, the branching + reduction rules based algorithms become worse (Exact_vs_approximate_algorithm_time_comparison). 
10. The greedy approximate algorithm gives the best approximation across probabilities, second only to the modified genetic algorithm (however, this is the second costliest approximate algorithm in terms of time complexity.) There does not seem to be any obvious relation between edge probability, number of nodes, and the approximation, however, for very low probability 2-approximation algorithm performs significantly worse than all other. (Approximate_algorithms_comparison)
