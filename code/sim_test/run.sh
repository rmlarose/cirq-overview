#!bin/bash
# ================================================================================
# run.sh
#
# Bash script wrapper for python code to test Cirq's XmonSimulator performance.
#
# written by Ryan LaRose <laroser1@msu.edu>
# at Michigan State University August 2018.
# ================================================================================

# ============
# outfile name 
# ============

today=`date '+%Y_%m_%d_%H_%M_%S'`;
outfname="timing_$today.txt"

# ============
# main testing
# ============

for n in 10 11 12 13 14 15 16
do
    for depth in 5 10 15 20 25 30
    do
        python sim_test.py $n $depth 1 >> timing/$outfname
    done
done
