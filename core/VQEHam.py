from qiskit import ClassicalRegister, QuantumRegister, QuantumCircuit, BasicAer, execute
#from qiskit.visualization import circuit_drawer
#import matplotlib.pyplot as plt
import numpy as np
import random
import time

def Measurement(quantumcircuit, **kwargs):
    """Executes measurements of a QuantumCircuit object 
    
    Parameters:
    quantumcircuit (object) - a QuantumCircuit object to be measured
    
    Keyword Arguments:
    shots (integer) - number of trials to execute for the measurement(s)
    return_M (Bool) - indicates whether to return dictionary of measurement
        results
    print_M (Bool) - indicates whether to print measurement (flipped) results
    column (Bool) - indicates whether to print measurement (flipped) results
        in a vertical column
    """

    # default kwargs
    p_M = True
    Shots=1
    ret = False
    NL = False
    if 'shots' in kwargs:
        Shots = int(kwargs['shots'])
    if 'return_M' in kwargs:
        ret = kwargs['return_M']
    if 'print_M' in kwargs:
        p_M = kwargs['print_M']
    if 'column' in kwargs:
        NL = kwargs['column']
    M1 = execute(quantumcircuit, BasicAer.get_backend('qasm_simulator'),
                 shots=Shots).result().get_counts(quantumcircuit)
    M2 = {}
    k1 = list(M1.keys())
    v1 = list(M1.values())
    for k in np.arange(len(k1)):
        key_list = list(k1[k])
        new_key = ''
        for j in np.arange(len(key_list)):
            new_key = new_key+key_list[len(key_list)-(j+1)]
        M2[new_key] = v1[k]
    if(p_M):
        k2 = list(M2.keys())
        v2 = list(M2.values())
        measurements = ''
        for i in np.arange( len(k2) ):
            m_str = str(v2[i])+'|'
            for j in np.arange(len(k2[i])): 
                if( k2[i][j] == '0' ):
                    m_str = m_str+'0'
                if( k2[i][j] == '1' ):
                    m_str = m_str+'1'
                if( k2[i][j] == ' ' ):
                    m_str = m_str+'>|'
            m_str = m_str+'> '
            if(NL):
                m_str = m_str + '\n'
            measurements = measurements + m_str
        print(measurements)
    if(ret):
        return M2   
    
def Two_Qubit_HEA(qc, params):
    """Applies rotation and entangling gates for a 2-qubit HEA state

    Parameters:
    qc (QuantumCircuit) - the quantum circuit to be measured
    params (array) - contains 8 parameters for current iteration
    """

    qc.ry(params[0], 0)
    qc.rz(params[1], 0)
    qc.ry(params[2], 1)
    qc.rz(params[3], 1)
    qc.cx(0,1)
    qc.ry(params[4], 0)
    qc.rz(params[5], 0)
    qc.ry(params[6], 1)
    qc.rz(params[7], 1)

def Two_Qubit_UniversalAnsatz(qc, params):
    """Applies rotation and entangling gates for a universal 2-qubit ansatz
        state

    Parameters:
    qc (QuantumCircuit) - the quantum circuit to be measured
    params (array) - contains 16 parameters for current iteration
    """

    qc.ry(params[0], 0)
    qc.rz(params[1], 0)
    qc.ry(params[2], 1)
    qc.rz(params[3], 1)
    qc.cx(0,1)
    qc.ry(params[4], 0)
    qc.rz(params[5], 0)
    qc.ry(params[6], 1)
    qc.rz(params[7], 1)
    qc.cx(1,0)
    qc.ry(params[8], 0)
    qc.rz(params[9], 0)
    qc.ry(params[10], 1)
    qc.rz(params[11], 1)
    qc.cx(0,1)
    qc.ry(params[12], 0)
    qc.rz(params[13], 0)
    qc.ry(params[14], 1)
    qc.rz(params[15], 1)
    
def Four_Qubit_HEA(qc, params):
    """Applies rotation and entangling gates for a universal 2-qubit ansatz
        state

    Parameters:
    qc (QuantumCircuit) - the quantum circuit to be measured
    params (array) - contains 16 parameters for current iteration
    """
    qc.ry(params[0], 0)
    qc.rx(params[1], 1)
    qc.ry(params[2], 2)
    qc.rx(params[3], 3)
    qc.cx(0,1)
    qc.cx(1,2)
    qc.cx(2,3)
    qc.ry(params[4], 0)
    qc.rx(params[5], 1)
    qc.ry(params[6], 2)
    qc.rx(params[7], 3)
    qc.cx(1,0)
    qc.cx(2,3)
    qc.cx(1,2)
    qc.ry(params[8], 0)
    qc.rx(params[9], 1)
    qc.ry(params[10], 2)
    qc.rx(params[11], 3)
    qc.cx(0,1)
    qc.cx(1,2)
    qc.cx(2,3)
    qc.ry(params[12], 0)
    qc.rx(params[13], 1)
    qc.ry(params[14], 2)
    qc.rx(params[15], 3)

