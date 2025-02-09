class Ship:
    def __init__(self, size):
        self.size = size
        self.grid = [['.' for _ in range(size)] for _ in range(size)]  # Everything is open

    def print_grid(self):
        for row in self.grid:
            print(" ".join(row))
