#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# =============================================================================
# cirq_test.py
#
# Testing out the new quantum software Cirq by Google.
#
# written by Ryan LaRose <rlarose@umich.edu>
# in Santa Fe, NM August 2018.
# =============================================================================

# =============================================================================
# imports
# =============================================================================

import cirq

import sys
import time
import numpy as np

# =============================================================================
# constants
# =============================================================================

# =============================================================================
# functions
# =============================================================================

def rng(repetitions=10, verbose=False):
    # get a qubit
    qbit = cirq.LineQubit(0)
    
    # create a circuit
    circuit = cirq.Circuit.from_ops(
            cirq.H(qbit),
            cirq.measure(qbit, key='z')
            )
    
    # get a simulator and run the circuit
    simulator = cirq.google.XmonSimulator()
    outcome = simulator.run(circuit, repetitions=repetitions)
    
    # output
    print(outcome.histogram(key='z'))
    print(outcome)
    outstring = outcome.__str__()
    print("number of 0's = {}".format(
            outstring.count('0', outstring.find('='))))
    print("number of 1's = {}".format(
            outstring.count('1', outstring.find('='))))
    
def teleport():
    pass

def hst(length=4):
    qbits = [cirq.GridQubit(ii, 0) for ii in range(length)]
    circ = cirq.Circuit()
    circ.append([cirq.H.on(q) for q in qbits if (q.row + q.col) < length // 2],
                strategy=cirq.InsertStrategy.EARLIEST)
    for ii in range(length // 2):
        circ.append(cirq.CNOT.on(qbits[ii], qbits[ii + length // 2]),
                    strategy=cirq.InsertStrategy.EARLIEST)
        
    print(circ)
    
def sim_test(nqubits, depth, nreps, 
             insert_strategy=cirq.InsertStrategy.EARLIEST, 
             verbose=False):
    """
    Simulator test for Cirq.
    """
    # get a simulator
    simulator = cirq.google.XmonSimulator()
    
    # get some qubits and a circuit
    qbits = [cirq.GridQubit(ii, 0) for ii in range(nqubits)]
    circ = cirq.Circuit()
    
    # =========================================================================
    # random circuit
    # =========================================================================
    
    def rot(qubit, params):
        """
        Helper function to return an arbitrary rotation of the form
        R = Rx(params[0]) * Ry(params[1]) * Rz(params[2])
        on the qubit.
        """
        rx = cirq.RotXGate(half_turns=params[0])
        ry = cirq.RotYGate(half_turns=params[1])
        rz = cirq.RotZGate(half_turns=params[2])
        
        yield (rx(qubit), ry(qubit), rz(qubit))

    for _ in range(depth):
        # random single qubit rotations
        for q in qbits:
            circ.append(rot(q, 2 * np.random.rand(3) - 1),
                        strategy=insert_strategy)
        
        # layer of CNOTS
        for q in qbits:
            circ.append([cirq.CNOT(q, targ) for targ in qbits if targ != q],
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
    
    print(nqubits, depth, 
          shots, sim_test(nqubits, depth, shots, verbose=verbose))
    
# =============================================================================
# script
# =============================================================================
    
if __name__ == "__main__":
    main()