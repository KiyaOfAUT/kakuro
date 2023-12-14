import numpy as np
import copy
from board import Board
import time
import os
from itertools import permutations


class Agent:
    def __init__(self, size, closed, rules):
        self.rules = sorted(rules, key=lambda x: (x[0], x[1]))
        self.board_ = Board(size, closed, rules)
        self.result = []

    def solve(self):
        self.backtrack()

    def backtrack(self):
        stack = [self.board_]
        hold_state = stack[0]
        while stack:
            hold_state = stack.pop()
            if hold_state.win():
                os.system('cls' if os.name == 'nt' else 'clear')
                print("\033[92mSolved:\033[0m")
                hold_state.print_board()
                return
            if hold_state.constraint_satisfied():
                for i in self.rules:
                    if self.is_empty(i, hold_state):
                        for j in self.find_combinations(self.length(i), i[2]):
                            hold_perm = permutations(j)
                            for k in hold_perm:
                                hold_ = self.new_state(hold_state.num_matrix, hold_state.size, i, k)
                                if hold_.constraint_satisfied():
                                    stack.append(hold_)
                        break
        print("unable to solve!")

    def new_state(self, matrix, size, rule, set_):
        d = 1
        new_board = Board(size, copy.copy(self.board_.closed), copy.copy(self.board_.rules))
        new_board.num_matrix = np.copy(matrix)
        if rule[3] == 1:
            for i in set_:
                new_board.num_matrix[rule[0]][rule[1] + d] = i
                d += 1
        else:
            for i in set_:
                new_board.num_matrix[rule[0] + d][rule[1]] = i
                d += 1
        return new_board

    def find_combinations(self, n, m):
        self.result.clear()
        self.combination([], n, m, 1)
        return self.result

    def combination(self, curr_comb, remaining_count, target_sum, start):
        if remaining_count == 0 and target_sum == 0:
            self.result.append(curr_comb[:])
            return
        if remaining_count == 0 or target_sum < 0:
            return
        for i in range(start, 10):
            curr_comb.append(i)
            self.combination(curr_comb, remaining_count - 1, target_sum - i, i + 1)
            curr_comb.pop()

    @staticmethod
    def is_empty(rule, hold_state):
        d = 1
        if rule[3] == 1:
            hold_ = hold_state.num_matrix[rule[0]][rule[1] + d]
            while hold_ >= 0:
                if hold_ == 0:
                    return True
                d += 1
                if rule[1] + d == hold_state.size:
                    return False
                hold_ = hold_state.num_matrix[rule[0]][rule[1] + d]
        else:
            hold_ = hold_state.num_matrix[rule[0] + d][rule[1]]
            while hold_ >= 0:
                if hold_ == 0:
                    return True
                d += 1
                if rule[0] + d == hold_state.size:
                    return False
                hold_ = hold_state.num_matrix[rule[0] + d][rule[1]]
        return False

    def length(self, rule):
        d = 1
        count_ = 0
        if rule[3] == 1:
            while self.board_.num_matrix[rule[0]][rule[1] + d] >= 0:
                count_ += 1
                d += 1
                if rule[1] + d == self.board_.size:
                    return count_
        else:
            while self.board_.num_matrix[rule[0] + d][rule[1]] >= 0:
                count_ += 1
                d += 1
                if rule[0] + d == self.board_.size:
                    return count_
        return count_
