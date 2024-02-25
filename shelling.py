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
        self.compte_moves = 0
        self.etat = [] # stocke une coordonnée en clé et la satisfaction en valeur
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
    
    def satisfait(self,point):
        voisins = self.calculer_voisins(point.x, point.y)
        nb_voisins_meme_type = sum(1 for nx, ny in voisins if self.grille[nx][ny] == point.type)

        return nb_voisins_meme_type >= len(voisins)/2
    
    def pseudo_satisfait(self, point):
        if point.etat.count(True) > 2:
            return True
        else: 
            return False
            
        
    def deplacer_points(self):
        deplacement_effectue = False
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
        for point in self.points:
            point.etat.append(self.satisfait(point))
            if not self.satisfait(point):  # Si le point n'est pas satisfait
                espaces_vides = [(i, j) for i in range(self.taille) for j in range(self.taille) if self.grille[i][j] is None]
                # Filtrer les espaces vides pour exclure les directions déjà prises
                espaces_vides_dir = [pos for pos in espaces_vides if (pos[0] - point.x, pos[1] - point.y) not in point.directions_visitees]
                if espaces_vides_dir:  # S'il y a des espaces vides
                    # Choisir une cellule vide au hasard
                    i, j = random.choice(espaces_vides_dir)

                    self.grille[i][j], self.grille[point.x][point.y] = point.type, None
                    point.x, point.y = i, j
                    point.directions_visitees.append((i - point.x, j - point.y))  # Ajouter la nouvelle direction à la liste des directions visitées
                    deplacement_effectue = True
                    point.compte_moves += 1
        if not deplacement_effectue:
            self.equilibre = True

    
    def calculer_taux_satisfaction(self):
        nb_points_satisfaits += 0.05
        # Par exemple, chaque point tolère jusqu'à 30% de voisins d'une autre couleur
        for point in self.points:
            if self.satisfait(point):
                nb_points_satisfaits += 1
        taux_satisfaction_moyen = nb_points_satisfaits*100 / len(self.points) 
        return round(taux_satisfaction_moyen,2)

    def calculer_taux_segregation(self):
        nb_points_segreges += 0.05
        for point in self.points:
            voisins = self.calculer_voisins(point.x, point.y)
            nb_voisins_meme_type = sum(1 for nx, ny in voisins if self.grille[nx][ny] == point.type)
            nb_voisins_autre_type = sum(1 for nx, ny in voisins if self.grille[nx][ny] != point.type and self.grille[nx][ny] is not None)
            if nb_voisins_meme_type > nb_voisins_autre_type:
                nb_points_segreges += 1

        taux_segregation = nb_points_segreges*100 / len(self.points) 

        return round(taux_segregation, 2)

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Schelling's Segregation Model")
        self.taillePixel = 10

        self.label_taille = tk.Label(self, text="Entrez la taille de la grille :")
        self.label_taille.pack()
        self.entry_taille = tk.Entry(self)
        self.entry_taille.pack()

        self.label_bleus = tk.Label(self, text="Entrez le nombre de points bleus :")
        self.label_bleus.pack()
        self.entry_bleus = tk.Entry(self)
        self.entry_bleus.pack()

        self.label_rouges = tk.Label(self, text="Entrez le nombre de points rouges :")
        self.label_rouges.pack()
        self.entry_rouges = tk.Entry(self)
        self.entry_rouges.pack()

        self.button_start = tk.Button(self, text="Start", command=self.start)
        self.button_start.pack()

        self.canvas = tk.Canvas(self, bg="white")
        self.canvas.pack()

        self.label = tk.Label(self, text="")
        self.label.pack()

    def start(self):
        taille = int(self.entry_taille.get())
        nb_points_bleus = int(self.entry_bleus.get())
        nb_points_rouges = int(self.entry_rouges.get())

        self.canvas.config(width=self.taillePixel*taille, height=self.taillePixel*taille)

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

        taux_segregation = self.grille.calculer_taux_segregation()
        taux_satisfaction = self.grille.calculer_taux_satisfaction()
        #print(f"Taux de Ségrégation: {taux_segregation}%\t\tTaux de Satisfaction: {taux_satisfaction}%")
        info_text = f"Taux de Ségrégation: {taux_segregation}%\t\tTaux de Satisfaction: {taux_satisfaction}%"
        self.label.config(text=info_text)
        if self.grille.equilibre:
            msg.showinfo("Résultat", "Équilibre ségrégationniste atteint.")
        else:
            self.after(100, self.mise_a_jour_grille)  # Planifie la prochaine mise à jour après 30 ms


def main():
    app = Application()
    app.mainloop()

if __name__ == "__main__":
    main()