import tkinter as tk
from tkinter import messagebox
import random
import heapq

GOAL_STATE = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

class PuzzleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("8-Puzzle Solver")
        self.board = [row[:] for row in GOAL_STATE]
        self.buttons = [[None] * 3 for _ in range(3)]
        self.create_widgets()

    def create_widgets(self):
        # Create puzzle buttons
        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(self.root, font=("Helvetica", 24), width=4, height=2)
                self.buttons[i][j].grid(row=i, column=j, padx=5, pady=5)

        # Solve and shuffle buttons
        tk.Button(self.root, text="Shuffle", command=self.shuffle_board).grid(row=3, column=0, columnspan=1)
        tk.Button(self.root, text="Solve", command=self.solve_puzzle).grid(row=3, column=1, columnspan=1)
        self.step_label = tk.Label(self.root, text="Steps: 0")
        self.step_label.grid(row=3, column=2)

        self.update_buttons()

    def update_buttons(self):
        for i in range(3):
            for j in range(3):
                num = self.board[i][j]
                self.buttons[i][j]["text"] = str(num) if num != 0 else ""
                self.buttons[i][j]["bg"] = "#f0f0f0" if num != 0 else "#dddddd"

    def shuffle_board(self):
        flat = list(range(9))
        while True:
            random.shuffle(flat)
            self.board = [flat[:3], flat[3:6], flat[6:]]
            if self.is_solvable(flat):
                break
        self.update_buttons()
        self.step_label["text"] = "Steps: 0"

    def is_solvable(self, tiles):
        inv_count = 0
        for i in range(8):
            for j in range(i + 1, 9):
                if tiles[i] and tiles[j] and tiles[i] > tiles[j]:
                    inv_count += 1
        return inv_count % 2 == 0

    def solve_puzzle(self):
        start = tuple(sum(self.board, []))
        if start == tuple(sum(GOAL_STATE, [])):
            messagebox.showinfo("Already Solved", "The puzzle is already in the goal state.")
            return
        path = self.a_star(start)
        if not path:
            messagebox.showerror("Unsolvable", "This puzzle can't be solved.")
            return
        self.animate_solution(path)

    def animate_solution(self, path):
        if not path:
            return
        state = path.pop(0)
        self.board = [list(state[i:i+3]) for i in range(0, 9, 3)]
        self.update_buttons()
        self.step_label["text"] = f"Steps: {len(path)}"
        if path:
            self.root.after(500, lambda: self.animate_solution(path))

    def a_star(self, start):
        def heuristic(state):
            return sum(abs((val - 1) % 3 - i % 3) + abs((val - 1) // 3 - i // 3)
                       for i, val in enumerate(state) if val != 0)

        def neighbors(state):
            idx = state.index(0)
            x, y = divmod(idx, 3)
            moves = []
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < 3 and 0 <= ny < 3:
                    new_idx = nx * 3 + ny
                    lst = list(state)
                    lst[idx], lst[new_idx] = lst[new_idx], lst[idx]
                    moves.append(tuple(lst))
            return moves

        frontier = [(heuristic(start), 0, start, [])]
        visited = set()

        while frontier:
            est, cost, current, path = heapq.heappop(frontier)
            if current in visited:
                continue
            visited.add(current)
            if current == tuple(sum(GOAL_STATE, [])):
                return path + [current]
            for neighbor in neighbors(current):
                if neighbor not in visited:
                    heapq.heappush(frontier, (cost + 1 + heuristic(neighbor), cost + 1, neighbor, path + [current]))
        return []

if __name__ == "__main__":
    root = tk.Tk()
    app = PuzzleGUI(root)
    root.mainloop()
