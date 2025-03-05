import tkinter as tk
from tkinter import messagebox
from ai_player import AIPlayer
import game_controller as game_controller
from play_tree import PlayTree
from search_algorithms import SearchAlgorithms

# Global UI settings
WINDOW_WIDTH = 700
WINDOW_HEIGHT = 900
FONT_LARGE = ("Arial", 16)
FONT_MEDIUM = ("Arial", 12)
FONT_SMALL = ("Arial", 10)
BUTTON_WIDTH = 20
BUTTON_HEIGHT = 1
CELL_BORDER_WIDTH = 1
CELL_COLORS = {0: "white", 1: "blue", 2: "red", "last_placed": "green"}
HIGHLIGHT_COLOR = "yellow"

GAME_BUTTON_STYLE = {
    "bg": "#155724", "fg": "white", "activebackground": "#0b3d20"
}

PLAN_BUTTON_STYLE = {
    "bg": "#003366", "fg": "white", "activebackground": "#002244"
}


class GameGUI:
    """
    Initializes the game GUI.
    """

    def __init__(self, root, game_controller):
        self.root = root
        self.root.title("Block Placement Game")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.game = game_controller
        self.ai_player = AIPlayer(self.game)  # Initialize AI Player
        self.last_placed_positions = []
        self.play_tree = self.calculate_tree()
        self.game_plan = None

        # Main frames
        self.board_frame = tk.Frame(root)
        self.board_frame.pack(pady=20)
        self.next_piece_frame = tk.Frame(root)
        self.next_piece_frame.pack(pady=10)
        self.input_frame = tk.Frame(root)
        self.input_frame.pack(pady=10)

        # Labels
        self.score_label = tk.Label(root, text="Score: 0", font=FONT_LARGE)
        self.score_label.pack(pady=10)
        self.remaining_pieces_label = tk.Label(root, text=f"Remaining Pieces: {len(self.game.piece_sequence.sequence)}", font=FONT_MEDIUM)
        self.remaining_pieces_label.pack(pady=10)
        self.status_label = tk.Label(root, text="", font=FONT_MEDIUM)
        self.status_label.pack(pady=5)

        # User input fields
        tk.Label(self.input_frame, text="Row:", font=FONT_MEDIUM).pack(side=tk.LEFT)
        self.row_entry = tk.Entry(self.input_frame, width=5, font=FONT_MEDIUM)
        self.row_entry.pack(side=tk.LEFT)
        tk.Label(self.input_frame, text="Col:", font=FONT_MEDIUM).pack(side=tk.LEFT, padx=5)
        self.col_entry = tk.Entry(self.input_frame, width=5, font=FONT_MEDIUM)
        self.col_entry.pack(side=tk.LEFT)

        # Button Frame (to group buttons properly)
        self.button_frame = tk.Frame(root)
        self.button_frame.pack(pady=20)

        # Buttons for Gameplay
        self.manual_button = tk.Button(self.button_frame, text="Play Manually", command=self.manual_play_gui,
                                       font=FONT_LARGE, width=BUTTON_WIDTH, height=BUTTON_HEIGHT, **GAME_BUTTON_STYLE)
        self.manual_button.pack(pady=5)

        self.ai_button = tk.Button(self.button_frame, text="Play assisted by AI", command=self.play_ai_turn,
                                   font=FONT_LARGE, width=BUTTON_WIDTH, height=BUTTON_HEIGHT, state=tk.DISABLED,
                                   **GAME_BUTTON_STYLE)
        self.ai_button.pack(pady=5)

        # Buttons for Planning
        self.dfs_button = tk.Button(self.button_frame, text="Calculate game plan DFS",
                                    command=lambda: self.get_game_plan('DFS'),
                                    font=FONT_LARGE, width=BUTTON_WIDTH, height=BUTTON_HEIGHT, **PLAN_BUTTON_STYLE)
        self.dfs_button.pack(pady=5)

        self.bfs_button = tk.Button(self.button_frame, text="Calculate game plan BFS",
                                    command=lambda: self.get_game_plan('BFS'),
                                    font=FONT_LARGE, width=BUTTON_WIDTH, height=BUTTON_HEIGHT, **PLAN_BUTTON_STYLE)
        self.bfs_button.pack(pady=5)

        self.a_star_button = tk.Button(self.button_frame, text="Calculate game plan A*",
                                       command=lambda: self.get_game_plan('A*'),
                                       font=FONT_LARGE, width=BUTTON_WIDTH, height=BUTTON_HEIGHT, **PLAN_BUTTON_STYLE)
        self.a_star_button.pack(pady=5)

        self.ids_button = tk.Button(self.button_frame, text="Calculate game plan IDS",
                                    command=lambda: self.get_game_plan('IDS'),
                                    font=FONT_LARGE, width=BUTTON_WIDTH, height=BUTTON_HEIGHT, **PLAN_BUTTON_STYLE)
        self.ids_button.pack(pady=5)

        # Initialize board and UI elements
        self.cells = {}
        self.update_board_display()
        self.update_next_piece_display()
        self.update_score_display()

    def calculate_tree(self):
        tree = PlayTree(self.game, len(self.game.piece_sequence.sequence))
        tree.print_tree()
        return tree

    def get_game_plan(self, algorithm):
        if algorithm == 'DFS':
            game_plan_positions = SearchAlgorithms.depth_first_search(self.play_tree)
            if game_plan_positions:
                pieces_names = [piece[0] for piece in self.game.piece_sequence.get_full_sequence()]
                self.game_plan = list(zip(game_plan_positions, pieces_names))
                print("DFS Game Plan:", self.game_plan)
            else:
                self.game_plan = None
                print("No DFS Game Plan found.")

        if algorithm == 'BFS':
            game_plan_positions = SearchAlgorithms.breadth_first_search(self.play_tree)
            if game_plan_positions:
                pieces_names = [piece[0] for piece in self.game.piece_sequence.get_full_sequence()]
                self.game_plan = list(zip(game_plan_positions, pieces_names))
                print("BFS Game Plan:", self.game_plan)
            else:
                self.game_plan = None
                print("No BFS Game Plan found.")

        elif algorithm == 'A*':
            game_plan_positions = SearchAlgorithms.a_star_search(self.play_tree)
            if game_plan_positions:
                pieces_names = [piece[0] for piece in self.game.piece_sequence.get_full_sequence()]
                self.game_plan = list(zip(game_plan_positions, pieces_names))
                print("A* Game Plan:", self.game_plan)
            else:
                self.game_plan = None
                print("No A* Game Plan found.")

        elif algorithm == 'IDS':
            game_plan_positions = SearchAlgorithms.iterative_deepening_search(self.play_tree, max_depth=10) # You can adjust max_depth
            if game_plan_positions:
                pieces_names = [piece[0] for piece in self.game.piece_sequence.get_full_sequence()]
                self.game_plan = list(zip(game_plan_positions, pieces_names))
                print("IDS Game Plan:", self.game_plan)
            else:
                self.game_plan = None
                print("No IDS Game Plan found.")


        if self.game_plan:  # If a valid game plan exists, enable AI button
            self.ai_button.config(state=tk.NORMAL)
        else:
            self.ai_button.config(state=tk.DISABLED)


    def update_board_display(self):
        """
        Updates the board display.
        """
        self.create_board_grid()
        self.update_cell_colors()

    def create_board_grid(self):
        """
        Creates the board grid.
        """
        for c in range(self.game.game_board.cols):
            tk.Label(self.board_frame, text=str(c), font=FONT_SMALL).grid(row=0, column=c + 1, padx=1, pady=1)

        for r in range(self.game.game_board.rows):
            tk.Label(self.board_frame, text=str(r), font=FONT_SMALL).grid(row=r + 1, column=0, padx=1, pady=1)
            for c in range(self.game.game_board.cols):
                if (r, c) not in self.cells:
                    cell_label = tk.Label(self.board_frame, width=2, height=1, relief=tk.SOLID,
                                          borderwidth=CELL_BORDER_WIDTH, font=FONT_SMALL)
                    cell_label.grid(row=r + 1, column=c + 1, padx=1, pady=1)
                    cell_label.bind("<Button-1>", lambda event, row=r, col=c: self.on_cell_click(row, col))
                    cell_label.bind("<Enter>", lambda event, row=r, col=c: self.on_cell_enter(row, col))
                    cell_label.bind("<Leave>", lambda event, row=r, col=c: self.on_cell_leave(row, col))
                    self.cells[(r, c)] = cell_label

    def on_cell_enter(self, row, col):
        """
        Handles cell enter events.
        """
        self.cells[(row, col)].config(bg=HIGHLIGHT_COLOR)

    def on_cell_leave(self, row, col):
        """
        Handles cell leave events.
        """
        if (row, col) in self.last_placed_positions:
            self.cells[(row, col)].config(bg=CELL_COLORS["last_placed"])
        else:
            self.cells[(row, col)].config(bg=CELL_COLORS.get(self.game.game_board.board[row][col]))

    def on_cell_click(self, row, col):
        """
        Handles cell click events.
        """
        placed_positions = self.game.play(row, col)
        if placed_positions:
            self.last_placed_positions = placed_positions
            self.update_board_display()
            self.update_next_piece_display()
            self.update_score_display()
            self.update_remaining_pieces_label()
            self.status_label.config(text="Piece placed successfully.")
            self.check_game_status()
        else:
            self.status_label.config(text="Invalid move. Try again.")

    def update_cell_colors(self):
        """
        Updates the colors of the cells.
        """
        for r in range(self.game.game_board.rows):
            for c in range(self.game.game_board.cols):
                cell_value = self.game.game_board.board[r][c]
                color = CELL_COLORS.get(cell_value, "white")
                if (r, c) in self.last_placed_positions:
                    color = "green"
                self.cells[(r, c)].config(bg=color)


    def update_next_piece_display(self):
        """
        Updates the next piece display.
        """
        self.clear_next_piece_frame()
        next_piece_info = self.game.piece_sequence.peek_next_piece()
        if next_piece_info:
            next_piece_name, next_piece_shape = next_piece_info
            tk.Label(self.next_piece_frame, text=f"Next Piece: {next_piece_name}", font=FONT_MEDIUM).pack()
            self.draw_next_piece_grid(next_piece_shape)
        else:
            tk.Label(self.next_piece_frame, text="No more pieces", font=FONT_MEDIUM).pack()

    def clear_next_piece_frame(self):
        """
        Clears the next piece frame.
        """
        for widget in self.next_piece_frame.winfo_children():
            widget.destroy()

    def draw_next_piece_grid(self, shape):
        """
        Draws the next piece grid.
        """
        piece_grid = tk.Frame(self.next_piece_frame)
        piece_grid.pack()
        for r in range(len(shape)):
            for c in range(len(shape[0])):
                color = "red" if shape[r][c] == 2 else "blue" if shape[r][c] == 1 else "white"
                tk.Label(piece_grid, width=2, height=1, relief=tk.SOLID, borderwidth=CELL_BORDER_WIDTH,
                         bg=color).grid(row=r, column=c, padx=1, pady=1)

    def update_score_display(self):
        """
        Updates the score label.
        """
        self.score_label.config(text=f"Score: {self.game.score}")

    def update_remaining_pieces_label(self):
        """
        Updates the remaining pieces label.
        """
        self.remaining_pieces_label.config(text=f"Remaining Pieces: {len(self.game.piece_sequence.sequence)}")

    def manual_play_gui(self):
        """
        Handles manual piece placement from user input.
        """
        self.check_game_status()
        try:
            row = int(self.row_entry.get())
            col = int(self.col_entry.get())
        except ValueError:
            self.status_label.config(text="Invalid input: Row and Column must be integers.")
            return

        placed_positions = self.game.play(row, col)
        if placed_positions:
            self.last_placed_positions = placed_positions
            self.update_board_display()
            self.update_next_piece_display()
            self.update_score_display()
            self.update_remaining_pieces_label()
            self.status_label.config(text="Piece placed successfully.")
            self.row_entry.delete(0, tk.END)
            self.col_entry.delete(0, tk.END)
        else:
            self.status_label.config(text="Invalid move. Try again.")

    def play_ai_turn(self):
        """
        Makes the AI play one step and updates the UI.
        """
        self.check_game_status()
        # placed_positions = self.ai_player.play_step()
        print('Game plan :', self.game_plan)
        if self.game_plan:
            next_move, piece_name = self.game_plan.pop(0)
            placed_positions = self.game.play(next_move[0],  next_move[1])

            if placed_positions:
                self.last_placed_positions = placed_positions
                self.update_board_display()
                self.update_next_piece_display()
                self.update_score_display()
                self.update_remaining_pieces_label()
                self.status_label.config(text="AI placed a piece successfully.")
                self.check_game_status()
            else:
                self.status_label.config(text="AI couldn't find a valid move.")
        else:
            self.status_label.config(text="No game plan available.")


    def check_game_status(self):
        """
        Checks the game status and displays a message if the game ends.
        """
        game_over_status = self.game.is_game_over()
        if game_over_status == "victory":
            messagebox.showinfo("Game Over",
                                f"Congratulations! You placed all pieces. Victory!\nScore: {self.game.score}")
            self.manual_button.config(state=tk.DISABLED)
            self.ai_button.config(state=tk.DISABLED)
        elif game_over_status == "defeat":
            messagebox.showinfo("Game Over", f"Sorry! You have lost. Defeat!\nScore: {self.game.score}")
            self.manual_button.config(state=tk.DISABLED)
            self.ai_button.config(state=tk.DISABLED)
        else:
            print("The player can keep playing")