def VQE_EV(params, Ansatz, H, **kwargs):
    """Computes and returns the expectation value of a Hamiltonian
        for some parametrized ansatz

    Parameters:
    params (array) - parameters for ansatz
    Ansatz (object) - type of ansatz to be used for measurement
    H (dictionary) - Pauli strings as keys and weights as values
    Keyword Arguments:
    shots (integer) - number of measurements to use per computation
    """

    Shots = 1000
    if 'shots' in kwargs:
        Shots = int(kwargs['shots'])
    Hk = list( H.keys() )
    H_EV = 0
    for k in np.arange( len(Hk) ):
        L = list( Hk[k] )
        q = QuantumRegister(len(L))
        c = ClassicalRegister(len(L))
        qc = QuantumCircuit(q,c)
        Ansatz( qc, params )
        for l in np.arange( len(L) ):
            if( L[l] == 'X' ):
                qc.ry(-np.pi/2,q[int(l)])
                qc.measure(int(l),int(l))
            if( L[l] == 'Y' ):
                qc.rx( np.pi/2,q[int(l)])
                qc.measure(int(l),int(l))
            if( L[l] == 'Z' ):
                qc.measure(int(l),int(l))
        M = Measurement( qc, shots=Shots, print_M=False, return_M=True )
        Mk = list( M.keys() )
        H_ev = 0
        for m1 in np.arange(len(Mk)):
            MS = list( Mk[m1] )
            e = 1
            for m2 in np.arange(len(MS)):
                if( MS[m2] == '1'):
                    e = e*(-1)
            H_ev = H_ev + e * M[Mk[m1]]
        H_EV = H_EV + H[Hk[k]]*H_ev/Shots
    return H_EV

def Nelder_Mead(H, Ansatz, Vert, Val):
    """Computes and appends values for the next step in the Nelder Mead
        optimization algorithm

    Parameters:
    H (dictionary) - Pauli strings as keys and weights as values
    Ansatz (function) - 
    Vert (array) -
    """
    alpha = 2
    gamma = 2
    rho   = 0.5
    sigma = 0.5
    add_reflect = False
    add_expand = False
    add_contract = False
    shrink = False
    add_bool = False
#----------------------------------------
    # gets value / index of largest point
    hi = Calculate_MinMax( Val,'max' )
    # gets value / index of all points not the largest
    Vert2 = []
    Val2 = []
    for i in np.arange(len(Val)):
        if( int(i) != hi[1] ):
            Vert2.append( Vert[i] )
            Val2.append( Val[i] )
    Center_P = Compute_Centroid(Vert2)
    Reflect_P = Reflection_Point(Vert[hi[1]],Center_P,alpha)
    #gets expectation value at Reflection Point
    Reflect_V = VQE_EV(Reflect_P,Ansatz,H)
#------------------------------------------------- 
# determine if: reflect / expand / contract / shrink
    hi2 = Calculate_MinMax( Val2,'max' ) # worst
    lo2 = Calculate_MinMax( Val2,'min' ) # best
    if( hi2[0] > Reflect_V >= lo2[0] ):
        add_reflect = True
    elif( Reflect_V < lo2[0] ):
        Expand_P = Reflection_Point(Center_P,Reflect_P,gamma)
        Expand_V = VQE_EV(Expand_P,Ansatz,H)
        if( Expand_V < Reflect_V ):
            add_expand = True
        else:
            add_reflect = True
    elif( Reflect_V > hi2[0] ):
        if( Reflect_V < hi[0] ):
            Contract_P = Reflection_Point(Center_P,Reflect_P,rho)
            Contract_V = VQE_EV(Contract_P,Ansatz,H)
            if( Contract_V < Reflect_V ):
                add_contract = True
            else:
                shrink = True
        else:
            Contract_P = Reflection_Point(Center_P,Vert[hi[1]],rho)
            Contract_V = VQE_EV(Contract_P,Ansatz,H)
            if( Contract_V < Val[hi[1]] ):
                add_contract = True
            else:
                shrink = True
