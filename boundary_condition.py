"""import de modules"""
import math

class Calcul:
    """Calcul les conditions aux limites"""

    def __init__(self, f, t):
        """Initialise les données pour le calcul des conditions aux limites"""
        self.chiffre_list = []
        self.calcul_list_total = []
        self.f = f
        self.t = t
        self.start = None
        self.end = None
        self.brackets_number = 0
        self.define_calcul()


    def define_calcul(self):
        """ecrit le calcul sous forme d'une liste"""
        chiffre_float = None
        chiffre_str = None
        for car in self.f:
            if car == " ":
                continue
            elif car == ".":
                self.chiffre_list.append(car)
                continue
            elif car == "p":
                chiffre_pi = "p"
                continue
            elif car == "i" and chiffre_pi == "p":
                chiffre_pi = ""
                car = str(math.pi)

            try:
                c = float(car)
                self.chiffre_list.append(car)
            except:
                if self.chiffre_list != [] or len(self.chiffre_list) > 1:
                    chiffre_str = "".join(self.chiffre_list)
                    chiffre_float = float(chiffre_str)
                elif self.chiffre_list != []:
                    chiffre_str = self.chiffre_list[0]
                    chiffre_float = float(chiffre_str)
                if chiffre_float != None:
                    self.calcul_list_total.append(chiffre_float)
                self.calcul_list_total.append(car)
                self.chiffre_list = []
                chiffre_float = None
                chiffre_str = None

        if self.chiffre_list != [] or len(self.chiffre_list) > 1:
            chiffre_str = "".join(self.chiffre_list)
            chiffre_float = float(chiffre_str)
        elif self.chiffre_list != []:
            chiffre_str = self.chiffre_list[0]
            chiffre_float = float(chiffre_str)
        if chiffre_float != None:
            self.calcul_list_total.append(chiffre_float)
        self.calcul(self.calcul_list_total)


    def multiplication(self):
        """calcul les multiplications"""
        for i in range(len(self.calcul_list)):
            if self.calcul_list[i] == "*":
                if self.calcul_list[i+1] == "t":
                    self.calcul_list[i-1] = self.calcul_list[i-1] * self.t
                elif self.calcul_list[i-1] == "t":
                    self.calcul_list[i-1] = self.t * self.calcul_list[i+1]
                else:
                    self.calcul_list[i-1] = self.calcul_list[i-1] * self.calcul_list[i+1]
                del self.calcul_list[i:i+2]
                break
    

    def division(self):
        """calcul les divisions"""
        for i in range(len(self.calcul_list)):
            if self.calcul_list[i] == "/":
                if self.calcul_list[i+1] == "t":
                    self.calcul_list[i-1] = self.calcul_list[i-1] / self.t
                elif self.calcul_list[i-1] == "t":
                    self.calcul_list[i-1] = self.t / self.calcul_list[i+1]
                else:
                    self.calcul_list[i-1] = self.calcul_list[i-1] / self.calcul_list[i+1]
                del self.calcul_list[i:i+2]
                break
    

    def soustraction_addition(self):
        """calcul les soustractions et les additions"""
        for i in range(len(self.calcul_list)):
            if self.calcul_list[i] == "+":
                if self.calcul_list[i+1] == "t":
                    self.calcul_list[i-1] = self.calcul_list[i-1] + self.t
                elif self.calcul_list[i-1] == "t":
                    self.calcul_list[i-1] = self.t + self.calcul_list[i+1]
                else:
                    self.calcul_list[i-1] = self.calcul_list[i-1] + self.calcul_list[i+1]
                del self.calcul_list[i:i+2]
                break

            elif self.calcul_list[i] == "-":
                if self.calcul_list[i+1] == "t":
                    self.calcul_list[i-1] = self.calcul_list[i-1] - self.t
                elif self.calcul_list[i-1] == "t":
                    self.calcul_list[i-1] = self.t - self.calcul_list[i+1]
                else:
                    self.calcul_list[i-1] = self.calcul_list[i-1] - self.calcul_list[i+1]
                del self.calcul_list[i:i+2]
                break



    def cos_sin_exp(self):
        """calcul les cosinus, sinus et exponentielles"""
        if self.verif_func == ["c", "o", "s"]:
            self.cos = True
            self.sin = False
            self.exp = False
        elif self.verif_func == ["s", "i", "n"]:
            self.cos = False
            self.sin = True
            self.exp = False
        elif self.verif_func == ["e", "x", "p"]:
            self.cos = False
            self.sin = False
            self.exp = True
        else:
            self.cos = False
            self.sin = False
            self.exp = False


    def brackets(self):
        """calcul les fonctions dans les parenthèses"""
        for i in range(len(self.calcul_list)):
            if self.calcul_list[i] == "(":
                self.verif_func = self.calcul_list[i-3:i]
                self.calcul_list = self.calcul_list[i+1:]
                if self.brackets_number == 0:
                    self.start = i
                else:
                    self.start += i
                self.brackets_number += 1
                self.cos_sin_exp()
                self.brackets()
                break
            elif self.calcul_list[i] == ")":
                self.calcul_list = self.calcul_list[:i]
                self.end = i + self.start
                self.calcul(self.calcul_list)
                break


    def calcul(self, calcul_considered):
        """calcul le calcul"""
        self.calcul_list = calcul_considered
        while len(self.calcul_list) > 1:
            self.brackets()
            self.multiplication()
            self.division()
            self.soustraction_addition()

        if self.start != None and self.end != None:
            if self.cos:
                result = math.cos(self.calcul_list[0])
                self.calcul_list_total[self.start + self.brackets_number - 4] = result
                del self.calcul_list_total[self.start + self.brackets_number - 3 : self.end + 1 + self.brackets_number]
            elif self.sin:
                result = math.sin(self.calcul_list[0])
                self.calcul_list_total[self.start + self.brackets_number - 4] = result
                del self.calcul_list_total[self.start + self.brackets_number - 3 : self.end + 1 + self.brackets_number]
            elif self.exp:
                result = math.exp(self.calcul_list[0])
                self.calcul_list_total[self.start + self.brackets_number - 4] = result
                del self.calcul_list_total[self.start + self.brackets_number - 3 : self.end + 1 + self.brackets_number]
            else:
                result = self.calcul_list[0]
                self.calcul_list_total[self.start + self.brackets_number - 1] = result
                del self.calcul_list_total[self.start + self.brackets_number : self.end + 1 + self.brackets_number]
            self.start = None
            self.end = None
            self.brackets_number = 0
            self.calcul(self.calcul_list_total)
        
        
    def return_result(self):
        """retourne le résultat"""
        return self.calcul_list[0]