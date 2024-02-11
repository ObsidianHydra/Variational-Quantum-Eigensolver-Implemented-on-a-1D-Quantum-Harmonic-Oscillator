# Variational Quantum Eigensolver Implemented on a 1D Quantum Harmonic Oscillator

## Contents
1. core functions for VQE in 
2. scripts for implementing core functions
3. walkthrough notebook

## Abstract
The rise in development of quantum computing technologies throughout recent
years has heralded the Noisy Intermediate Scale Quantum (NISQ) era, wherein the
limited available number of qubits prevents fault-tolerant error correction and limits
possible applications. Hybrid algorithms involving conventional and quantum re-
sources are often employed so as to make the most out of current architectures. We
investigate a particular hybrid NISQ algorithm known as the Variational Quantum
Eigensolver (VQE) and use it to solve the ground state energy of the 1 dimensional
quantum harmonic oscillator (1D QHO). The Hamiltonians for the 1D QHO are con-
structed in the position basis using discrete versions of the position and momentum
operator, and in the energy basis using discrete ladder operators. We then decom-
pose the Hamiltonians into a sum of tensor products of Identity and Pauli matrices,
known as Pauli strings, that are suitable for measurement on a quantum computer.
The Pauli strings are measured using a 2-qubit hardware efficient ansatz, a univer-
sal 2-qubit ansatz and a 4-qubit ansatz and the expectation values are variationally
minimized using the Nelder-Mead optimization algorithm. The results show that the
cost functions were minimized for the Hamiltonians constructed in both basis except
on the 4-qubit ansatz where the position basis Hamiltonian struggled to converge.
The minimization of the expectation values are affected by each component of the
VQE pipeline, such as the size of the system being studied, the expressiveness and
trainability of the chosen ansatz, and the chosen optimization algorithm.

PACS: 03.67.Lx Quantum computation architectures and implementations, 03.65.Aa
Quantum systems with finite Hilbert space, 03.65.-w Quantum mechanics
