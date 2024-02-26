class SudokuSolver:
    def __init__(self, grid, domain):
        self.grid = grid
        self.domain = domain

    def print_grid(self):
        for row in self.grid:
            print(" ".join(str(num) for num in row))

    def is_consistent(self, row, col, num):
        # Check row and column constraints
        for i in range(9):
            if self.grid[row][i] == num or self.grid[i][col] == num:
                return False

        # Check 3x3 box constraint
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if self.grid[i][j] == num:
                    return False

        # Check the constraint that certain cells must contain even numbers
        if self.grid[row][col] == -1 and num % 2 != 0:
            return False

        return True

    def find_empty_cell(self):
        for row in range(9):
            for col in range(9):
                if self.grid[row][col] == 0 or self.grid[row][col] == -1:
                    return row, col
        return None

    def mrv(self):
        min_remaining_values = 10
        min_cell = None
        for row in range(9):
            for col in range(9):
                if self.grid[row][col] == 0 or self.grid[row][col] == -1:
                    remaining_values = len([num for num in self.domain if self.is_consistent(row, col, num)])
                    if remaining_values < min_remaining_values:
                        min_remaining_values = remaining_values
                        min_cell = (row, col)
        return min_cell

    def forward_checking(self):
        if all(all(cell != 0 and cell != -1 for cell in row) for row in self.grid):
            return True

        cell = self.find_empty_cell()
        if cell is None:
            return True

        row, col = cell

        # row, col = self.mrv()

        if self.grid[row][col] == -1:
            for num in range(2, len(self.domain), 2):
                if self.is_consistent(row, col, num):
                    self.grid[row][col] = num
                    if self.forward_checking():
                        return True
                self.grid[row][col] = -1
        else:
            for num in self.domain:
                if self.is_consistent(row, col, num):
                    self.grid[row][col] = num
                    if self.forward_checking():
                        return True
                self.grid[row][col] = 0

        return False

    def arc_c(self):
        queue = [(i, j) for i in range(9) for j in range(9) if self.grid[i][j] == 0 or self.grid[i][j] == -1]

        while queue:
            row, col = queue.pop(0)
            for value in self.domain:
                if self.is_consistent(row, col, value):
                    self.grid[row][col] = value
                    if self.revise(row, col):
                        return False
                    queue.extend((row, c) for c in range(9) if c != col)
                    queue.extend((r, col) for r in range(9) if r != row)
                    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
                    for r in range(start_row, start_row + 3):
                        for c in range(start_col, start_col + 3):
                            if r != row and c != col:
                                queue.append((r, c))
        return True

    def revise(self, row, col):
        for i in range(9):
            if i != col and self.grid[row][i] == 0:
                if not any(self.is_consistent(row, i, val) for val in self.domain):
                    return True
            if i != row and self.grid[i][col] == 0:
                if not any(self.is_consistent(i, col, val) for val in self.domain):
                    return True
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if i != row and j != col and self.grid[i][j] == 0:
                    if not any(self.is_consistent(i, j, val) for val in self.domain):
                        return True
        return False

    def solve(self):
        if self.forward_checking() and self.arc_c():
            print("Solution found:")
            self.print_grid()
        else:
            print("No solution found.")
