import random
import tkinter as tk

import numpy as np


class Point:
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type


class Grille:
    def __init__(self, taille, points):
        self.taille = taille
        self.points = points
        self.grille = np.empty((taille, taille), dtype=object)
        self.equilibre = False

    def initialiser_grille(self):
        for point in self.points:
            self.grille[point.x][point.y] = point.type

    def calculer_voisins(self, x, y):
        voisins = [(nx, ny) for nx in range(max(0, x - 1), min(x + 2, self.taille))
                   for ny in range(max(0, y - 1), min(y + 2, self.taille))
                   if not (nx == x and ny == y)]
        return voisins

    def deplacer_points(self):
        deplacement_effectue = False
        for point in self.points:
            voisins = self.calculer_voisins(point.x, point.y)
            nb_voisins_meme_type = sum(1 for nx, ny in voisins if self.grille[nx][ny] == point.type)
            nb_voisins_autre_type = sum(1 for nx, ny in voisins if self.grille[nx][ny] != point.type and self.grille[nx][ny] is not None)

            if nb_voisins_meme_type >= nb_voisins_autre_type:
                continue  # Reste à sa position

            if point.type.startswith('B') and point.x > 0 and point.y < self.taille - 1 and self.grille[point.x - 1][
                point.y + 1] is None:
                self.grille[point.x - 1][point.y + 1], self.grille[point.x][point.y] = point.type, None
                point.x, point.y = point.x - 1, point.y + 1
                deplacement_effectue = True
            elif point.type.startswith('R') and point.x < self.taille - 1 and point.y > 0 and self.grille[point.x + 1][
                point.y - 1] is None:
                self.grille[point.x + 1][point.y - 1], self.grille[point.x][point.y] = point.type, None
                point.x, point.y = point.x + 1, point.y - 1
                deplacement_effectue = True
            else:  # Si le point ne peut pas se déplacer vers le coin cible, il se déplace aléatoirement vers une position libre
                positions_libres = [(nx, ny) for nx in range(self.taille) for ny in range(self.taille) if
                                    self.grille[nx][ny] is None]
                if positions_libres:
                    nx, ny = random.choice(positions_libres)
                    self.grille[nx][ny], self.grille[point.x][point.y] = point.type, None
                    point.x, point.y = nx, ny
                    deplacement_effectue = True

        if not deplacement_effectue:
            self.equilibre = True

    def grille_est_stable(self):
        return self.equilibre


def afficher_grille_tkinter(grille):
    fenetre = tk.Tk()
    fenetre.title("Grille de points")
    
    canvas = tk.Canvas(fenetre, width=400, height=400)
    canvas.pack()
    
    for i in range(grille.taille):
        for j in range(grille.taille):
            if grille.grille[i][j] is None:
                couleur = "white"
            else:
                if grille.grille[i][j].startswith('B'):
                    couleur = "blue"
                else:
                    couleur = "red"
            
            canvas.create_rectangle(j * 40, i * 40, (j + 1) * 40, (i + 1) * 40, fill=couleur)
    
    fenetre.mainloop()


def main():
    taille = int(input("Entrez la taille de la grille : "))
    nb_points_bleus = int(input("Entrez le nombre de points bleus : "))
    nb_points_rouges = int(input("Entrez le nombre de points rouges : "))

    indices = list(range(taille * taille))
    random.shuffle(indices)

    points = []
    for i in range(nb_points_bleus):
        x, y = divmod(indices[i], taille)
        points.append(Point(x, y, f"B{i + 1}"))

    for i in range(nb_points_rouges):
        x, y = divmod(indices[nb_points_bleus + i], taille)
        points.append(Point(x, y, f"R{i + 1}"))

    grille = Grille(taille, points)
    grille.initialiser_grille()
    afficher_grille_tkinter(grille)

    while grille.equilibre is False:
        action = input("Appuyez sur Enter pour continuer ou 'esc' pour sortir : ")
        if action.lower() == 'esc':
            return
        grille.deplacer_points()
        afficher_grille_tkinter(grille)

    if grille.grille_est_stable():
        print("Équilibre ségrégationniste atteint.")


if __name__ == "__main__":
    main()