"""import de modules"""
import sys
import numpy as np

def open_input_file(input_file):
    """Ouvre le fichier input et met les informations dans chaque variables"""
    with open(input_file, "r") as f:
        text = f.readlines()

    for line in text:
        line = line.split("=")
        line[1] = line[1].replace("\n","")
        if line[0] == "C_0":
            C_0 = float(line[1])
        elif line[0] == "L":
            L = float(line[1])
        elif line[0] == "x_d":
            x_d = float(line[1])
        elif line[0] == "x_f":
            x_f = float(line[1])
        elif line[0] == "D":
            D = float(line[1])
        elif line[0] == "N_x":
            N_x = int(line[1])
        elif line[0] == "t_fin":
            t_fin = float(line[1])
        elif line[0] == "N_t":
            N_t = int(line[1])
        elif line[0] == "boundary_0":
            boundary_0 = line[1]
        elif line[0] == "boundary_L":
            boundary_L = line[1]
    
    try:
        return C_0, L, x_d, x_f, D, N_x, t_fin, N_t, boundary_0, boundary_L
    except:
        print("Erreur dans le fichier input")
        sys.exit()

def initialize_data_numerical_solving(t_fin, N_t, L, N_x, C_0, x_d, x_f, D):
    """Initialise les données pour la résolution du schéma numérique"""
    dt = t_fin / (N_t - 1)
    dx = L / (N_x-1)
    x = 0
    t = 0
    C = np.zeros((N_x,N_t), dtype="float128")

    R = D * dt / (dx ** 2)

    for i in range(0,N_x):
        x = i * dx
        if x - x_d < 0 and x - x_f < 0:
            C[i,0] = 0
        elif x - x_d > 0 and x - x_f < 0:
            C[i,0] = C_0
        else:
            C[i,0] = 0
    
    
    return dt, dx, x, t, C, R

def initialize_data_exact_solving(N_x, N_t):
    """Initialise les données pour la résolution exacte"""
    C_verif = np.zeros((N_x,N_t))
    return C_verif