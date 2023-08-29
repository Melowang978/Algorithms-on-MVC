import time
import math

def Approx(graph, cutoff_time, seed):
    """
    `Approx` is a approximation algorithm for the minimum vertex cover problem. 

    The  funciton takes in the graph and a cutoff_time as input and provides the 
    minimum numver of vertex required (as per the heuristics) to cover all the 
    edges in the given graph. 

    If the total runtime of the algorithm is more than the provided cutoff time, 
    then we just output + infinity as our result.
    """
    trace = []
    start = time.time() 
    print("Approximation Algorithm: Maximum Degree Greedy (MDG)")
    N = graph.number_of_nodes()
    VC = set()

    #Initial parsing of the graph
    #for i in range(1,N+1): print("node: ", i, "--> ", len(graph.edges([i])))

    # Finding the worst case approximation ratio of this graph: App(n) ~= ln(n) + 0.57
    Delta = 0
    for i in range(1,N+1): Delta =  max(Delta, len(graph.edges([i])))
    Approx_ratio = (math.log(Delta)/math.log(math.e)) + 0.57
    print(Approx_ratio)
    
    # Sort the nodes using the reverse order of degree of nodes 
    deg_list = []
    for i in range(1,N+1):
        deg_list.append((i,graph.degree[i]))
    deg_list.sort(reverse=True, key=lambda x: x[1])
    #print(N,VC,deg_list)

    # Data structure to find out we have got the vertex cover 
    mvc_count = 0
    # Parsing the graph using maximum degree greedy strategy 
    idx = 0
    while (graph.number_of_edges() != 0):
        node = deg_list[idx][0]
        graph.remove_node(node)
        VC.add(idx)
        mvc_count += 1
        idx += 1

    # Final parsing of the graph
    # for i in range(1,N+1): print("node: ", i, "--> ", graph.edges([i]))
    
    # Print the mvc result 
    print("mvc_count is: ", mvc_count)

    end = time.time()
    time_spent = end - start 

    # Sanity checking 
    if (len(VC) != mvc_count):
        print("Length of vertex set != mvc_count. Check your code !!")

    if time_spent <= cutoff_time:
        trace.append(str(time_spent) + ',' + str(mvc_count))
        return( VC, trace)
    else:
        trace.append(str(cutoff_time) + ',' + str(N))
        VC_cutoff = set(graph.nodes)
        return(VC, trace)