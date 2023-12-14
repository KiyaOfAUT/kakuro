from board import Board
from smart_agent import Agent


def parse_input(rule_input):
    rule_list = []
    for rule in rule_input:
        y, x, z, t = map(int, rule.split(','))
        if t not in [1, 2]:
            raise ValueError("Invalid orientation value. Please use 1 for horizontal or 2 for vertical.")
        rule_list.append((y, x, z, t))
    return rule_list


def get_input(prompt):
    value = input(prompt)
    return value


size = int(input("Enter the size of the board (it will make a size * size board): "))
closed_cells_input = input("Enter closed cells as 'row,column' (separated by spaces): ").split()
closed_cells = [(int(cell.split(',')[0]), int(cell.split(',')[1])) for cell in closed_cells_input]
rule_count = int(input("Enter the number of rule cells: "))
rule_cells_input = [input(f"Enter rule cell {i + 1} (row,column,sum,orientation): ") for i in range(rule_count)]
rule_cells = parse_input(rule_cells_input)
try:
    intersection = any(cell in closed_cells for cell in rule_cells)
    if intersection:
        raise ValueError("Rule cells intersect with closed cells. Please provide valid inputs.")
    board_ = Board(size, list(closed_cells), list(rule_cells))
    print("the kakuro board:")
    board_.print_board()
    solver = Agent(board_.size, board_.closed, board_.rules)
    solver.solve()
except ValueError as e:
    print(f"Error: {e}")
