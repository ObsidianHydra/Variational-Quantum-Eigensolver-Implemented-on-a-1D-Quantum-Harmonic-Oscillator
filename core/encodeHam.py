import numpy as np
import itertools

def h2zixy(ham):
    """Decompose square real symmetric matrix into Pauli spin matrices 
    
    Parameters:
    ham (array) - a square numpy real symmetric numpy array
    
    Returns:
    a dictionary of Pauli string keys with weights as values
    """

    # weights smaller than eps are taken to be zero
    eps = 1.e-5
    
    dim = len(ham)
    
    # Step 1: expand Hamiltonian to have leading dimension = power of 2 and
    # pad with zeros if necessary

    NextPowTwo = int(2**np.ceil(np.log(dim)/np.log(2)))
    if NextPowTwo != dim:
        diff = NextPowTwo - dim
        ham = np.hstack((ham, np.zeros((dim,diff))))
        dim = NextPowTwo
        ham = np.vstack((ham, np.zeros((diff,dim))))
    
    # Step 2: generate all tensor products of the appropriate length with
    # all combinations of I, X, Y, Z, excluding those with an odd number of Y
    # matrices
    
    # Pauli is a dictionary with the four basis 2x2 Pauli matrices
    Pauli = {'I' : np.array([[1,0],[0,1]]),
             'X' : np.array([[0,1],[1,0]]),
             'Y' : np.array([[0,-1j],[1j,0]]),
             'Z' : np.array([[1,0],[0,-1]])}
    NumTensorRepetitions = int(np.log(dim) / np.log(2))
    PauliKeyList = []
    KeysToDelete = []
    PauliDict = {}
    
    def PauliDictValues(l):
        # returns a generator object, such that calling again yields the next object
        yield from itertools.product(*([l] * NumTensorRepetitions))
    

    # generate list of tensor products with all combinations of Pauli
    # matrices i .e. 'III', 'IIX', 'IIY', etc.
    for x in PauliDictValues('IXYZ'):
        PauliKeyList.append(''.join(x))
    
    for y in PauliKeyList:
        PauliDict[y] = 0
        
    for key in PauliDict:
        TempList = []
        PauliTensors = []
        NumYs = key.count('Y')
        TempKey = str(key)
    
        if (NumYs % 2) == 0:
            for string in TempKey:
                TempList.append(string)
            
            for SpinMatrix in TempList:
                PauliTensors.append(Pauli[SpinMatrix])
            
            PauliDict[key] = PauliTensors
            CurrentMatrix = PauliDict[key].copy()

            # compute tensor product between I , X , Y , Z matrices
            for k in range(1, NumTensorRepetitions):
                TemporaryDict = np.kron(CurrentMatrix[k-1], CurrentMatrix[k])
                CurrentMatrix[k] = TemporaryDict
        
            PauliDict[key] = CurrentMatrix[-1]
        
        else:
            KeysToDelete.append(key)
    
    for val in KeysToDelete:
        PauliDict.pop(val)
    
    # Step 3: loop through all the elements of the Hamiltonian matrix
    # and identify which Pauli matrix combinations contribute;
    # generate a matrix of simultaneous equations that need to be solved;
    # N.B. upper triangle of hamiltonian array is used  

    VecHamElements = np.zeros(int((dim**2 + dim) / 2))
    h=0
    for i in range(0,dim):
        for j in range(i,dim):
            arr = []
            VecHamElements[h] = ham[i,j]
            for key in PauliDict:
                TempVar = PauliDict[key]
                arr.append(TempVar[i,j].real)
            if i == 0 and j == 0:
                FinalMat = np.array(arr.copy())
            else:
                FinalMat = np.vstack((FinalMat,arr))
            
            h += 1
    
    # Step 4: use numpy.linalg.solve to solve the simultaneous equations
    # and return the weights of the Pauli strings

    x = np.linalg.solve(FinalMat,VecHamElements)
    var_list = list(PauliDict.keys())
    
    # return final Pauli decomposition of the Hamiltonian
    decHam = {}
    for i in range(len(PauliDict)):
        if abs(x[i])>eps:
            decHam[str(var_list[i])] = np.round(x[i],4)
            
    return decHam