import time
from queue import Queue, LifoQueue
import tkinter as tk
from tkinter import messagebox

# Utility function to check if placing num in (row, col) is valid
def is_valid(board, row, col, num):
    block_row, block_col = 3 * (row // 3), 3 * (col // 3)
    return (
        num not in board[row] and
        num not in [board[r][col] for r in range(9)] and
        num not in [
            board[r][c]
            for r in range(block_row, block_row + 3)
            for c in range(block_col, block_col + 3)
        ]
    )

class Node:
    def __init__(self, state, parent=None, action=None):
        self.state = state
        self.parent = parent
        self.action = action
        self.children = []

class Problem:
    def __init__(self, initial):
        self.initial = initial
        self.goal = [[0 for _ in range(9)] for _ in range(9)]

    def is_goal(self, state):
        return all(all(row) for row in state)

    def actions(self, state):
        for row in range(9):
            for col in range(9):
                if state[row][col] == 0:
                    return [(row, col, num) for num in range(1, 10) if is_valid(state, row, col, num)]

        return []

    def result(self, state, action):
        row, col, num = action
        new_state = [list(row) for row in state]
        new_state[row][col] = num
        return new_state

class SudokuSolver:
    def __init__(self, problem):
        self.problem = problem
        self.solution = None
        self.search_tree = None

    def dfs(self):
        start_time = time.time()
        frontier = LifoQueue()
        frontier.put(Node(self.problem.initial))
        while not frontier.empty():
            node = frontier.get()
            if self.problem.is_goal(node.state):
                self.solution = node.state
                return time.time() - start_time
            for action in self.problem.actions(node.state):
                child_state = self.problem.result(node.state, action)
                child = Node(child_state, node, action)
                frontier.put(child)

        return None

    def bfs(self):
        start_time = time.time()
        frontier = Queue()
        frontier.put(Node(self.problem.initial))
        while not frontier.empty():
            node = frontier.get()
            if self.problem.is_goal(node.state):
                self.solution = node.state
                return time.time() - start_time
            for action in self.problem.actions(node.state):
                child_state = self.problem.result(node.state, action)
                child = Node(child_state, node, action)
                frontier.put(child)

        return None

    def dls(self, limit):
        start_time = time.time()

        def recursive_dls(node, depth):
            if self.problem.is_goal(node.state):
                self.solution = node.state
                return True
            if depth == 0:
                return False
            for action in self.problem.actions(node.state):
                child_state = self.problem.result(node.state, action)
                child = Node(child_state, node, action)
                if recursive_dls(child, depth - 1):
                    return True
            return False

        result = recursive_dls(Node(self.problem.initial), limit)
        if result:
            return time.time() - start_time

        return None

class SudokuApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sudoku Solver")
        self.grid = [[tk.StringVar() for _ in range(9)] for _ in range(9)]
        self.create_grid()
        self.create_controls()

    def create_grid(self):
        frame = tk.Frame(self.root)
        frame.pack()
        for row in range(9):
            for col in range(9):
                entry = tk.Entry(frame, width=2, font=('Arial', 18), textvariable=self.grid[row][col], justify='center')
                entry.grid(row=row, column=col, padx=2, pady=2)

    def create_controls(self):
        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        tk.Button(frame, text="Solve with DFS", command=lambda: self.solve('DFS')).grid(row=0, column=0, padx=5)
        tk.Button(frame, text="Solve with BFS", command=lambda: self.solve('BFS')).grid(row=0, column=1, padx=5)
        tk.Button(frame, text="Solve with DLS", command=lambda: self.solve('DLS')).grid(row=0, column=2, padx=5)
        tk.Label(frame, text="Depth Limit:").grid(row=1, column=0, padx=5, sticky='e')
        self.limit_entry = tk.Entry(frame, width=5)
        self.limit_entry.grid(row=1, column=1, padx=5)

    def get_board(self):
        try:
            board = [[int(self.grid[row][col].get() or 0) for col in range(9)] for row in range(9)]
            return board
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter numbers only.")
            return None

    def solve(self, algorithm):
        board = self.get_board()
        if not board:
            return

        problem = Problem(board)
        solver = SudokuSolver(problem)

        if algorithm == 'DFS':
            elapsed_time = solver.dfs()
        elif algorithm == 'BFS':
            elapsed_time = solver.bfs()
        elif algorithm == 'DLS':
            try:
                limit = int(self.limit_entry.get())
            except ValueError:
                messagebox.showerror("Error", "Invalid depth limit.")
                return
            elapsed_time = solver.dls(limit)
        else:
            messagebox.showerror("Error", "Unknown algorithm.")
            return

        if solver.solution:
            for row in range(9):
                for col in range(9):
                    self.grid[row][col].set(solver.solution[row][col])
            messagebox.showinfo("Success", f"Solved in {elapsed_time:.2f} seconds using {algorithm}.")
        else:
            messagebox.showerror("Error", "Unable to solve the Sudoku.")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = SudokuApp()
    app.run()
