from board import Board
from smart_agent import Agent
import time


def parse_input(rule_input):
    rule_list = []
    for rule in rule_input:
        y, x, z, t = map(int, rule.split(','))
        rule_list.append((y, x, z, t))
    return rule_list


print("\033[91mAttention!\033[0m\n\033[94mThis program does not check if your entered values "
      "can be placed correctly on a table or if they interfere with each other.\nso be sure to "
      "enter the right values. Otherwise, you may encounter unexpected bugs and errors!\033[0m")
size = int(input("Enter the size of the board (it will make a size * size board): "))
closed_cells_input = input("Enter closed cells as 'row,column' (separated by spaces): ").split()
closed_cells = [(int(cell.split(',')[0]), int(cell.split(',')[1])) for cell in closed_cells_input]
rule_count = int(input("Enter the number of rule cells: "))
rule_cells_input = [input(f"Enter rule cell {i + 1} (row,column,sum,orientation): ") for i in range(rule_count)]
rule_cells = parse_input(rule_cells_input)
board_ = Board(size, list(closed_cells), list(rule_cells))
the_agent = Agent(board_.size, board_.closed, board_.rules)
start_time = time.time()
the_agent.solve()
end_time = time.time()
execution_time = end_time - start_time
print("\033[94m" + f"Execution time: {execution_time} seconds" + "\033[0m")
