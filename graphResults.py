import pandas as pd 
from core.buildHam import QHO
import numpy as np
import matplotlib.pyplot as plt

def shortlist(path, msize, basis):
    # Grab a shortlist of accurate ground states
    vals, vecs = np.linalg.eig(QHO(msize,basis))
    exact = np.sort(vals)[0]
    
    df = pd.read_csv(path)
    header1 = df.columns.values[1]
    header2 = df.columns.values[2]

    acc = 50
    for i in range(len(df[header1])):
        removebracks = df[header1][i].replace("[","").replace("]","")
        mylist = removebracks.split()
        numlist = [float(i) for i in mylist]
        run_time = float(df[header2][i])

        if abs(numlist[-1] - exact) < acc:
            acc = abs(numlist[-1] - exact)
            slvals = []
            sltimes = []
            slvals.append(numlist)
            sltimes.append(run_time)
        elif abs(numlist[-1] - exact) == acc:
            slvals.append(numlist)
            sltimes.append(run_time)
    return slvals, sltimes, exact

# Edit paths and matrix size here
mypathen = "genData/2QHEAEnBasis.csv"
slvalsen, sltimesen, exacten = shortlist(mypathen,4,"en")
mypathpos = "genData/2QHEAPosBasis.csv"
slvalspos, sltimespos, exactpos = shortlist(mypathpos,4,"pos")
# Edit img path here
imgpath  ="genFigs/2QHEA.png"

maxlen = 500
# Grab shortest number of iterations and graph
import matplotlib.pyplot as plt
for i in range(len(slvalsen)):
    if len(slvalsen[i]) < maxlen:
        tographen = []
        maxlen = len(slvalsen[i])
        tographen.append(slvalsen[i])
        tographen.append(sltimesen[i])
maxlen = 500
for i in range(len(slvalspos)):
    if len(slvalspos[i]) < maxlen:
        tographpos = []
        maxlen = len(slvalspos[i])
        tographpos.append(slvalspos[i])
        tographpos.append(sltimespos[i])
print(tographpos[1])

fig, ax = plt.subplots(1, 1, figsize=(6,5))
ax.plot(range(0,len(tographpos[0])),tographpos[0],marker="o", markersize = 7,
        markevery=10, linewidth = 1, linestyle = 'dotted')
ax.plot(range(0,len(tographen[0])),tographen[0],marker="^", markersize = 7,
        markevery=10, linewidth = 1, linestyle = 'dotted')
ax.plot((0,300),(exactpos,exactpos),color='red', linewidth = 1, linestyle="dashed")
ax.plot((0,300),(exacten,exacten),color='blue', linewidth = 1, linestyle="dashed")
ax.set_ylabel("Cost Function")
ax.set_xlabel("nth Iteration")
ax.legend(["position basis; runtime = "+str(round(tographpos[1],3)) + " s\n" r"$E_{VQE} = $" + str(np.round(tographpos[0][-1],4)),
           "energy basis; runtime = "+str(round(tographen[1],3)) + " s\n" r"$E_{VQE} = $" + str(np.round(tographen[0][-1],4)),
           "position basis "+ r"$E_0$ = "+str(np.real(np.round(exactpos,4))),
           "energy basis " + r"$E_0$ = "+str(exacten)],loc='best')

plt.savefig(imgpath, dpi=600)
plt.show()
