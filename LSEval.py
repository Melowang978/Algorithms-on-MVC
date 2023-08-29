import matplotlib.pyplot as plt
import os
import csv
import argparse

# you can run this like: LSEval.py -inst power.graph -alg LS1 -time 500 
# **time is the cutoff time in the name of output files we want

def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('-inst', "--filename", help = 'filename: power.graph|star2.graph', choices=['dummy1.graph','power.graph','star2.graph'], type = str)
    parser.add_argument('-alg', "--algorithm", help = 'Methods: BnB|Approx|LS1|LS2', choices=['BnB', 'Approx', 'LS1', 'LS2'], type = str)
    parser.add_argument('-time', "--cutofftime", help= 'cutoff time in output file name', type = int)
    args = parser.parse_args()
    return args


def importTraceFile(root, filename):
    #output trace dictionary key = time, value = solution size
    #round runtime to two digit

    with open(os.path.join(root, filename), 'r') as file:
        reader = csv.reader(file)
        trace_dict = {round(float(rows[0]),2):int(rows[1]) for rows in reader}
    return trace_dict

def importAllTrace(graph_filename, alg, cutoff_time):
    # import all trace file with given name, alg, and time
    # output list of dict
  
    number_of_output = 0
    all_trace = []

    #read all files starts with ... and end with ".trace"
    output_name = graph_filename.split('.')[0] + '_' + alg + '_' + str(cutoff_time)
    for root, dirs, files in os.walk(os.getcwd()):
        for filename in files:
            if filename.endswith('.trace') and filename.startswith(output_name):
                number_of_output += 1
                trace_ordered_dict = importTraceFile(root, filename)
                all_trace.append(trace_ordered_dict)
                
    #check if we found at least 10 outputfiles
    if number_of_output < 10:
        raise('We need more than 10 outputs')
    
    return number_of_output, all_trace

def RelErr(vc_size,opt):
    #round to two digit
    return round((vc_size-opt)/opt,2)

def calculateRelErr(graph_filename, all_trace):
    if graph_filename == 'star2.graph':
        opt = 4542
    
    elif graph_filename == 'power.graph':
        opt = 2203

    elif graph_filename == 'dummy1.graph':
        opt = 3
    else:
        raise('invalid file name')

    #round to two digit
    for trace_dict in all_trace:
        trace_dict.update((time, RelErr(vc_size,opt)) for time, vc_size in trace_dict.items())

    return all_trace

##################################################################################
#def calculatePSolveGivenRelErr(RelErr, number_of_output, all_RelErr_trace):
    # number_of_success = ...
#    return #...

#def calculatePSolveGivenRuntime(Runtime, number_of_output, all_RelErr_trace):
    # number_of_success = ...
    #return #...

    

#def plotQrtd (): #plot result from calculatePSolveGivenRelErr

#def plotSqd(runtime) #plot result from calculatePSolveGivenRuntime 



def plotAll(graph_filename, alg, cutoff_time):
    number_of_output, all_trace = importAllTrace(graph_filename, alg, cutoff_time)
    all_RelErr_trace = calculateRelErr(graph_filename, all_trace)

    for RelErr_trace in all_RelErr_trace:
        print(RelErr_trace)
    #############################################
    ###### Skeleton for calculating the plot#####
    #RelErr_list = [0.2,0.4,0.6,0.8,1] #example
    #for RelErr in RelErr_list:
        #... = calculatePSolveGivenRelErr(RelErr, number_of_output, all_RelErr_trace) 
    

    #runtime_list = [50 ,100, 200, 300, 400]#example
    #for rntime in Runtime_list:
        #... = calculatePSolveGivenRelErr(RelErr, number_of_output, all_RelErr_trace) 

    #############################################
    ###### Actually plot the result #####
    #plotQrtd(...)
    #plotSqd(...)

    #return

if __name__ == '__main__':
    args = parseArgs()
    plotAll(args.filename, args.algorithm, args.cutofftime,)
