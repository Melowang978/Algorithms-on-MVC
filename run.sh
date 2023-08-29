#!/bin/sh
echo "running:  \n"
cd DATA
datafiles=`ls *.graph`
# as-22july06.graph email.graph hep-th.graph  karate.graph power.graph star2.graph delaunay_n10.graph football.graph jazz.graph  netscience.graph  star.graph
cd ..
for datafile in as-22july06.graph email.graph hep-th.graph  karate.graph power.graph star2.graph delaunay_n10.graph football.graph jazz.graph  netscience.graph  star.graph
do
    for CUTTIME in 55
    do 
        for ALG in Approx
        do  
            for SEED in 001
            do 
                echo "python main.py -inst $datafile -alg $ALG -time $CUTTIME -seed $SEED\n"
                python main.py -inst $datafile -alg $ALG -time $CUTTIME -seed $SEED
            done
        done
    done
done
