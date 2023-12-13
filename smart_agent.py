import numpy as np
import copy
from board import Board

class Agent:
    def __init__(self, size, closed, rules):
        self.board_ = Board(size, closed, rules)

    def solve(self):
        self.back_track()

    def back_track(self):
        stack = [self.board_]
        hold_state = stack[0]
        while stack:
            count_row = 0
            count_cul = 0
            flag = False
            hold_state = stack.pop()
            # print(hold_state.constraint_satisfied())
            # hold_state.print_board()
            # print()
            if hold_state.win():
                print("solved:")
                hold_state.print_board()
                break
            if hold_state.constraint_satisfied():
                for i in hold_state.num_matrix:
                    for j in i:
                        if j == 0:
                            for k in range(1, 10):
                                hold_matrix = np.copy(hold_state.num_matrix)
                                hold_matrix[count_row][count_cul] = k
                                hold = self.new_state(hold_matrix, hold_state.size)
                                if hold.constraint_satisfied():
                                    stack.append(hold)
                            flag = True
                        count_cul += 1
                        if flag:
                            break
                    if flag:
                        break
                    count_cul = 0
                    count_row += 1
        if hold_state.win():
            return
        else:
            print("unable to solve!")

    def new_state(self, matrix, size):
        new_board = Board(size, copy.copy(self.board_.closed), copy.copy(self.board_.rules))
        new_board.num_matrix = np.copy(matrix)
        return new_board
