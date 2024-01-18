import numpy as np
import matplotlib.pyplot as plt
from core.buildHam import QHO

def exactE(n):
    """Returns exact energy levels of a 1D QHO up to the nth level"""
    E = []
    for i in range(0,n):
        E.append(i+1/2)
    return E

def compareSpect(n):
    """Compares discrete and continuous eigenspectrum of a 1D QHO for n values"""
    H_pos = QHO(n,'pos')
    H_en = QHO(n,'en')
    e_pos, v_pos = np.linalg.eig(H_pos)
    e_en, v_en = np.linalg.eig(H_en)      
    
    E = exactE(n)  
    e_exact = np.arange(1,n+1,1)
    
    plt.rcParams["font.family"] = "Times New Roman"
    fig, ax = plt.subplots(1,1,figsize=(6,5))
    ax.scatter(e_exact, np.sort(e_pos), s=20, c="#1f77b4",
               label="position basis", marker="o")
    ax.scatter(e_exact, np.sort(e_en), s=20, c="#ff7f0e", 
               label="energy basis", marker="v")
    ax.plot(e_exact, E, c ="#2ca02c", label="exact")
    ax.set_xlabel("Eigenvalue")
    ax.set_ylabel("Energy")
    ax.legend()
    plt.savefig("genFigs/compareSpectrum.png", dpi=600)
    plt.show()

compareSpect(64)