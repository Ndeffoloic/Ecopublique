import random
import tkinter as tk
import tkinter.messagebox as msg

import numpy as np


class Point:
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type
        self.directions_visitees = []


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
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
        for point in self.points:
            voisins = self.calculer_voisins(point.x, point.y)
            nb_voisins_meme_type = sum(1 for nx, ny in voisins if self.grille[nx][ny] == point.type)
            nb_voisins_autre_type = sum(1 for nx, ny in voisins if self.grille[nx][ny] != point.type and self.grille[nx][ny] is not None)

            if nb_voisins_meme_type >= nb_voisins_autre_type:
                continue  # Reste à sa position

            espaces_vides = [(i, j) for i in range(self.taille) for j in range(self.taille) if self.grille[i][j] is None]
            espaces_vides_dir = [pos for pos in espaces_vides if (pos[0] - point.x, pos[1] - point.y) not in point.directions_visitees]
            if espaces_vides_dir:  # S'il y a des espaces vides
                # Calculer la distance entre le point et chaque espace vide
                distances = [(i, j, (i - point.x)**2 + (j - point.y)**2) for i, j in espaces_vides_dir]
                # Choisir l'espace le plus proche
                i, j, _ = min(distances, key=lambda x: x[2])
                direction_prise = (i - point.x, j - point.y)
                self.grille[i][j], self.grille[point.x][point.y] = point.type, None
                point.x, point.y = i, j
                point.directions_visitees.append(direction_prise)  # Ajouter la direction prise à la liste des directions visitées
                deplacement_effectue = True

        if not deplacement_effectue:
            self.equilibre = True

    def grille_est_stable(self):
        return self.equilibre
    def calculer_taux_segregation(self):
        nb_points_segreges = 0
        for point in self.points:
            voisins = self.calculer_voisins(point.x, point.y)
            nb_voisins_meme_type = sum(1 for nx, ny in voisins if self.grille[nx][ny] == point.type)
            nb_voisins_autre_type = sum(1 for nx, ny in voisins if self.grille[nx][ny] != point.type and self.grille[nx][ny] is not None)
            if nb_voisins_meme_type > nb_voisins_autre_type:
                nb_points_segreges += 1

        taux_segregation = nb_points_segreges*100 / len(self.points) 

        return round(taux_segregation, 2)

    def calculer_taux_satisfaction(self):
        taux_satisfaction_total = 0
        for point in self.points:
            voisins = self.calculer_voisins(point.x, point.y)
            nb_voisins_meme_type = sum(1 for nx, ny in voisins if self.grille[nx][ny] == point.type)
            nb_voisins_vide = sum(1 for nx, ny in voisins if self.grille[nx][ny] is None)
            taux_satisfaction_total += (nb_voisins_meme_type + nb_voisins_vide) / len(voisins)
        taux_satisfaction_moyen = taux_satisfaction_total / len(self.points) * 100
        return  round(taux_satisfaction_moyen, 2)

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