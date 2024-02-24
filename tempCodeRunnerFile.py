deplacement_effectue = False
        for point in self.points:
            if not self.satisfait(point):  # Si le point n'est pas satisfait
                espaces_vides = [(i, j) for i in range(self.taille) for j in range(self.taille) if self.grille[i][j] is None]
                if espaces_vides:  # S'il y a des espaces vides
                    i, j = random.choice(espaces_vides)  # Choisir un espace vide aléatoire
                    self.grille[i][j], self.grille[point.x][point.y] = point.type, None
                    point.x, point.y = i, j
                    deplacement_effectue = True
                    point.compte_moves += 1
        if deplacement_effectue is False:
            self.equilibre = True