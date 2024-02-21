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
            self.after(1000, self.mise_a_jour_grille)  # Planifie la prochaine mise à jour après 30 ms