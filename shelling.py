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
        self.tolerance = 0.1

    def initialiser_grille(self):
        for point in self.points:
            self.grille[point.x][point.y] = point.type

    def calculer_voisins(self, x, y):
        voisins = [(nx, ny) for nx in range(max(0, x - 1), min(x + 2, self.taille))
                   for ny in range(max(0, y - 1), min(y + 2, self.taille))
                   if not (nx == x and ny == y)]
        return voisins
    
    def satisfait(self,point):
        voisins = self.calculer_voisins(point.x, point.y)
        nb_voisins_meme_type = sum(1 for nx, ny in voisins if self.grille[nx][ny] == point.type)
        nb_voisins_autre_type = sum(1 for nx, ny in voisins if self.grille[nx][ny] != point.type and self.grille[nx][ny] is not None)
        total_voisins = nb_voisins_meme_type + nb_voisins_autre_type
        return nb_voisins_meme_type > nb_voisins_autre_type and nb_voisins_autre_type >self.tolerance*total_voisins
    
    def condition_deplacement(self,point,nx, ny):
        voisins = self.calculer_voisins(point.x, point.y)
        nb_voisins_meme_type = sum(1 for nx, ny in voisins if self.grille[nx][ny] == point.type)
        nb_voisins_autre_type = sum(1 for nx, ny in voisins if self.grille[nx][ny] != point.type and self.grille[nx][ny] is not None)

        nouveaux_voisins = self.calculer_voisins(nx, ny)
        nb_nouveaux_voisins_meme_type = sum(1 for vx, vy in nouveaux_voisins if self.grille[vx][vy] == point.type)
        nb_nouveaux_voisins_autre_type = sum(1 for vx, vy in nouveaux_voisins if self.grille[vx][vy] != point.type and self.grille[nx][ny] is not None)      
        total_nouveaux_voisins = nb_nouveaux_voisins_meme_type + nb_nouveaux_voisins_autre_type
        condition_deplacement = (nb_nouveaux_voisins_meme_type > nb_voisins_meme_type or nb_nouveaux_voisins_autre_type < nb_voisins_autre_type) and nb_voisins_autre_type >self.tolerance*total_nouveaux_voisins
        return condition_deplacement
    
  # Le point serait insatisfait dans toutes les positions vMoliputoisines
    def deplacer_points(self):
        deplacement_effectue = False
        tolerance = 0.3  # Par exemple, chaque point tolère jusqu'à 30% de voisins d'une autre couleur

        # Définir les directions possibles de déplacement
        directionsR = [(0, 1), (1, 0),(0, -1), (-1, 0)] #(0, -1), (-1, 0)
        directionsB = [(1, -1), (-1, 1),(1, 1), (-1, -1) ] #(1, 1), (-1, -1) 

        for point in self.points:
            if self.satisfait(point):
                continue  # Reste à sa position  # Passer au point suivant
            # Choisir les directions en fonction de la couleur du point
            directions = directionsB if point.type.startswith('B') else directionsR
            for dx, dy in directions:
                nx, ny = point.x + dx, point.y + dy
                # Vérifier si la nouvelle position est dans la grille et est vide
                if 0 <= nx < self.taille and 0 <= ny < self.taille and self.grille[nx][ny] is None:
                    # Calculer le taux de voisins du même type dans la nouvelle position
                    if  self.satisfait(point) is False and self.condition_deplacement(point,nx, ny):
                        self.grille[nx][ny], self.grille[point.x][point.y] = point.type, None
                        point.x, point.y = nx, ny
                        deplacement_effectue = True
                        break  # Arrêter de chercher une fois qu'un espace libre est trouvé
                    elif  self.satisfait(point) is False and self.condition_deplacement(point,nx, ny) is False and point.comptemoves < 4:
                        espaces_vides = [point for pt in self.points if self.grille[pt.x][pt.y] is None]
                        if len(espaces_vides) > 0:
                            pt = random.choice(espaces_vides)
                            self.grille[pt.x][pt.y], self.grille[point.x][point.y] = point.type, None
                            point.x, point.y = pt.x, pt.y
                            deplacement_effectue = True
                            point.comptemoves += 1
                            break  # Arrêter de chercher une fois qu'un espace libre est trouvé
        if not deplacement_effectue:
            self.equilibre = True

    
    def calculer_taux_satisfaction(self):
        # Par exemple, chaque point tolère jusqu'à 30% de voisins d'une autre couleur
        for point in self.points:
            if self.satisfait(point):
                self.nb_points_satisfaits += 1
        taux_satisfaction_moyen = self.nb_points_satisfaits*100 / len(self.points) if len(self.points) > 0 else 0
        return round(taux_satisfaction_moyen)




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

                self.canvas.create_rectangle(j * self.taillePixel, i * self.taillePixel, (j + 1) * self.taillePixel, (i + 1) * self.taillePixel, fill=couleur)

        taux_satisfaction = self.grille.calculer_taux_satisfaction()
        info_text = f"Taux de Satisfaction: {taux_satisfaction}%"
        self.label.config(text=info_text)

        if self.grille.equilibre:
            msg.showinfo("Résultat", "Équilibre ségrégationniste atteint.")
        else:
            self.after(10, self.mise_a_jour_grille)  # Planifie la prochaine mise à jour après 30 ms


def main():
    app = Application()
    app.mainloop()

if __name__ == "__main__":
    main()