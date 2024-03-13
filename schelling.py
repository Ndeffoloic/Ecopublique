
import tkinter as tk
import tkinter.messagebox as msg
import tkinter.simpledialog as sd

import numpy as np


class Grille:
    def __init__(self, taille, points_bleus, points_rouges, ratio_similarite):
        self.taille = taille
        self.points_bleus = points_bleus
        self.points_rouges = points_rouges
        self.ratio_similarite = ratio_similarite
        self.grille = np.zeros((self.taille, self.taille), dtype=object)
        self.equilibre = False
        self.cases_vides =  1 - ((self.points_bleus + self.points_rouges) / (taille * taille))

    def initialiser_grille(self):
        p_vide = self.cases_vides
        p_bleu = self.points_bleus / (self.taille * self.taille)
        p_rouge = self.points_rouges / (self.taille * self.taille)

        self.grille = np.random.choice([0, 1, 2], (self.taille, self.taille), p=[p_vide, p_bleu, p_rouge])  # 0: vide, 1: bleu, 2: rouge

    def calculer_voisins(self, x, y):
        voisins = [(nx, ny) for nx in range(max(0, x - 1), min(x + 2, self.taille))
                   for ny in range(max(0, y - 1), min(y + 2, self.taille))
                   if not (nx == x and ny == y)]
        return voisins
    
    def satisfait(self, x,y):
        current_agent = self.grille[x, y]
        count_similar = 0
        count_different = 0
        voisins = self.calculer_voisins(x, y)
        for nx, ny in voisins:
            if current_agent == self.grille[nx, ny]:  # Utilisez (nx, ny) comme indice pour self.grille
                count_similar += 1
            elif current_agent != self.grille[nx, ny] and self.grille[nx, ny] != 0:  # Utilisez (nx, ny) comme indice pour self.grille
                count_different += 1
        if count_similar + count_different == 0:
            return True
        else:
            return (count_similar / (count_similar + count_different)) >= self.ratio_similarite

            
        
    def deplacer_points(self):
        deplacement_effectue = False

        for j in range(self.taille*self.taille):
            x, y = np.unravel_index(j, (self.taille, self.taille))
            if self.grille[x, y] == 0 :
                continue
            if not self.satisfait(x,y):  # Si le point n'est pas satisfait
                espaces_vides = np.argwhere(self.grille == 0)  # Trouver les cellules vides

                if len(espaces_vides) > 0:  # S'il y a des espaces vides
                    # Choisir une cellule vide au hasard
                    i, j = espaces_vides[np.random.choice(len(espaces_vides))]

                    # Déplacer le point à la cellule vide
                    self.grille[i, j], self.grille[x, y] = self.grille[x, y], 0
                    deplacement_effectue = True

        if not deplacement_effectue:
            self.equilibre = True


    
    def calculer_taux_satisfaction(self):
        nb_points_satisfaits = 0
        for i in range(self.taille):
            for j in range(self.taille):
                if self.grille[i, j] != 0 and self.satisfait(i, j):
                    nb_points_satisfaits += 1
        taux_satisfaction = nb_points_satisfaits*100 / (self.points_bleus + self.points_rouges) if (self.points_bleus + self.points_rouges) > 0 else 0
        return round(taux_satisfaction, 2) if taux_satisfaction < 100 else 100.00
    
    def calculer_taux_segregation(self):
        nb_points_segreges = 0
        for i in range(self.taille):
            for j in range (self.taille):
                if self.grille[i][j] != 0 :
                    voisins = self.calculer_voisins(i,j)
                    nb_voisins_meme_type = sum(1 for nx, ny in voisins if self.grille[nx][ny] == self.grille[i][j])
                    nb_voisins_autre_type = sum(1 for nx, ny in voisins if self.grille[nx][ny] != self.grille[i][j])
                    if nb_voisins_meme_type > nb_voisins_autre_type:
                        nb_points_segreges += 1

        taux_segregation = nb_points_segreges*100 / (self.points_bleus + self.points_rouges) if (self.points_bleus + self.points_rouges) > 0 else 0

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

        self.label_similarite = tk.Label(self, text="Entrez le ratio de similarité :")
        self.label_similarite.pack()
        self.entry_similarite = tk.Entry(self)
        self.entry_similarite.pack()
        
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
        similarite = float(self.entry_similarite.get())

        self.canvas.config(width=self.taillePixel*taille, height=self.taillePixel*taille)

        self.schelling = Grille(taille, nb_points_bleus, nb_points_rouges, similarite)
        self.schelling.initialiser_grille()

        self.mise_a_jour_grille()



    def mise_a_jour_grille(self):
        self.canvas.delete("all")  # Efface tous les éléments du canvas
        self.label.config(text=f"Taux de segregation : {self.schelling.calculer_taux_segregation()}\t\t taux de satisfaction : {self.schelling.calculer_taux_satisfaction()}")
        self.after(100, self.mise_a_jour_grille)  # Planifie la prochaine mise à jour après 100 ms

        for i in range(self.schelling.taille):
            for j in range(self.schelling.taille):
                color = "blue" if self.schelling.grille[i, j] == 1 else "red" if self.schelling.grille[i, j] == 2 else "white"
                self.canvas.create_rectangle(j*self.taillePixel, i*self.taillePixel, j*self.taillePixel+self.taillePixel, i*self.taillePixel+self.taillePixel, fill=color)
        if not self.schelling.equilibre:
            self.schelling.deplacer_points()
            

def main():
    app = Application()
    app.mainloop()

if __name__ == "__main__":
    main()