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