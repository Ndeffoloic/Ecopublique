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
        tolerance = 0.3  # Par exemple, chaque point tolère jusqu'à 30% de voisins d'une autre couleur
        iteration = 0
        for point in self.points:
            voisins = self.calculer_voisins(point.x, point.y)
            nb_voisins_meme_type = sum(1 for nx, ny in voisins if self.grille[nx][ny] == point.type)
            nb_voisins_autre_type = sum(1 for nx, ny in voisins if self.grille[nx][ny] != point.type and self.grille[nx][ny] is not None)
            #nb_espaces_vides = sum(1 for nx, ny in voisins if self.grille[nx][ny] is None)
            
            if nb_voisins_meme_type > nb_voisins_autre_type:
                continue  # Reste à sa position

            # Définir les directions possibles de déplacement
            directionsR = [(0, 1), (1, 0)] #(0, -1), (-1, 0)
            directionsB = [(1, -1), (-1, 1)] #(1, 1), (-1, -1) 
            directions = directionsB if point.type.startswith('B') else directionsR
            for dx, dy in directions:
                nx, ny = point.x + dx, point.y + dy
                # Vérifier si la nouvelle position est dans la grille et est vide
                if 0 <= nx < self.taille and 0 <= ny < self.taille and self.grille[nx][ny] is None:
                    self.grille[nx][ny], self.grille[point.x][point.y] = point.type, None
                    point.x, point.y = nx, ny
                    deplacement_effectue = True
                    break  # Arrêter de chercher une fois qu'un espace libre est trouvé

        if not deplacement_effectue:
            self.equilibre = True

    def grille_est_stable(self):
        return self.equilibre
    
    def calculer_taux_segregation(self):
        nb_points_bleus = sum(1 for point in self.points if point.type.startswith('B'))
        nb_points_rouges = sum(1 for point in self.points if point.type.startswith('R'))
        taux_segregation = abs(nb_points_bleus - nb_points_rouges) / abs(nb_points_bleus + nb_points_rouges) * 100
        return round(taux_segregation, 2)

    def calculer_taux_satisfaction(self):
        tolerance = 0.3  # Par exemple, chaque point tolère jusqu'à 30% de voisins d'une autre couleur
        nb_points_satisfaits = 0
        for point in self.points:
            voisins = self.calculer_voisins(point.x, point.y)
            nb_voisins_meme_type = sum(1 for nx, ny in voisins if self.grille[nx][ny] == point.type)
            nb_voisins_autre_type = sum(1 for nx, ny in voisins if self.grille[nx][ny] != point.type and self.grille[nx][ny] is not None)
            total_voisins = nb_voisins_meme_type + nb_voisins_autre_type
            taux_voisins_meme_type = nb_voisins_meme_type / total_voisins if total_voisins > 0 else 0
            if taux_voisins_meme_type >= tolerance:
                nb_points_satisfaits += 1
        taux_satisfaction_moyen = nb_points_satisfaits / len(self.points) * 100 if len(self.points) > 0 else 0
        return round(taux_satisfaction_moyen, 2)


import tkinter.simpledialog as sd


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Schelling's Segregation Model")

        taille = sd.askinteger("Input", "Entrez la taille de la grille :")
        nb_points_bleus = sd.askinteger("Input", "Entrez le nombre de points bleus :")
        nb_points_rouges = sd.askinteger("Input", "Entrez le nombre de points rouges :")

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
            self.after(100, self.mise_a_jour_grille)  # Planifie la prochaine mise à jour après 30 ms


def main():
    app = Application()
    app.mainloop()

if __name__ == "__main__":
    main()