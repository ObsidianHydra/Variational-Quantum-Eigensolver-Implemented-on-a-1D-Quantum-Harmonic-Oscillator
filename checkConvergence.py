from core.buildHam import QHO
from core.encodeHam import h2zixy
from core.VQEHam import runVQE, Two_Qubit_HEA, Two_Qubit_UniversalAnsatz, Four_Qubit_HEA
import pandas as pd

def multiRuns(runs, H, ansatz, fname):
    multires = []
    if ansatz == Two_Qubit_HEA or ansatz == Two_Qubit_UniversalAnsatz:
        save = H["II"]
        del(H["II"])
    elif ansatz == Four_Qubit_HEA:
        save = H["IIII"]
        del(H["IIII"])
    for i in range(runs):
        print("\n_____Multi-Run: Iteration "+str(i+1)+"_____\n")
        results = runVQE(H,ansatz)
        multires.append([results[0] + save,results[1]])
    lowvals = [i[0] for i in multires]
    runtimes = [i[1] for i in multires]
    dict = {'Lowest Values':lowvals, 'Run Times (s)':runtimes}
    df = pd.DataFrame(dict)
    df.to_csv(fname+'.csv')

    return multires

def unliRuns( H, ansatz, fname):
    converged = False
    unlires = []
    iters = 0
    if ansatz == Two_Qubit_HEA or ansatz == Two_Qubit_UniversalAnsatz:
        save = H["II"]
        del(H["II"])
    elif ansatz == Four_Qubit_HEA:
        save = H["IIII"]
        del(H["IIII"])
    while converged == False:
        iters += 1
        print("\n_____Multi-Run: Iteration "+str(iters)+"_____\n")
        results = runVQE(H,ansatz)
        test = results[0] + save
        if(test[-1] <= 0.51):
            converged = True
        unlires.append([test,results[1]])
        print(test[-1])
        
    lowvals = [i[0] for i in unlires]
    runtimes = [i[1] for i in unlires]
    dict = {'Lowest Values':lowvals, 'Run Times (s)':runtimes}
    df = pd.DataFrame(dict)
    df.to_csv(fname+'.csv')

    return unlires

#multiRuns(30,h2zixy(QHO(4,"pos")),Two_Qubit_HEA,"genData/2QHEAPosBasis_30runs")
#multiRuns(30,h2zixy(QHO(4,"pos")),Two_Qubit_UniversalAnsatz,"genData/2QUAPosBasis_30runs")
#multiRuns(30,h2zixy(QHO(16,"pos")),Four_Qubit_HEA,"genData/4QHEQPosBasis_30runs")

#multiRuns(30,h2zixy(QHO(4,"en")),Two_Qubit_HEA,"genData/2QHEAEnBasis_30runs")
#multiRuns(30,h2zixy(QHO(4,"en")),Two_Qubit_UniversalAnsatz,"genData/2QUAEnBasis_30runs")
#multiRuns(30,h2zixy(QHO(16,"en")),Four_Qubit_HEA,"genData/4QHEQEnBasis_30runs")
unliRuns(h2zixy(QHO(16,'en')), Four_Qubit_HEA,"genData/4QHEAEnBasis_unliruns")