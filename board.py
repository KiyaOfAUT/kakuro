import numpy as np


class Board:
    def __init__(self, size, closed_cells, rule_cells):
        self.rules = rule_cells
        self.closed = closed_cells
        self.size = size
        hold_matrix = [[0 for _ in range(size)] for _ in range(size)]
        self.num_matrix = np.array(hold_matrix)
        for (i, j, k, z) in rule_cells:
            self.num_matrix[i][j] -= 1
        for (i, j) in closed_cells:
            self.num_matrix[i][j] = -3

    def win(self):
        if not self.constraint_satisfied():
            return False
        for (i, j, k, t) in self.rules:
            sum_ = 0
            if t == 1:
                d = 1
                if j + d < self.size:
                    while self.num_matrix[i][j + d] >= 0:
                        hold_num = self.num_matrix[i][j + d]
                        if hold_num == 0:
                            return False
                        sum_ += hold_num
                        d += 1
                        if j + d == self.size:
                            break
            if t == 2:
                d = 1
                if i + d < self.size:
                    while self.num_matrix[i + d][j] >= 0:
                        hold_num = self.num_matrix[i + d][j]
                        if hold_num == 0:
                            return False
                        sum_ += hold_num
                        d += 1
                        if i + d == self.size:
                            break
            if sum_ == k:
                pass
            else:
                return False
        return True

    def constraint_satisfied(self):
        count = 0
        for (i, j, k, t) in self.rules:
            zero_flag = False
            count += 1
            sum_ = 0
            set_ = set()
            if t == 1:
                d = 1
                if j + d < self.size:
                    while self.num_matrix[i][j + d] >= 0:
                        hold_ = self.num_matrix[i][j + d]
                        if hold_ > 9:
                            return False
                        if set_.__contains__(hold_):
                            return False
                        if hold_ > 0:
                            sum_ += hold_
                            set_.add(hold_)
                        if hold_ == 0:
                            zero_flag = True
                        d += 1
                        if j + d >= self.size:
                            break
            elif t == 2:
                d = 1
                if i + d < self.size:
                    while self.num_matrix[i + d][j] >= 0:
                        hold_ = self.num_matrix[i + d][j]
                        if hold_ > 9:
                            return False
                        if set_.__contains__(hold_):
                            return False
                        if hold_ > 0:
                            sum_ += hold_
                            set_.add(hold_)
                        if hold_ == 0:
                            zero_flag = True
                        d += 1
                        if i + d >= self.size:
                            break
            if sum_ > k:
                return False
            if sum_ == k and zero_flag:
                return False
            if not zero_flag and sum_ < k:
                return False
        return True

    def insert_new_cell_number(self, row, col, value):
        try:
            if value < 0:
                raise ValueError("Negative numbers are not allowed for cell values.")
            if not (0 <= row < self.size) or not (0 <= col < self.size):
                raise ValueError("Cell coordinates out of bounds.")
            if (row, col) in [(cell[0], cell[1]) for cell in self.rules + self.closed]:
                raise ValueError("Cannot change value of a closed or rule cell.")
            self.num_matrix[row][col] = value
            if self.constraint_satisfied():
                if self.win():
                    return 1
                else:
                    return 2
            else:
                return 0
        except ValueError as e:
            print(f"Error: {e}")

    def print_board(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.num_matrix[i][j] == -3:
                    print("  X", end=" ")
                elif self.num_matrix[i][j] == -2:
                    hold = [0, 0]
                    for (x, y, k, t) in self.rules:
                        if x == i and y == j:
                            hold[t - 1] = int(k)
                    print(f" {hold[1]}\\{hold[0]}", end="")
                elif self.num_matrix[i][j] == -1:
                    for (x, y, k, t) in self.rules:
                        if x == i and y == j:
                            if t == 1:
                                print(f"  \\{k}", end="")
                            if t == 2:
                                print(f" {k}\\", end=" ")
                else:
                    print(" ", self.num_matrix[i][j], end=" ")
            print()
