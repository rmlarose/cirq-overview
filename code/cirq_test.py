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
    
# =============================================================================
# main 
# =============================================================================

def main():
    rng()
    
# =============================================================================
# script
# =============================================================================
    
if __name__ == "__main__":
    main()