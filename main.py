import numpy as np
import math
import matplotlib.pyplot as plt
import os


def open_input_file():
    with open(r"C:\Users\avene\Documents\code\programme_complet\projet_calcul_scientifique\projet_S6\input.txt", "r") as f:
        text = f.readlines()

    for line in text:
        line = line.split("=")
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
    
    return C_0, L, x_d, x_f, D, N_x, t_fin, N_t

def initialize_data_numerical_solving(t_fin, N_t, L, N_x, C_0, x_d, x_f, D):
    dt = t_fin / (N_t + 1)
    dx = L / (N_x + 1)
    x = 0
    t = 0
    C = np.zeros((N_x+1,N_t+1))
    R = D * dt / (dx ** 2)

    for i in range(0,N_x+1):
        x = i * dx
        if x - x_d < 0 and x - x_f < 0:
            C[i,0] = 0
        elif x - x_d > 0 and x - x_f < 0:
            C[i,0] = C_0
        else:
            C[i,0] = 0
    
    return dt, dx, x, t, C, R

def initialize_data_exact_solving(N_x):
    C_verif = np.zeros((N_x+1,N_t+1))
    return C_verif

def solve_concentration_numericaly(N_t, N_x, R, C):
    for i in range(0,N_t):
        for j in range(0,N_x + 1):
            if j == 0:
                C[j,i+1] = 0 # potentiel fonction
            elif j == N_x:
                C[j,i+1] = 0 # potentiel fonction
            else:
                C[j,i+1] = R *C[j-1,i] + (1 - 2 * R) * C[j,i] + R * C[j+1,i]
    return C

def solve_concentration_exactly(dx, dt, C_verif, N_t, N_x, D):
    x = 0
    t = 0
    for j in range(0,N_t+1):
        for i in range(0,N_x+1):
            x = i * dx
            C_verif[i,j] = 1 - math.erf(x/(2*math.sqrt(D*(t))))
        t = j * dt
    return C_verif

def initialize_output_file():
    if os.path.isdir("output") == False:
        os.mkdir("output")

def plot_concentration(C, N_t):
    for i in range(0,N_t+1):
        plt.plot(C[:,i])
        plt.savefig("output/C_{}.png".format(i))
        plt.clf()

def plot_numerical_exact_comparison(C_verif, C):
    plt.plot(C_verif[:,N_t])
    plt.plot(C[:,N_t])
    plt.savefig("output/numerical_exact_comparison.png")
    plt.clf()

C_0, L, x_d, x_f, D, N_x, t_fin, N_t = open_input_file()
dt, dx, x, t, C, R = initialize_data_numerical_solving(t_fin, N_t, L, N_x, C_0, x_d, x_f, D)
C = solve_concentration_numericaly(N_t, N_x, R, C)
