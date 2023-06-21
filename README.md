Nom du programme : main.py

Date de dernière modification : 16/06/2023

# Auteur : 
Alison Da Silva, Florio Avenel

# Objectif :  
Programme de resolution d'une equation de diffusion
par une methode de différence finie
(schéma Euler explicite en temps et centré en espace)

our déterminer le champ de concentration $C$ à un instant $t_{f}$ dans un milieu diffusif le long d'un domaine de longueur $L$ (par défaut $L=1 \mathrm{~km}$ ) suivant la direction $x$, on est amené à résoudre l'équation différentielle suivante (terme d'advection négligé) :

$$\frac{\partial C(x,t)}{\partial t} = D \frac{\partial^2 C(x,t)}{\partial x^2}$$

La condition initiale à $t=0$ est $C(x, 0)=C_{\text {init }}(x)$ telle que :

$$
C_{\text {init }}(x)=C_{0} \times\left(H\left(x-x_{d}\right)-H\left(x-x_{f}\right)\right)
$$

où $C_{0}$ est la concentration du polluant lors de l'injection dans le domaine, $x_{d}$ et $x_{f}$ sont les positions de début et de fin de la zone de pollution $(0 \leq x_{d}<x_{f} \leq L)$ et $H(x)$ est la fonction d'Heaviside telle que $H(x \geq 0)=1$ et $H(x<0)=0$.


Les conditions limites en $x=0$ et $x=L$ sont des conditions de Dirichlet, à savoir $C(0, t)=f(t)$ et $C(L, t)=0$ avec $t \geq 0$ où $f$ est une fonction du temps qui sera précisée par la suite. Par défaut, $f(t)=0$. La solution numérique de ce problème est obtenue en utilisant la méthode des différences finies. Pour cela, le domaine physique de longueur $L$ et de direction $x$ est discrétisé en $N$ segments de longueur $\Delta x$, ce dernier étant appelé le pas d'espace. Ici, les $N+1$ points $x_{k}$ de calcul seront numérotés de $k=0$ à $k=N$ depuis $x_{0}=0$ jusqu'à $x_{N}=L$. Les solutions en temps sont calculées tous les $\Delta t$ depuis $t=0$ jusqu'à $t_{f}=N_{t} \Delta t$ avec $\Delta t$ appelé le pas de temps et $N_{t}$ est le nombre total de pas de temps.

On souhaite tester le schéma numérique dit « explicite centré » pour résoudre cette équation.


En utilisant un schéma Euler explicite en temps et centré en espace, on obtient la solution en $t+\Delta t$ en fonction de celle en $t$ via :

$$
\begin{array}{ll}
\left.C\left(x_{k}, t+\Delta t\right)=R C\left(x_{k}-\Delta x, t\right)+(1-2 R) C\left(x_{k}, t\right)+R C\left(x_{k}+\Delta x, t\right) \quad \text { pour } k \in\right] 0, N[, \\
C\left(x_{0}, t+\Delta t\right)=f(t+\Delta t) & \text { pour } k=0, \\
C\left(x_{N}, t+\Delta t\right)=0 & \text { pour } k=N,
\end{array}
$$

avec $R=D \Delta t / \Delta x^{2}$, un nombre sans dimension appelé par la suite «nombre de Fourier ».
# Fichier d'entrée:   
Le fichier d'entrée est un fichier texte qui sera selectionner dans le programme si le module tkinter
est installé, sinon il faut le mettre dans le répertoire du programme
avec le nom "input.txt"
le fichier doit être de la forme:
```
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
```

les fonctions dans les deux conditions aux limites peuvent contenir: pi, cos, sin, exp, t, *, +, -, /

# Fichiers résultats :
Création de graphique:      
![Exemple de graphique](assets/Concentration_boundary_0.png)    
images et vidéos stocké dans le dossier output dans le répertoire du programme


# Pour exécuter le programme : 
Afin d'exécuter le programme il faut utiliser la commande `python3 main.py` ou `python main.py`

# Module python aditionnel 
+ module nécessaire : numpy, matplotlib, os, sys, math, subprocess
+ module optionnel : concurrent futures, functools, tkinter