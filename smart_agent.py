import numpy as np
import copy
from board import Board
import time
import os
from itertools import permutations


class Agent:
    def __init__(self, size, closed, rules):
        self.board_ = Board(size, closed, rules)
        hold_rules = []
        self.rules = []
        self.intersection_matrix = np.copy(self.board_.num_matrix)
        self.calculate_intersections()
        self.intersected_rules = []
        self.result = []
        for (i, j, t, k) in rules:
            self.rules.append([i, j, t, k, 0, 0])
        for (i, j, t, k, n, c) in self.rules:
            hold_rules.append([i, j, t, k, self.length((i, j, t, k)), self.remained_values((i, j, t, k, 0, 0), self.board_)])
        self.rules = sorted(hold_rules, key=lambda x: (x[5], x[0], x[1]))

    def solve(self):
        self.backtrack()

    def backtrack(self):
        d = 1
        stack = [self.board_]
        while stack:
            d += 1
            # print(self.rules)
            hold_state = stack.pop()
            # hold_state.print_board()
            # time.sleep(2)
            # os.system('cls' if os.name == 'nt' else 'clear')
            # print(1111111111111111111111111111111111111111111111111111111111)
            for i in self.rules:
                # print(len(self.remained_values(i, hold_state)))
                i[5] = len(self.remained_values(i, hold_state))
            self.rules = sorted(self.rules, key=lambda x: (x[5], x[0], x[1]))
            if hold_state.win():
                os.system('cls' if os.name == 'nt' else 'clear')
                print("\033[92mSolved:\033[0m")
                hold_state.print_board()
                return
            for i in self.rules:
                if i[5] > 0:
                    hold_states = []
                    for j in self.remained_values(i, hold_state):
                        hold_next_rules = []
                        for (k1, k2, k3, k4) in self.intersects_rules(i):
                            for (y, x, z, q, w, e) in self.rules:
                                if k1 == y and k2 == x and k4 == w:
                                    hold_next_rules.append([y, x, z, q, w, e])
                        sum_ = 0
                        hold_ = self.new_state(hold_state.num_matrix, hold_state.size, i, j)
                        if hold_.constraint_satisfied():
                            for k in hold_next_rules:
                                sum_ += len(self.remained_values(k, hold_))
                            hold_states.append((hold_, sum_))
                    hold_states = sorted(hold_states, key=lambda key: key[1])
                    while hold_states:
                        stack.append(hold_states.pop(0)[0])
                    break
        print("unable to solve!", d)

    def new_state(self, matrix, size, rule, perm):
        d = 1
        new_board = Board(size, copy.copy(self.board_.closed), copy.copy(self.board_.rules))
        new_board.num_matrix = np.copy(matrix)
        if rule[3] == 1:
            for i in perm:
                new_board.num_matrix[rule[0]][rule[1] + d] = i
                d += 1
        else:
            for i in perm:
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

    def calculate_intersections(self):
        for rule in self.rules:
            d = 1
            if rule[3] == 1:
                while self.intersection_matrix[rule[0]][rule[1] + d] >= 0:
                    self.intersection_matrix[rule[0]][rule[1] + d] += 1
                    d += 1
                    if rule[1] + d == self.board_.size:
                        break
            else:
                while self.intersection_matrix[rule[0] + d][rule[1]] >= 0:
                    self.intersection_matrix[rule[0] + d][rule[1]] += 1
                    d += 1
                    if rule[0] + d == self.board_.size:
                        break

    def intersects_rules(self, rule):
        d = 1
        hold_rules = []
        if rule[3] == 1:
            while self.intersection_matrix[rule[0]][rule[1] + d] >= 0:
                if self.intersection_matrix[rule[0]][rule[1] + d] == 2:
                    j = 1
                    while self.intersection_matrix[rule[0] - j][rule[1] + d] >= 0:
                        j += 1
                    hold_rules.append((rule[0] - j, rule[1] + d, d, 2))
                d += 1
                if rule[1] + d == self.board_.size:
                    break
        else:
            while self.intersection_matrix[rule[0] + d][rule[1]] >= 0:
                if self.intersection_matrix[rule[0] + d][rule[1]] == 2:
                    j = 1
                    while self.intersection_matrix[rule[0] + d][rule[1] - j] >= 0:
                        j += 1
                    hold_rules.append((rule[0] + d, rule[1] - j, d, 1))
                d += 1
                if rule[0] + d == self.board_.size:
                    break
        return hold_rules

    def available_perms(self, rule):
        self.intersected_rules.clear()
        for (i, j, k, t) in self.intersects_rules(rule):
            for (y, x, l, m, n, c) in self.rules:
                if i == y and j == x and t == m:
                    self.intersected_rules.append((y, x, l, k, n))
                    break
        main_perms = []
        for i in self.find_combinations(rule[4], rule[2]):
            for j in permutations(i):
                main_perms.append(j)
        return filter(self.check_intersections, main_perms)

    def check_intersections(self, perm):
        for (i, j, k, t, n) in self.intersected_rules:
            flag = False
            hold_ = set()
            for d in self.find_combinations(n, k):
                hold_.clear()
                for d_ in d:
                    hold_.add(d_)
                if hold_.__contains__(perm[t - 1]):
                    flag = True
            if not flag:
                return False
        return True

    def remained_values(self, rule, board_state):
        if not self.is_empty(rule, board_state):
            return []
        hold_ = []
        filled_cells = self.filled(rule, board_state.num_matrix)
        for i in self.available_perms(rule):
            hold_.append([i, filled_cells])
        hold = []
        for i in filter(self.check_full_cells, hold_):
            hold.append(i[0])
        # print(hold)
        return hold

    @staticmethod
    def check_full_cells(perm):
        d = 0
        for i in perm[0]:
            if 0 < perm[1][d] != i:
                return False
            d += 1
        return True

    def filled(self, rule, matrix):
        hold = []
        d = 1
        if rule[3] == 1:
            while matrix[rule[0]][rule[1] + d] >= 0:
                hold.append(matrix[rule[0]][rule[1] + d])
                d += 1
                if rule[1] + d == self.board_.size:
                    break
        else:
            while matrix[rule[0] + d][rule[1]] >= 0:
                hold.append(matrix[rule[0] + d][rule[1]])
                d += 1
                if rule[0] + d == self.board_.size:
                    break
        return hold
