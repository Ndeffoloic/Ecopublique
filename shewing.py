import random
import tkinter as tk
import tkinter.messagebox as msg

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
    def calculer_taux_segregation(self):
        nb_points_bleus = sum(1 for point in self.points if point.type.startswith('B'))
        nb_points_rouges = len(self.points) - nb_points_bleus
        taux_segregation = abs(nb_points_bleus - nb_points_rouges) / len(self.points) * 100
        return taux_segregation

    def calculer_taux_satisfaction(self):
        taux_satisfaction_total = 0
        for point in self.points:
            voisins = self.calculer_voisins(point.x, point.y)
            nb_voisins_meme_type = sum(1 for nx, ny in voisins if self.grille[nx][ny] == point.type)
            nb_voisins_vide = sum(1 for nx, ny in voisins if self.grille[nx][ny] is None)
            taux_satisfaction_total += (nb_voisins_meme_type + nb_voisins_vide) / len(voisins)
        taux_satisfaction_moyen = taux_satisfaction_total / len(self.points) * 100
        return taux_satisfaction_moyen

class Application(tk.Tk):
    def __init__(self, taille, nb_points_bleus, nb_points_rouges):
        super().__init__()
        self.title("Schelling's Segregation Model")
        self.canvas = tk.Canvas(self, width=40*taille, height=40*taille, bg="white")
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
        self.canvas.delete("all")  # Efface tous les éléments du canvas

        for i in range(self.grille.taille):
            for j in range(self.grille.taille):
                if self.grille.grille[i][j] is None:
                    couleur = "white"
                else:
                    if self.grille.grille[i][j].startswith('B'):
                        couleur = "blue"
                    else:
                        couleur = "red"

                self.canvas.create_rectangle(j * 40, i * 40, (j + 1) * 40, (i + 1) * 40, fill=couleur)

        taux_segregation = self.grille.calculer_taux_segregation()
        taux_satisfaction = self.grille.calculer_taux_satisfaction()
        info_text = f"Taux de Ségrégation: {taux_segregation}%\nTaux de Satisfaction: {taux_satisfaction}%"
        self.label.config(text=info_text)

        if self.grille.grille_est_stable():
            msg.showinfo("Résultat", "Équilibre ségrégationniste atteint.")
        else:
            self.after(1000, self.mise_a_jour_grille)  # Planifie la prochaine mise à jour après 30 ms


def main():
    taille = int(input("Entrez la taille de la grille : "))
    nb_points_bleus = int(input("Entrez le nombre de points bleus : "))
    nb_points_rouges = int(input("Entrez le nombre de points rouges : "))

    app = Application(taille, nb_points_bleus, nb_points_rouges)
    app.mainloop()


if __name__ == "__main__":
    main()