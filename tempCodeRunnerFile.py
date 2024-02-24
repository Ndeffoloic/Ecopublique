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
