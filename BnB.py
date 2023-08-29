import time
import copy
import sys
sys.setrecursionlimit(25000)

trace_history = []
star_time = time.time()


def multi_copy(data):
    """
    `multi_copy` is a sub_function that create a list of copy based on the given 
    data. 
    """
    new_data = []
    for i in data:
        new_data.append(copy.copy(i))
    return new_data


def BnB(graph, timelim, seed):
    """
    `BnB` is a function implenting branch and bound algorithm computing the exact 
    optimal solution based on the lower bound and the global optimal solution. 
    
    `BnB` takes the input of network graph and generate the root data of the graph.
    Root data inlcuding initial vertex cover, which is the size of initial nodes.
    It create covered nodes, uncovered nodes,  and best nodes as blank 
    list for future storing. The function stops when the subresult do not have more 
    unselected nodes.
    """

    global star_time
    global trace_history
    star_time = time.time()
    minimum = len(graph.nodes)  # minimum cover size, initialize as |V|
    covered_nodes, uncovered_nodes, best_nodes = [], [], []  # stores covered nodes
    free_nodes = list(graph.nodes)  # stores free nodes, initialize as all nodes
    uncovered_edges = list(graph.edges)
    distance = [0 for _ in range(max(list(graph.nodes)))]
    for j in free_nodes:
        distance[j - 1] = len(graph.adj[j])
    min_uncovered, best_uncovered = search(graph, minimum, covered_nodes, uncovered_nodes, free_nodes, best_nodes,
                                           uncovered_edges, distance, timelim)
    if len(best_uncovered) == 0:
        return set(list(graph.nodes)), trace_history
    else:
        return set(best_uncovered), trace_history


def search(graph, minimum, covered_nodes, uncovered_nodes, free_nodes, best_nodes, uncovered_edges, distance, timelim):
    """
    `search` is a sub-function implenting branch and bound algorithm.
    
    `search` takes the input of current sub network graph and creating local
    lower bound value and compare with the current best solution. Current
    graph data includes the subgraph, sub-minimum vertex cover, sub-uncovered nodes
    ...ect as we stated in BnB function. The function will first copy current graph 
    by multi-copy function and generate the lower bound = |C'| + |G'|. We would compare
    the computed lb with the current optimal solution if we reach to the optimal. Unless,
    the function will keep iterating untill we used out of time or we do not have unselected
    nodes or edges. 
    
    The recursion will be on two branches: 1. The next node is covered on the future brand or
    2. The next node is not covered.
    
    """

    time_consuming = time.time() - star_time
    V, E_sub = len(covered_nodes) + 1, len(uncovered_edges)
    
    descending_free = [distance[val - 1] for index, val in enumerate(free_nodes)]
    # sort free nodes based on decending free list
    sorted_free_nodes = [free_node for _, free_node in sorted(zip(descending_free, free_nodes), reverse=True)]
    sum = 0  # Initiallize sum
    # From the description we have lb = |C'| + |G'|
    lower_bound = len(covered_nodes) + len(free_nodes)
    if len(covered_nodes) - minimum >= 0 or len(free_nodes) == 0 or time_consuming - timelim >= 0:
        return minimum, best_nodes
    elif len(uncovered_edges) == 0:  # No unchoosen edge left
        if len(covered_nodes) - minimum < 0:
            best_nodes = copy.copy(covered_nodes)  # new solution becomes best solution
            # global LB becomes length of new solution
            trace_history.append(f'{time_consuming},{len(best_nodes)}')
        return minimum, best_nodes
    
    # updates lb and compare it with the current optimal solution
    for index, val in enumerate(sorted_free_nodes):
        sum += distance[val - 1]
        if sum - E_sub >= 0:
            lower_bound = V + index
            break
    if abs(lower_bound) - abs(minimum) >= 0:
        return minimum, best_nodes
    
    free_temp, covered_temp, uncovered_temp, descending_temp, uncovered_edges_temp = multi_copy(
    [free_nodes, covered_nodes, uncovered_nodes, distance, uncovered_edges])

    # Generate sub graph
    next_node = sorted_free_nodes[0]
    temp_graph = list(graph.adj[next_node])

    for index, j in enumerate(temp_graph):
        descending_temp[j - 1] -= 1
        if (j, next_node) in uncovered_edges_temp:
            uncovered_edges_temp.remove((j, next_node))
        if (next_node, j) in uncovered_edges_temp:
            uncovered_edges_temp.remove((next_node, j))
    uncovered_temp.append(next_node)
    free_temp.remove(next_node)
    covered_temp.append(next_node)
    # Branch 1: the node is covered
    min_covered, best_covered = search(graph, minimum, covered_temp, uncovered_nodes, free_temp, best_nodes,
                                       uncovered_edges_temp, descending_temp, timelim)
    # Branch 2: the node is not covered
    min_uncovered, best_uncovered = search(graph, min_covered, covered_nodes, uncovered_temp, free_temp, best_covered,
                                           uncovered_edges, distance, timelim)
    return min_uncovered, best_uncovered
