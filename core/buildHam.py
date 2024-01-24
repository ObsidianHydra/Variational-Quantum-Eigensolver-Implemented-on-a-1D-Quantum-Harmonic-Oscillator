import numpy as np
    
def ell(i,n):
    """Returns the index of the ith site for a lattice with n sites""" 
    return (2*i - 1 - n)/2

#discrete fourier transform
def DFT(n):
    """Returns the discrete fourier transform for n lattice sites"""
    F = []
    for j in range(1,n+1):
        F_row = []
        for k in range(1,n+1):
            F_row.append((1/np.sqrt(n)) * np.exp((2*np.pi*1j*ell(j,n)*ell(k,n)) / n ))
        F.append(F_row)
    F = np.matrix(np.round(F,10))
    return F

#position operator
def X_pos(n):
    """Returns the discrete position operator for n lattice sites"""
    X = []
    for j in range(1,n+1):
        X_row = []
        for k in range(1,n+1):
            if j==k:
                 X_row.append(np.sqrt(2*np.pi/n) * ell(j,n))
            else:
                X_row.append(0)
        X.append(X_row)
    return np.matrix(np.round(X,10))

def P_pos(n):
    """Returns the discrete momentum operator for n lattice sites"""
    F = DFT(n)
    X_op = X_pos(n)
    F_dag = F.H
    return np.round((F_dag*X_op*F),10)


def A_minus(n):
    """Returns the discrete annihilation operator for n energy levels"""
    A = []
    for j in range(1,n+1):
        A_row = []
        for k in range(1,n+1):
            if j == (k-1):
                A_row.append(np.sqrt(j))
            else:
                A_row.append(0)
        A.append(A_row)
    return np.matrix(A)


def A_plus(n):
    """Returns the discrete creation operator for n energy levels"""
    A = []
    for j in range(1,n+1):
        A_row = []
        for k in range(1,n+1):
            if j == (k+1):
                A_row.append(np.sqrt(k))
            else:
                A_row.append(0)
        A.append(A_row)
    return np.matrix(A)

def QHO(n,basis):
    """Returns discrete 1D QHO of size n constructed in chosen basis"""
    if basis == 'pos':
        X_op = X_pos(n)
        P_op = P_pos(n)
        H = (X_op*X_op)/2 + (P_op*P_op)/2
        return H
    elif basis == 'en':
        A_dag = A_minus(n)
        A_undag = A_plus(n)
        H = (A_dag*A_undag) + np.identity(n)/2
        return H