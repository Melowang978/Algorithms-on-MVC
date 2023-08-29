import numpy as np
import time
import random
import math

def LS2(graph, cutoff_time, seed):
    np.random.seed(seed)
    trace = []
    all_node = set(graph.nodes)
    curr_solution = set(graph.nodes)
    number_of_node = len(all_node)
    T = 50
    alpha = 0.95
    miu = 0
    miu_increase = 0.01/number_of_node
    start_time = time.time()

    count_no_improve_iter = 0
    max_no_improve = max(400,number_of_node)
    best_cost_so_far = number_of_node
    longest_no_improve_iter = 0

    while time.time() - start_time < cutoff_time and longest_no_improve_iter < max_no_improve:
        step = False
        #decide 50-50 whether a node is removed or added
        remove_node = decision(0.5)

        if remove_node: #if a node is to be removed
            rand_node = np.random.choice(list(curr_solution))
            neighbor = curr_solution - {rand_node}
            #if removing node gives invalid VC, move on
            if isValid(neighbor, graph.edges):
                old_cost = len(curr_solution)
                new_cost = len(neighbor)
                if new_cost < old_cost:
                    trace.append(str(time.time() - start_time) + ',' + str(new_cost))
                    curr_solution = neighbor
                    
                else:
                    acceptance_probability = np.exp(np.array((old_cost - new_cost) / T, dtype=np.float128))
                    if acceptance_probability > np.random.random():
                        trace.append(str(time.time() - start_time) + ',' + str(new_cost))
                        curr_solution = neighbor
            
            #count how many iterations quality hasn't improved
            if count_no_improve_iter > longest_no_improve_iter:
                    longest_no_improve_iter = count_no_improve_iter
            
            if len(curr_solution) < best_cost_so_far:
                best_cost_so_far = len(curr_solution)
                count_no_improve_iter = 0
            else:
                count_no_improve_iter += 1

            T = T * alpha
            miu += miu_increase

        else: #if a node is to be added
            if decision(math.exp(-miu)): #add with a probability of exp(miu)
                unincluded_node = all_node - curr_solution
                if len(unincluded_node) != 0: #if solution != all node
                    rand_node = np.random.choice(list(unincluded_node))
                    neighbor = curr_solution | {rand_node}

                    old_cost = len(curr_solution)
                    new_cost = len(neighbor)
                    if new_cost < old_cost:
                        trace.append(str(time.time() - start_time) + ',' + str(new_cost))
                        curr_solution = neighbor
                        
                    else:
                        acceptance_probability = np.exp(np.array((old_cost - new_cost) / T, dtype=np.float128))
                        if acceptance_probability > np.random.random():
                            trace.append(str(time.time() - start_time) + ',' + str(new_cost))
                            curr_solution = neighbor
                    
                    #count how many iterations quality hasn't improved
                    if count_no_improve_iter > longest_no_improve_iter:
                            longest_no_improve_iter = count_no_improve_iter
                    
                    if len(curr_solution) < best_cost_so_far:
                        best_cost_so_far = len(curr_solution)
                        count_no_improve_iter = 0
                    else:
                        count_no_improve_iter += 1
                    
                    T = T * alpha
                    miu += miu_increase 

    return curr_solution, trace

def decision(probability):
    return random.random() < probability

def isValid(vertex_cover, all_edges):
    for u, v in all_edges:
        if u not in vertex_cover and v not in vertex_cover:
            return False
    return True