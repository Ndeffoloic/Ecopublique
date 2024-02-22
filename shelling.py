import random
import tkinter as tk
import tkinter.messagebox as msg
import tkinter.simpledialog as sd

import numpy as np


class Point:
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type
        self.comptemoves = 0



class Grille:
    def __init__(self, taille, points):
        self.taille = taille
        self.points = points
        self.grille = np.empty((taille, taille), dtype=object)
        self.equilibre = False
        self.nb_points_satisfaits = 0

    def initialiser_grille(self):
        for point in self.points:
            self.grille[point.x][point.y] = point.type

    def calculer_voisins(self, x, y):
        voisins = [(nx, ny) for nx in range(max(0, x - 1), min(x + 2, self.taille))
                   for ny in range(max(0, y - 1), min(y + 2, self.taille))
                   if not (nx == x and ny == y)]
        return voisins
    
    def satisfait(self, point):
        voisins = self.calculer_voisins(point.x, point.y)
        nb_voisins_meme_type = sum(1 for nx, ny in voisins if self.grille[nx][ny] == point.type)
        nb_voisins_autre_type = sum(1 for nx, ny in voisins if self.grille[nx][ny] != point.type and self.grille[nx][ny] is not None)
        nb_espace_vide = sum(1 for nx, ny in voisins if self.grille[nx][ny] is None)
        # Ajoutez cette ligne pour vérifier si un point a des voisins

        return (nb_voisins_meme_type > 3 or nb_espace_vide > nb_voisins_meme_type>=nb_voisins_autre_type)

  # Le point serait insatisfait dans toutes les positions vMoliputoisines
    def deplacer_points(self):
        deplacement_effectue = False

        for point in self.points:
            if not self.satisfait(point):  # Si le point n'est pas satisfait
                espaces_vides = [(i, j) for i in range(self.taille) for j in range(self.taille) if self.grille[i][j] is None]
                if espaces_vides:  # S'il y a des espaces vides
                    i, j = random.choice(espaces_vides)  # Choisir un espace vide aléatoire
                    self.grille[i][j], self.grille[point.x][point.y] = point.type, None
                    point.x, point.y = i, j
                    deplacement_effectue = True
        if not deplacement_effectue:
            self.equilibre = True


    def calculer_taux_satisfaction(self):
        self.nb_points_satisfaits = 0  # Ajoutez cette ligne
        for point in self.points:
            if self.satisfait(point):
                self.nb_points_satisfaits += 1
        taux_satisfaction_moyen = self.nb_points_satisfaits*100 / len(self.points) if len(self.points) > 0 else 49.00
        return round(taux_satisfaction_moyen,2)





class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Schelling's Segregation Model")
        self.taillePixel = 10
        taille = sd.askinteger("Input", "Entrez la taille de la grille :")
        nb_points_bleus = sd.askinteger("Input", "Entrez le nombre de points bleus :")
        nb_points_rouges = sd.askinteger("Input", "Entrez le nombre de points rouges :")

        self.canvas = tk.Canvas(self, width=self.taillePixel*taille, height=self.taillePixel*taille, bg="white")
        self.canvas.pack()

        indices = list(range(taille * taille))
        random.shuffle(indices)

        points = []
        for i in range(nb_points_bleus):
            x, y = divmod(indices[i], taille)
            points.append(Point(x, y, f"B{i + 1}"))

        for i in range(nb_points_rouges):
            x, y = divmod(indices[nb_points_bleus + i], taille)
            points.append(Point(x, y, f"R{i + 1}"))

        self.grille = Grille(taille, points)
        self.grille.initialiser_grille()

        self.label = tk.Label(self, text="")
        self.label.pack()

        self.mise_a_jour_grille()

    def mise_a_jour_grille(self):
        self.grille.deplacer_points()
        self.canvas.delete("all")  # Efface tous les Ã©lÃ©ments du canvas

        for i in range(self.grille.taille):
            for j in range(self.grille.taille):
                if self.grille.grille[i][j] is None:
                    couleur = "white"
                else:
                    if self.grille.grille[i][j].startswith('B'):
                        couleur = "blue"
                    else:
                        couleur = "red"

                self.canvas.create_rectangle(j * self.taillePixel, i * self.taillePixel, (j + 1) * self.taillePixel, (i + 1) * self.taillePixel, fill=couleur)

        taux_satisfaction = self.grille.calculer_taux_satisfaction()
        info_text = f"Taux de Satisfaction: {taux_satisfaction}%"
        self.label.config(text=info_text)

        if self.grille.equilibre:
            msg.showinfo("RÃ©sultat", "équilibre ségrégationniste atteint.")
        else:
            self.after(10, self.mise_a_jour_grille)  # Planifie la prochaine mise Ã  jour aprÃ¨s 30 ms


def main():
    app = Application()
    app.mainloop()

if __name__ == "__main__":
    main()