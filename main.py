# system
#from pathlib import Path
import argparse
import networkx as nx
import os
#import time
#import numpy as np
#import math as math
#import matplotlib.pyplot as plt

from BnB import BnB
from LS1 import LS1
from LS2 import LS2
from Approx import Approx

#np.set_printoptions(precision=5)

def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('-inst', "--filename", help = 'filename (e.g. jazz.graph)', type = str)
    parser.add_argument('-alg', "--algorithm", help = 'Methods: BnB|Approx|LS1|LS2', choices=['BnB', 'Approx', 'LS1', 'LS2'], type = str)
    parser.add_argument('-time', "--cutofftime", help= 'cutoff in seconds', type = int)
    parser.add_argument('-seed', "--randomseed", help = 'random seed for randomized methods', type = int)
    args = parser.parse_args()
    return args


def getGraph(filename: str):
    G = nx.Graph()

    nodes_no_edges = set()

    for root, dirs, files in os.walk(os.getcwd()):
        if filename in files :
            with open(os.path.join(root, filename), 'r') as file:
                firstline = file.readline().strip('\n').split(' ')
                vertex_num = firstline[0]
                #edge_num = firstline[1]
                G.add_nodes_from(range(1, int(vertex_num)))

                for vertex_label, line in enumerate(file, 1):
                    adj_edges = line.strip('\n').split(' ')
                    if not adj_edges:
                        nodes_no_edges.add(vertex_label)
                    else:
                        for j in adj_edges:
                            if j != '':
                                G.add_edge(vertex_label, int(j))
 
    return G

def output(vertex_cover_set, 
           trace_history,
           filename: str,
           alg: str,
           time: int,
           seed: int):

    output_folder = os.path.join(os.getcwd(),"output")
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    name = filename.split('/')[-1]
    output_name = name.split('.')[0] + '_' + alg + '_' + str(time) 
    if alg not in ['BnB','Approx']: #deterministic, no random seed in name
        output_name = output_name +'_' + str(seed)
        #output_path += '_' + str(seed) 

    output_path = os.path.join(output_folder,output_name)


    with open(output_path +'.sol', 'w+') as vc_output:
        vc_output.write(str(len(vertex_cover_set)) + '\n')
        vc_output.write(','.join(map(str, list(vertex_cover_set))))
    
    with open(output_path +'.trace', 'w+') as trace_output:
        for history in trace_history:
            trace_output.write(history + '\n') ######check with specs again


def main(filename, alg, time, seed):
    
    graph = getGraph(filename)

    function_mappings = {
        'BnB': BnB,
        'Approx': Approx,
        'LS1': LS1,
        'LS2': LS2
    }

    try:
        vertex_cover_set, trace_history = function_mappings[alg](graph,time,seed)
        output(vertex_cover_set, trace_history, filename, alg, time, seed)
        print('...done!')
        
    except KeyError:
        print ('Invalid method.')

if __name__ == '__main__':
    args = parseArgs()
    main(args.filename, args.algorithm, args.cutofftime, args.randomseed)



   