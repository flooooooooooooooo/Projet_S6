import numpy as np
import math
import matplotlib.pyplot as plt
import os
import subprocess
import concurrent.futures
from functools import partial
import sys

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
    C = np.zeros((N_x,N_t), dtype="float16")

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
                """w = 2*math.pi/(t_fin*5)
                C[j,i+1] = 1 + 1*math.sin(w*t)""" # potentiel fonction
                C[j,i+1] = 1 # potentiel fonction
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

def create_save_plot(dt,C,i):
    """Créer et sauvegarde un graphique de la concentration en fonction de la position à un temps donné"""
    plt.plot(C)
    plt.title("Concentration en fonction de la position à t = {} s".format(round(i*dt,2)))
    plt.xlabel("Position")
    plt.ylabel("Concentration")
    plt.ylim(-0.1,2.1)
    plt.savefig("output/C_000{}.png".format(i))
    plt.clf()

def plot_concentration(C, N_t,dt):
    """Fait un graphique de la concentration pour chaque pas de temps calculé"""
    if os.path.isdir("output") == False:
        initialize_output_file()
    if os.path.isfile("output/C_0000.png") == True:
        answer = input("des images existe déjà dans le fichier output, voulez-vous continuez ? (O/N)")
        if answer == "N":
            return
    C = np.transpose(C)
    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.map(partial(create_save_plot,dt),C,range(0,N_t))
        

def plot_numerical_exact_comparison(C_verif, C):
    """Fait un graphique de la comparaison entre la solution exacte et la solution numérique"""
    plt.plot(C_verif[:,N_t-1], color="blue", linestyle="solid")
    plt.plot(C[:,N_t-1], color="red", linestyle="dashed")

    plt.plot(C_verif[:,50000], color="blue", linestyle="solid")
    plt.plot(C[:,50000], color="red", linestyle="dashed")

    plt.plot(C_verif[:,10000], color="blue", linestyle="solid")
    plt.plot(C[:,10000], color="red", linestyle="dashed")

    plt.plot(C_verif[:,5000], color="blue", linestyle="solid")
    plt.plot(C[:,5000], color="red", linestyle="dashed")

    plt.plot(C_verif[:,1000], color="blue", linestyle="solid")
    plt.plot(C[:,1000], color="red", linestyle="dashed")

    plt.plot(C_verif[:,100], color="blue", linestyle="solid")
    plt.plot(C[:,100], color="red", linestyle="dashed")
    plt.title("Comparaison entre la solution exacte et la solution numérique")
    plt.xlabel("Position")
    plt.ylabel("Concentration")
    plt.legend(["Solution exacte", "Solution numérique"])
    plt.savefig("output/numerical_exact_comparison.png")
    plt.clf()

def video_concentration():
    """fait une vidéo de la concentration en fonction de la position à chaque pas de temps avec les images déja créées"""
    if os.path.isfile("output/video_concentration.mp4") == True:
        answer = input("une vidéo existe déjà voulez-vous la supprimer ?(O/N)")
        if answer == "O":
            input("Appuyer sur entrer pour supprimer la vidéo")
        elif answer == "N":
            input("renomer la vidéo avant de continuer, une fois renommer appuyer sur entrer pour continuer")
        os.remove("output/video_concentration.mp4")
    if os.path.isfile("output/C_0000.png") == True:
        subprocess.call("ffmpeg -s 800x600 -i output/C_000%d.png -vcodec libx264 -crf 25 -pix_fmt yuv420p output/video_concentration.mp4")
    else:
        print("Pas de fichier image à convertir en vidéo")

def end_plot(C,N_t,N_x,t_fin):
    """Plot la concentration en fonction de la position à la fin du calcul"""
    x_coord = np.linspace(0,1000,N_x)
    plt.plot(x_coord,C[:,N_t-1])
    plt.title("Concentration en fonction de la position à t = {t_fin} s")
    plt.xlabel("Position")
    plt.ylabel("Concentration")
    plt.show()

"""Main"""

"""Initialisation des données"""
C_0, L, x_d, x_f, D, N_x, t_fin, N_t = open_input_file()
dt, dx, x, t, C, R = initialize_data_numerical_solving(t_fin, N_t, L, N_x, C_0, x_d, x_f, D)
C_verif = initialize_data_exact_solving(N_x)
if R >= 1/2:
    print("Le schéma n'est pas stable")
    answer = input("Voulez-vous continuer ? (O/N)")
    if answer == "N":
        sys.exit()

"""Calcul de la concentration"""
C = solve_concentration_numericaly(N_t, N_x, R, C,t_fin,dt)
C_verif = solve_concentration_exactly(dx, dt, C_verif, N_t, N_x, D)
diff = difference_exact_numerique(C_verif,C,N_t,N_x)

"""Création des graphiques et de la vidéo"""
initialize_output_file()
plot_concentration(C, N_t,dt)
plot_numerical_exact_comparison(C_verif, C)
video_concentration()
end_plot(C,N_t,N_x)


