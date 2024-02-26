import random
import tkinter as tk

import numpy as np


class Schelling:
    def __init__(self, width, height, empty_ratio, similarity_threshold, n_iterations, file_name):
        self.width = width
        self.height = height
        self.empty_ratio = empty_ratio
        self.similarity_threshold = similarity_threshold
        self.n_iterations = n_iterations
        self.agents = np.zeros((self.width, self.height))
        self.file_name = file_name

    def populate(self):
        self.agents = np.random.choice([0, 1], size=(self.width, self.height))
        self.agents[self.agents == 0] = -1
        empty_index = np.random.choice(self.width*self.height, int(self.width*self.height*self.empty_ratio), replace=False)
        self.agents.flat[empty_index] = 0
        
    def get_neighbours_index(self, x, y):
        indexes = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nx, ny = x + dx, y + dy
                if (nx >= 0 and nx < self.width and ny >= 0 and ny < self.height) and (nx != x or ny != y):
                    indexes.append((nx, ny))
        return indexes

    def is_unsatisfied(self, x, y):
        current_agent = self.agents[x, y]
        count_similar = 0
        count_different = 0
        neighbours_index = self.get_neighbours_index(x, y)
        for i in neighbours_index:
            if current_agent == self.agents[i]:  # Utilisez i comme indice pour self.agents
                count_similar += 1
            elif current_agent == -self.agents[i]:  # Utilisez i comme indice pour self.agents
                count_different += 1
        if count_similar + count_similar == 0:
            return True
        else:
            return (count_similar / (count_similar + count_different)) < self.similarity_threshold
    def segregation_rate(self):
        count_segregated = 0
        count_agents = 0
        for i in range(self.width):
            for j in range(self.height):
                if self.agents[i, j] != 0:
                    count_agents += 1
                    if not self.is_unsatisfied(i, j):
                        count_segregated += 1
        return count_segregated / count_agents if count_agents > 0 else 0

    def satisfaction_rate(self):
        count_satisfied = 0
        count_agents = 0
        for i in range(self.width):
            for j in range(self.height):
                if self.agents[i, j] != 0:
                    count_agents += 1
                    if not self.is_unsatisfied(i, j):
                        count_satisfied += 1
        return count_satisfied / count_agents if count_agents > 0 else 0

    
    def update(self):
        n_changes = 0
        for j in range(self.width*self.height):
            x, y = np.unravel_index(j, (self.width, self.height))
            if self.agents[x, y] == 0:
                continue
            if self.is_unsatisfied(x, y):
                self.move_to_empty(x, y)
                n_changes += 1
        print(f"Iteration, changed {n_changes}")
        print(f"Segregation rate: {self.segregation_rate()}")
        print(f"Satisfaction rate: {self.satisfaction_rate()}")
        if n_changes == 0:
            print("System stabilized")
            return False
        return True

    def move_to_empty(self, x, y):
        current_agent = self.agents[x, y]
        empty_houses = np.where(self.agents == 0)
        index_to_move = np.random.choice(len(empty_houses[0]))
        self.agents[empty_houses[0][index_to_move], empty_houses[1][index_to_move]] = current_agent
        self.agents[x, y] = 0
        
    def count_agents(self):
        count_blue = np.count_nonzero(self.agents == -1)
        count_red = np.count_nonzero(self.agents == 1)
        return count_blue, count_red
class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Schelling's Model")
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

        empty_ratio = 1 - ((nb_points_bleus + nb_points_rouges) / (taille * taille))
        self.schelling = Schelling(taille, taille, empty_ratio, similarite, 1000, "schelling.npy")
        self.schelling.populate()

        self.update()

    def update(self):
        self.canvas.delete("all")  # Efface tous les éléments du canvas
        for i in range(self.schelling.width):
            for j in range(self.schelling.height):
                color = "blue" if self.schelling.agents[i, j] == -1 else "red" if self.schelling.agents[i, j] == 1 else "white"
                self.canvas.create_rectangle(j*self.taillePixel, i*self.taillePixel, j*self.taillePixel+self.taillePixel, i*self.taillePixel+self.taillePixel, fill=color)
        if self.schelling.update():
            self.label.config(text=f"Segregation rate: {self.schelling.segregation_rate()}\nSatisfaction rate: {self.schelling.satisfaction_rate()}")
            self.after(100, self.update)  # Planifie la prochaine mise à jour après 100 ms

def main():
    app = Application()
    app.mainloop()



if __name__ == "__main__":
    main()
