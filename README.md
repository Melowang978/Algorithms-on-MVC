# CSE 6140 Fall 2022 Project - Minimum Vertex Cover 

`main.py` is the main function that runs a given algorithm on a given input graph with proper cutoff time and seed value. 

Usage: ```main.py [-h] -args filename -alg {BnB,Approx,LS1,LS2} -time cutoff -seed seed_value```

Positional arguments:
```bash
  filename              name of the data file (e.g. jazz.graph)
  {BnB,Approx,LS1,LS2}  algorithm to use
  cutoff                cut-off time in seconds
  seed_value            seed to generate the random numbers (for local search algorithms only)
```
Optional arguments:
```bash
  -h, --help            show this help message and exit
```

## Example:
```zsh
python main.py -time 500 -seed 11 -inst power.graph -alg Approx
```

---

## Directory Structure:
```tree
.
├── run.sh (script to run the experiments)
├── main.py (main code to execute a given algorithm on a given input graph using user defined parameters)
├── Approx.py (approximate algorithm)
├── BnB.py (branch and bound algorithm - intelligent exhaustive search)
├── LS1.py (local search method 1 - simulated annealing ?? CHANGE IT IF WRONG)
├── LS2.py (local search method 2 - hill climbing ?? CHANGE IT IF WRONG)
├── README.md
 - - - - - - -Output Folder  - - - - - - - 
├── output (outputs folder)
|   └── Additional LS1 experiment folder
|   |   └── Solution Files (*.sol)
|   |   └── Solution Trace Files (*.trace)
|   └── Additional LS2 experiment folder
|   |   └── Solution Files (*.sol)
|   |   └── Solution Trace Files (*.trace)
|   └── Solution Files (*.sol)
|   └── Solution Trace Files (*.trace)    
 - - - - - - - - Data Input  - - - - - - - 
├── DATA (data folder)
│   ├── ExampleSolutions
│   │   ├── dummy1.sol
│   │   ├── dummy2.sol
│   │   ├── email.sol
│   │   └── jazz.sol
│   ├── as-22july06.graph
│   ├── delaunay_n10.graph
│   ├── dummy1.graph
│   ├── dummy2.graph
│   ├── email.graph
│   ├── football.graph
│   ├── hep-th.graph
│   ├── jazz.graph
│   ├── karate.graph
│   ├── netscience.graph
│   ├── power.graph
│   ├── star.graph
│   └── star2.graph
 - - - - - - - - - - - - - - - - - - - -

```
