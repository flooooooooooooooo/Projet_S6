"""import de modules"""
import sys

"""import de modules facultatifs et possiblement non présent d'origine sur python"""
try:
    import concurrent.futures
    from functools import partial
    multiprocessing = True
except:
    multiprocessing = False
try:
    from tkinter.filedialog import askopenfilename, askopendirectory
    tkinter = True
except:
    tkinter = False

"""import de modules personnels"""
import boundary_condition as bc
import initialisation as init
import output_data as out
import solve


if __name__ == "__main__":
    """Initialisation des données"""
    if tkinter:
        input_file = askopenfilename(title="Ouvrir le fichier d'entrée", filetypes=[('txt files','*.txt')])
    else:
        input_file = "input.txt"
    C_0, L, x_d, x_f, D, N_x, t_fin, N_t, boundary_0, boundary_L = init.open_input_file(input_file)
    dt, dx, x, t, C, R = init.initialize_data_numerical_solving(t_fin, N_t, L, N_x, C_0, x_d, x_f, D)
    C_verif = init.initialize_data_exact_solving(N_x, N_t)
    if R >= 1/2:
        print("R = ", R)
        print("Le schéma n'est pas stable")
        answer = input("Voulez-vous continuer ? (O/N)")
        if answer == "N":
            sys.exit()


    """Calcul de la concentration"""
    C = solve.solve_concentration_numericaly(N_t, N_x, R, C,dt,boundary_0,boundary_L)
    C_verif = solve.solve_concentration_exactly(dx, dt, C_verif, N_t, N_x, D)
    diff = solve.difference_exact_numerique(C_verif,C,N_t,N_x)


    """Création des graphiques et de la vidéo"""
    out.initialize_output_file()
    if multiprocessing:
        out.plot_concentration(C, N_t,dt)
    else:
        for i in range(0,N_t):
            out.create_save_plot(dt,C,i)
    out.plot_numerical_exact_comparison(C_verif, C,N_t)
    out.video_concentration()
    out.end_plot(C,N_t,N_x,t_fin)