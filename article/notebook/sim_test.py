#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# =============================================================================
# sim_test.py
#
# Testing out the simulator in Cirq.
#
# written by Ryan LaRose <laroser1@msu.edu>
# at Michigan State University August 2018.
# =============================================================================

# =============================================================================
# imports
# =============================================================================

import cirq

import numpy as np
import sys
import time

# =============================================================================
# functions
# =============================================================================

def sim_test(nqubits, depth, nreps, 
             insert_strategy=cirq.InsertStrategy.EARLIEST, 
             verbose=False):
    """
    Cirq XmonSimulator test for a circuit structure of layers consisting of
    random one qubit rotations and CNOTs between all qubits.
    
    input:
        nqubits [type: int]
            number of qubits in the circuit
            
        depth [type: int]
            number of layers (described above) in the circuit
            
        nreps [type: int]
            number of times to run the circuit as per the keyword argument
            'repetitions' in the method cirq.google.XmonSimulator.run.
            
        insert_strategy [type: cirq.InsertStrategy,
                         default = cirq.InsertStrategy.EARLIEST]
            insert strategy for new gates in the circuit
        
        verbose [type: bool,
                 default = False]
            flag for verbose output to console (prints out circuit)
            
    returns:
        (runtime of simulating the circuit) / nreps
    """
    # get a simulator
    simulator = cirq.google.XmonSimulator()
    
    # get some qubits and a circuit
    qbits = [cirq.LineQubit(x) for x in range(nqubits)]
    circ = cirq.Circuit()
    
    # =========================================================================
    # random circuit
    # =========================================================================
    
    def rot(qubit, params):
        """
        Helper function to return an arbitrary rotation of the form
        R = Rz(params[2]) * Ry(params[1]) * Rx(params[0])
        on the qubit.
        """
        rx = cirq.RotXGate(half_turns=params[0])
        ry = cirq.RotYGate(half_turns=params[1])
        rz = cirq.RotZGate(half_turns=params[2])
        
        yield (rx(qubit), ry(qubit), rz(qubit))

    for _ in range(depth):
        # append random single qubit rotations
        for q in qbits:
            circ.append(rot(q, 2 * np.random.rand(3) - 1),
                        strategy=insert_strategy)

        # get a random control qubit for cnots
        ctrl = qbits[np.random.randint(len(qbits))]

        # append layer of CNOTS
        circ.append([cirq.CNOT(ctrl, targ) for targ in qbits if targ != ctrl],
                     strategy=insert_strategy)
    # measurements     
    for q in qbits:
        circ.append(cirq.measure(q),
                    strategy=cirq.InsertStrategy.INLINE)
    
    # verbose options
    if verbose:
        print('Circuit structure shown below:', circ, sep='\n')
        
    # =========================================================================
    # do the circuit execution and time it
    # =========================================================================
    
    start = time.time()
    simulator.run(circ, repetitions=nreps)
    return (time.time() - start) / nreps

# =============================================================================
# main 
# =============================================================================

def main():
    """
    Main function for the script.
    """
    # grab user input    
    if len(sys.argv) >= 2:
        nqubits = int(sys.argv[1])
    else:
        nqubits = 2
    if len(sys.argv) >= 3:
        depth = int(sys.argv[2])
    else:
        depth = 3
    if len(sys.argv) >= 4:
        shots = int(sys.argv[3])
    else:
        shots = 1
    if len(sys.argv) >= 5:
        verbose=True
    else:
        verbose=False
        
    # run the simulator test and print the results
    print(nqubits, depth, 
          shots, sim_test(nqubits, depth, shots, verbose=verbose))
    
# =============================================================================
# script
# =============================================================================
    
if __name__ == "__main__":
    main()