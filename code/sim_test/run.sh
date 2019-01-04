#!bin/bash
# ================================================================================
# run.sh
#
# Bash script wrapper for python code to test Cirq's simulator performance.
# ================================================================================

# ============
# outfile name 
# ============

today=`date '+%Y_%m_%d_%H_%M_%S'`;
outfname="timing_$today.txt"

# ============
# main testing
# ============

for n in 10 12 14 16 18 20 22 24
do
    echo "n=$n"
    for depth in 20 40 60 80 100
    do
	echo "depth=$depth"
        python sim_test.py $n $depth 1 1 >> timing/$outfname
    done
done