#-------------------------------------------------
 # apply: reflect / expand / contract / shrink
    if( add_reflect == True ):
        new_P = Reflect_P
        new_V = Reflect_V
        add_bool = True
    elif( add_expand == True ):
        new_P = Expand_P
        new_V = Expand_V
        add_bool = True
    elif( add_contract == True ):
        new_P = Contract_P
        new_V = Contract_V
        add_bool = True
    if( add_bool ):
        del Vert[hi[1]]
        del Val[hi[1]]
        Vert.append( new_P )
        Val.append( new_V )
    if( shrink ):
        Vert3 = []
        Val3 = []
        lo = Calculate_MinMax( Val,'min' )
        Vert3.append( Vert[lo[1]] )
        Val3.append( Val[lo[1]] )
        for j in np.arange( len(Val) ):
            if( int(j) != lo[1] ):
                Shrink_P = Reflection_Point(Vert[lo[1]],Vert[j],sigma)
                Vert3.append( Shrink_P )
                Val3.append( VQE_EV(Shrink_P,Ansatz,H) )
        for j2 in np.arange( len(Val) ):
            del Vert[0]
            del Val[0]
            Vert.append( Vert3[j2] )
            Val.append( Val3[j2] )

def Calculate_MinMax(V, C_type):
    """Returns the smallest or biggest value / index in an array"""
    if( C_type == 'min' ):
        lowest = [V[0],0]
        for i in np.arange(1,len(V)):
            if( V[i] < lowest[0] ):
                lowest[0] = V[i]
                lowest[1] = int(i)
        return lowest
    if( C_type == 'max' ):
        highest = [V[0],0]
        for i in np.arange(1,len(V)):
            if( V[i] > highest[0] ):
                highest[0] = V[i]
                highest[1] = int(i)
        return highest
            
def Compute_Centroid(V):
    """Computes and returns the centroid from a given array of values"""
    points = len( V ) # no. of points
    dim = len( V[0] ) # dimension of parameter space
    Cent = []

    # for each parameter, compute average across all 
    for d in np.arange( dim ):
        avg = 0
        for a in np.arange( points ):
            avg = avg + V[a][d]/points
        Cent.append( avg )
    return Cent

def Reflection_Point(P1, P2, alpha):
    """Computes a reflection point from P1 around P2 by an amount alpha"""
    P = []
    for p in np.arange( len(P1) ):
        D = P2[p] - P1[p]
        P.append( P1[p]+alpha*D )
    return P

def runVQE(H, myAnsatz):
    if myAnsatz == Two_Qubit_HEA:
        paramdim = 8
    elif (myAnsatz == Two_Qubit_UniversalAnsatz) or (myAnsatz == Four_Qubit_HEA):
        paramdim = 16

    start_time = time.time()
    lowestvals = []
    P = []
    for p in np.arange(paramdim/2):
        P.append( random.random()*np.pi )
        P.append( random.random()*2*np.pi )
    delta = 0.001
    #------------------------------
    Vertices = []
    Values = []
    # generate initial set of vertices and values
    for v1 in np.arange(len(P)+1):
        V = [] 
        # generates initial set of vertices
        for v2 in np.arange(len(P)):
            # radius ensures points are relatively grouped together;
            # small coordinate perturbations
            R = round((0.4+random.random()*0.8)*(-1)**(round(random.random())),5)
            V.append( P[v2]+R )
        Vertices.append( V )
        # generates initial set of values
        Values.append( VQE_EV(V, myAnsatz, H) )
    #------------------------------
    terminate = False
    iters = 0
    terminate_count = 0
    terminate_limit = 50
    while( (terminate==False) ): #removed maxiters
        iters = iters + 1
        low = Calculate_MinMax( Values,'min' )
        lowestvals.append(low[0])
        Nelder_Mead(H, myAnsatz, Vertices, Values)
        new_low = Calculate_MinMax( Values,'min' )
        if( abs( new_low[0] - low[0] ) < delta ):
            terminate_count += 1
        else:
            terminate_count = 0
        if( terminate_count >= terminate_limit ):
            terminate = True
            print('\n_____ Nelder-Mead Complete _____\n')
            print(' --------------------- \n Iteration: ',iters,'Lowest EV: ',round( low[0],6 ))
        if( ( (iters==1) or (iters%10==0) ) and (terminate==False) ):
            print('Iteration: ',iters,' Lowest EV: ',round( low[0],6 ))
    
    run_time = time.time() - start_time
    return [lowestvals,run_time]