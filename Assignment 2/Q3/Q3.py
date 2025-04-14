# Code Walkthrough -> This code solves Sudoku puzzles from a file (`Q03.txt`) using two methods: a custom solver with AC-3 and backtracking, and a ChatGPT-inspired solver 
# with additional heuristics (MRV, LCV). It reads each puzzle as an 81-character string, converts it to a 9x9 grid, and applies the solvers to find a solution. 
# Finally, it compares the solvers' performance by timing their execution and displays a solved puzzle grid.
from collections import deque
from typing import List, Tuple, Dict, Optional
from ortools.sat.python import cp_model  # type: ignore
import time

# Read puzzle strings from a file
def load_puzzles(file_path):
    with open(file_path, 'r') as f:
        return [line.strip() for line in f if line.strip()]

# Convert a puzzle string into a 9x9 grid
def string_to_grid(puzzle_string):
    return [[int(puzzle_string[i * 9 + j]) if puzzle_string[i * 9 + j] != '.' else 0 for j in range(9)] for i in range(9)]

# Custom solver using AC-3 and Backtracking
def custom_solve(board):
    row_flags = [[False] * 10 for _ in range(9)]  # Track used numbers in rows
    col_flags = [[False] * 10 for _ in range(9)]  # Track used numbers in columns
    box_flags = [[False] * 10 for _ in range(9)]  # Track used numbers in 3x3 boxes
    possible_values = {(row, col): set(range(1, 10)) for row in range(9) for col in range(9)}

    def enforce_arc_consistency():
        queue = deque((row, col) for row in range(9) for col in range(9) if board[row][col] == 0)
        while queue:
            row, col = queue.popleft()
            box_idx = (row // 3) * 3 + col // 3
            valid_nums = {num for num in possible_values[(row, col)]
                         if not row_flags[row][num] and not col_flags[col][num] and not box_flags[box_idx][num]}
            if not valid_nums:
                return False
            if len(valid_nums) == 1 and valid_nums != possible_values[(row, col)]:
                num = next(iter(valid_nums))
                set_value(row, col, num)
                # Add related cells to queue (same row, column, or box)
                queue.extend((r, c) for r in range(9) for c in range(9)
                            if (r == row or c == col or (r // 3 == row // 3 and c // 3 == col // 3))
                            and (r, c) != (row, col) and board[r][c] == 0)
            possible_values[(row, col)] = valid_nums
        return True

    def set_value(row, col, value):
        board[row][col] = value
        row_flags[row][value] = col_flags[col][value] = box_flags[(row // 3) * 3 + col // 3][value] = True
        possible_values[(row, col)] = {value}

    def clear_value(row, col, value):
        board[row][col] = 0
        row_flags[row][value] = col_flags[col][value] = box_flags[(row // 3) * 3 + col // 3][value] = False

    def search_with_backtracking():
        empty_cells = [(row, col) for row in range(9) for col in range(9) if board[row][col] == 0]
        if not empty_cells:
            return True
        row, col = empty_cells[0]
        box_idx = (row // 3) * 3 + col // 3

        for value in possible_values[(row, col)]:
            if row_flags[row][value] or col_flags[col][value] or box_flags[box_idx][value]:
                continue
            set_value(row, col, value)
            if search_with_backtracking():
                return True
            clear_value(row, col, value)
        return False

    # Initialize the board with given values
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                continue
            value = board[row][col]
            if row_flags[row][value] or col_flags[col][value] or box_flags[(row // 3) * 3 + col // 3][value]:
                return False
            set_value(row, col, value)

    if enforce_arc_consistency() and search_with_backtracking():
        return board
    return None

# OR-Tools-based solver
def solve_with_or_tools(board):
    solver_model = cp_model.CpModel()

    cell_values = [[solver_model.NewIntVar(1, 9, f"cell_{r}_{c}") for c in range(9)] for r in range(9)]

    # Set up constraints
    for r in range(9):
        for c in range(9):
            if board[r][c] != 0:
                solver_model.Add(cell_values[r][c] == board[r][c])
            solver_model.AddAllDifferent(cell_values[r])
            solver_model.AddAllDifferent([cell_values[i][c] for i in range(9)])
            if r % 3 == 0 and c % 3 == 0:
                solver_model.AddAllDifferent([
                    cell_values[r + i][c + j] for i in range(3) for j in range(3)
                ])

    solver = cp_model.CpSolver()
    result = solver.Solve(solver_model)
    if result in (cp_model.FEASIBLE, cp_model.OPTIMAL):
        return [[solver.Value(cell_values[r][c]) for c in range(9)] for r in range(9)]
    return None

# ChatGPT-inspired solver with AC-3 and heuristics
class PuzzleSolver:
    def __init__(self, puzzle: List[List[int]]):
        self.puzzle = puzzle
        self.grid_size = 9
        self.box_size = 3
        self.value_sets = self.setup_domains()

    def setup_domains(self) -> Dict[Tuple[int, int], List[int]]:
        domains = {}
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                if self.puzzle[row][col] == 0:
                    domains[(row, col)] = list(range(1, 10))
                else:
                    domains[(row, col)] = [self.puzzle[row][col]]
        return domains

    def find_related_cells(self, row: int, col: int) -> List[Tuple[int, int]]:
        related = set()
        for i in range(self.grid_size):
            related.add((row, i))  # Same row
            related.add((i, col))  # Same column
        box_row, box_col = row // self.box_size, col // self.box_size
        for r in range(box_row * self.box_size, (box_row + 1) * self.box_size):
            for c in range(box_col * self.box_size, (box_col + 1) * self.box_size):
                related.add((r, c))
        related.discard((row, col))
        return list(related)

    def apply_ac3(self) -> bool:
        queue = deque((cell1, cell2) for cell1 in self.value_sets for cell2 in self.find_related_cells(*cell1))
        while queue:
            cell1, cell2 = queue.popleft()
            if self.update_domain(cell1, cell2):
                if not self.value_sets[cell1]:
                    return False
                for neighbor in self.find_related_cells(*cell1):
                    if neighbor != cell2:
                        queue.append((neighbor, cell1))
        return True

    def update_domain(self, cell1: Tuple[int, int], cell2: Tuple[int, int]) -> bool:
        updated = False
        for val in self.value_sets[cell1][:]:
            if all(val == other_val for other_val in self.value_sets[cell2]):
                self.value_sets[cell1].remove(val)
                updated = True
        return updated

    def pick_next_cell(self) -> Tuple[int, int]:
        return min(
            (cell for cell in self.value_sets if self.puzzle[cell[0]][cell[1]] == 0),
            key=lambda cell: len(self.value_sets[cell]),
        )

    def sort_values(self, cell: Tuple[int, int]) -> List[int]:
        related_cells = self.find_related_cells(*cell)
        return sorted(
            self.value_sets[cell],
            key=lambda val: sum(val in self.value_sets[neighbor] for neighbor in related_cells),
        )

    def check_validity(self, cell: Tuple[int, int], value: int) -> bool:
        row, col = cell
        for related_cell in self.find_related_cells(row, col):
            if value in self.value_sets[related_cell] and len(self.value_sets[related_cell]) == 1:
                return False
        return True

    def recursive_search(self) -> Optional[List[List[int]]]:
        if all(len(self.value_sets[cell]) == 1 for cell in self.value_sets):
            return [[self.value_sets[(r, c)][0] for c in range(self.grid_size)] for r in range(self.grid_size)]

        cell = self.pick_next_cell()
        for value in self.sort_values(cell):
            if self.check_validity(cell, value):
                self.puzzle[cell[0]][cell[1]] = value
                previous_domains = self.value_sets.copy()
                self.value_sets[cell] = [value]
                if self.apply_ac3():
                    solution = self.recursive_search()
                    if solution:
                        return solution
                self.value_sets = previous_domains
                self.puzzle[cell[0]][cell[1]] = 0
        return None

    def solve(self) -> Optional[List[List[int]]]:
        if not self.apply_ac3():
            return None
        return self.recursive_search()

def display_board(board):
    if not board:
        return ""
    for row in range(9):
        if row != 0 and row % 3 == 0:
            print("-" * (9 + 2))
        for col in range(9):
            if col != 0 and col % 3 == 0:
                print("|", end="")
            print(board[row][col] if board[row][col] else '.', end="")
        print()

# Measurs avg runtime of solver
def measure_time(solver_func, *args, trials=10):
    elapsed = 0
    for _ in range(trials):
        start = time.time()
        solver_func(*args)
        elapsed += time.time() - start
    return elapsed / trials

# Comparing solvers' performance
def compare_solvers(solver, puzzle_strings):
    print(f"Running {solver.__name__}...")
    total_time = 0
    for puzzle in puzzle_strings:
        total_time += measure_time(solver, string_to_grid(puzzle), trials=10)
    return total_time / len(puzzle_strings)

puzzles = load_puzzles("Q3.txt")
print("Custom Solver:", compare_solvers(custom_solve, puzzles))
print("OR-Tools Solver:", compare_solvers(solve_with_or_tools, puzzles))
print("ChatGPT Solver:", compare_solvers(lambda grid: PuzzleSolver(grid).solve(), puzzles))
print()
display_board(solve_with_or_tools(string_to_grid(puzzles[1])))
