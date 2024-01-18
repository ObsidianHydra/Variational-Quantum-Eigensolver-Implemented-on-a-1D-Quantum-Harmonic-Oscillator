from qiskit import QuantumCircuit, execute, BasicAer
import matplotlib.pyplot as plt
import numpy as np

#myqc = QuantumCircuit(2,2)
#myqc.h(0)
#myqc.cx(0,1)
#circuit_drawer(circuit=myqc,output="mpl")
#plt.savefig("genFigs/test.png", dpi=600)


#qc = QuantumCircuit(2,2)
#qc.x(0)
#qc.measure(0,0)
#qc.measure(1,1)
#qc.draw('mpl')
#plt.show()
#results = execute(qc, BasicAer.get_backend("qasm_simulator"), shots=1000).result().get_counts(qc)

from core.buildHam import QHO
from core.encodeHam import h2zixy
from core.VQEHam import runVQE, Two_Qubit_HEA, Four_Qubit_HEA
pauliDecomp = h2zixy(QHO(4,"pos"))
save = pauliDecomp["II"]
del(pauliDecomp["II"])
print(pauliDecomp)
results = runVQE(pauliDecomp, Two_Qubit_HEA)
print("Lowest EV: ", str(results[0][-1] + save))
