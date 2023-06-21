Nom du programme : main.py

Date de dernière modification : 16/06/2023

# Auteur : 
Alison Da Silva, Florio Avenel

# Objectif :  
Programme de resolution d'une equation de diffusion
par une methode de différence finie
(schéma Euler explicite en temps et centré en espace)

# Fichier d'entrée:   
fichier texte qui sera selectionner dans le programme si le module tkinter
est installé, sinon il faut le mettre dans le répertoire du programme
avec le nom "input.txt"
le fichier doit être de la forme:
'''
C_0=
L=
x_d=
x_f=
D=
N_x=
t_fin=
N_t=
boundary_0=
boundary_L=
'''

les fonctions dans les deux conditions aux limites peuvent contenir: pi, cos, sin, exp, t, *, +, -, /

Fichiers résultats : images et vidéos dans le dossier output dans le répertoire du programme


Pour exécuter le programme : python3 main.py ou python main.py

module nécessaire : numpy, matplotlib, os, sys, math, subprocess
module optionnel : concurrent futures, functools, tkinter