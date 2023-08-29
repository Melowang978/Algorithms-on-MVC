import networkx as nx
import time


def LS1(graph, cutoff_time, seed):
    """
    `LS1` is a local search algorithm implementing hill climbing method for the
    minimum vertex cover problem. This algorithm takes in the graph, cutoff_time,
    and seed as input and outputs a small set of vertices that cover the edges,
    and a trace file documenting the running time and result quality.

    This algorithm starts with the full set of vertices excluding the seed. At
    each iteration, the algorithm evaluates the weight of each vertex in the
    candidate solution. The weight is defined as the number of adjacent vertices
    not included in the candidate solution. A vertex with zero weight is popped
    from the candidate solution at each iteration. The iterative process
    continues until the minimum weight in the candidates solution is no longer
    zero.

    The algorithm includes a build-in deterministic seed randomization, which
    generates initial seeds to be excluded from the vertex set based on the
    input seed. The total number of seeds is set to be around 1% of the vertex
    number in the graph. The algorithm outputs the smallest vertex cover
    obtained from the searches.
    """
    G = graph
    # Initial Setup
    ratio = 100
    v = list(G.nodes())
    k = (len(G.nodes()) + ratio - 1) // ratio
    v_shift = v[seed - 1:] + v[:seed - 1]
    vertex_set = v
    trace = []
    # Iterative Process - Loop each seed
    start_time = time.time()
    for i in range(0, k):
        candidate, weight = sol_init(G, v_shift[i * ratio])
        # Iterative Process - Hill Climbing
        while time.time() - start_time < cutoff_time and 0 in weight:
            idx = weight.index(0)
            v = candidate[idx]
            candidate.remove(v)
            weight.pop(idx)
            for j in G.adj[v]:
                if j in candidate:
                    idx2 = candidate.index(j)
                    weight[idx2] += 1
            new_cost = len(candidate)
            trace.append(str(time.time() - start_time) + ',' + str(new_cost))
        if len(candidate) < len(vertex_set):
            vertex_set = candidate
    return set(vertex_set), trace


def sol_init(gr, seed):
    s = list(set(gr.nodes())-{seed})
    w = [0]*len(s)
    for ii in list(gr.adj[seed]):
        w[s.index(ii)] += 1
    return s, w
