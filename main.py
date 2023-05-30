import numpy as np
import math
import matplotlib.pyplot as plt
import os
import subprocess

def open_input_file():
    """Ouvre le fichier input et met les informations dans chaque variables"""
    with open(r"input.txt", "r") as f:
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
    """Initialise les données pour la résolution du schéma numérique"""
    dt = t_fin / N_t
    dx = L / N_x
    x = 0
    t = 0
    C = np.zeros((N_x,N_t))
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

def initialize_data_exact_solving(N_x):
    """Initialise les données pour la résolution exacte"""
    C_verif = np.zeros((N_x,N_t))
    return C_verif

def solve_concentration_numericaly(N_t, N_x, R, C,t_fin,dt):
    """Résout le schéma numérique"""
    for i in range(0,N_t-1):
        t = i * dt
        for j in range(0,N_x):
            if j == 0:
                """w = 10*math.pi/t_fin
                C[j,i+1] = 1 + 1*math.sin(w*t)""" # potentiel fonction
                C[j,i+1] = 0 # potentiel fonction
            elif j == N_x -1:
                C[j,i+1] = 0 # potentiel fonction
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
            C_verif[i,j] = 1 - math.erf(x/(2*math.sqrt(D*(t))))
        
    return C_verif

def difference_exact_numerique(C_verif,C,N_t,N_x):
    """Calcul la différence entre la solution exacte et la solution numérique"""
    diff = np.zeros((N_x,N_t))
    for i in range(0,N_t):
        for j in range(0,N_x):
            diff[j,i] = C_verif[j,i] - C[j,i]
    return diff

def initialize_output_file():
    """Initialise le dossier output"""
    if os.path.isdir("output") == False:
        os.mkdir("output")

def plot_concentration(C, N_t):
    """Plot la concentration en fonction du temps"""
    for i in range(0,N_t+1):
        plt.plot(C[:,i])
        plt.savefig("output/C_000{}.png".format(i))
        plt.clf()

def plot_numerical_exact_comparison(C_verif, C):
    """Plot la comparaison entre la solution exacte et la solution numérique"""
    plt.plot(C_verif[:,N_t-1], color="blue", linestyle="solid")
    plt.plot(C[:,N_t-1], color="red", linestyle="dashed")
    plt.savefig("output/numerical_exact_comparison.png")
    plt.clf()

def video_concentration():
    subprocess.call("ffmpeg -s 800x600 -i output/C_000%d.png -vcodec libx264 -crf 25 -pix_fmt yuv420p output/video_concentration.mp4", shell=True)

def end_plot(C,N_t,N_x):
    """Plot la concentration en fonction de la position à t = 1000 s"""
    x_coord = np.linspace(0,1000,N_x)
    plt.plot(x_coord,C[:,N_t-1])
    plt.title("Concentration en fonction de la position à t = 1000000 s")
    plt.xlabel("Position")
    plt.ylabel("Concentration")
    plt.show()

"""Main"""
C_0, L, x_d, x_f, D, N_x, t_fin, N_t = open_input_file()
dt, dx, x, t, C, R = initialize_data_numerical_solving(t_fin, N_t, L, N_x, C_0, x_d, x_f, D)
print(R)
C = solve_concentration_numericaly(N_t, N_x, R, C,t_fin,dt)
#C_verif = initialize_data_exact_solving(N_x)
#C_verif = solve_concentration_exactly(dx, dt, C_verif, N_t, N_x, D)
#diff = difference_exact_numerique(C_verif,C,N_t,N_x)
initialize_output_file()
x_coord = np.linspace(0,1000,N_x)
plt.plot(x_coord,C[:,N_t-1])
plt.title("Concentration à t = 1000 s")
plt.xlabel("Position")
plt.ylabel("Concentration")
plt.show()
#plot_concentration(diff, N_t)
#plot_numerical_exact_comparison(C_verif, C)
#end_plot(C,N_t,N_x)


