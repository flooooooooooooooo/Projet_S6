"""import de modules"""
import numpy as np
import math

"""import de modules personnels"""
import boundary_condition as bc

def solve_concentration_numericaly(N_t, N_x, R, C,dt,boundary_0,boundary_L):
    """Résout le schéma numérique"""
    for i in range(0,N_t-1):
        t = i * dt
        for j in range(0,N_x):
            if j == 0:
                result = bc.Calcul(boundary_0, i*dt)
                C[j,i+1] = result.return_result()
            elif j == N_x -1:
                result = bc.Calcul(boundary_L, i*dt)
                C[j,i+1] = result.return_result()
            else:
                C[j,i+1] = R *C[j-1,i] + (1 - 2 * R) * C[j,i] + R * C[j+1,i]
    return C

def solve_concentration_exactly(dx, dt, C_verif, N_t, N_x, D):
    """Calcul la solution exacte du problème"""
    x = 0
    t = 0
    for j in range(1,N_t):
        t = j * dt
        for i in range(0,N_x):
            x = i * dx
            C_verif[i,j] = 1 - math.erf(x/(2*np.sqrt(D*(t))))
        
    return C_verif

def difference_exact_numerique(C_verif,C,N_t,N_x):
    """Calcul la différence entre la solution exacte et la solution numérique"""
    diff = np.zeros((N_x,N_t))
    for i in range(0,N_t):
        for j in range(0,N_x):
            diff[j,i] = C_verif[j,i] - C[j,i]
    return diff