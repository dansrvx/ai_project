import tkinter as tk
from tkinter import messagebox
import game_controller as game_controller
from ai_player import AIPlayer

# Global UI settings - Increased sizes (and further adjustments)
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 800
FONT_LARGE = ("Arial", 24)
FONT_MEDIUM = ("Arial", 18)  # Slightly increased medium font
FONT_SMALL = ("Arial", 14)   # Slightly increased small font
BUTTON_WIDTH = 25
CELL_BORDER_WIDTH = 1
CELL_COLORS = {0: "white", 1: "blue", 2: "red", "last_placed": "green"}
HIGHLIGHT_COLOR = "yellow"


class GameGUI:
    def __init__(self, root, game_controller):
        """Initializes the game GUI."""
        self.root = root
        self.root.title("Wood Block Puzzle - By DM, AO, RP [MECD AI Project]")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")

        # Configure root window to be resizable
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

        self.game = game_controller
        self.ai_player = AIPlayer(self.game)  # Initialize AI Player
        self.last_placed_positions = []

        # Main frames
        self.board_frame = tk.Frame(root)
        self.board_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
        self.next_piece_frame = tk.Frame(root)
        self.next_piece_frame.pack(pady=20)  # Increased pady for next_piece_frame
        self.input_frame = tk.Frame(root)
        self.input_frame.pack(pady=20)      # Increased pady for input_frame

        # Labels
        self.score_label = tk.Label(root, text="Score: 0", font=FONT_LARGE)
        self.score_label.pack(pady=15)      # Increased pady for score_label
        self.remaining_pieces_label = tk.Label(root, text=f"Remaining Pieces: {len(self.game.piece_sequence.sequence)}",
                                               font=FONT_MEDIUM)
        self.remaining_pieces_label.pack(pady=15) # Increased pady for remaining_pieces_label
        self.status_label = tk.Label(root, text="", font=FONT_MEDIUM)
        self.status_label.pack(pady=10)     # Increased pady for status_label

        # User input fields
        input_font = FONT_MEDIUM
        tk.Label(self.input_frame, text="Row:", font=input_font).pack(side=tk.LEFT, padx=5) # Added padx
        self.row_entry = tk.Entry(self.input_frame, width=5, font=input_font)
        self.row_entry.pack(side=tk.LEFT, padx=5) # Added padx
        tk.Label(self.input_frame, text="Col:", font=input_font).pack(side=tk.LEFT, padx=5) # Added padx
        self.col_entry = tk.Entry(self.input_frame, width=5, font=input_font)
        self.col_entry.pack(side=tk.LEFT, padx=5) # Added padx

        # Buttons - Increased font and width
        self.manual_button = tk.Button(root, text="Play Manually", command=self.manual_play_gui, font=FONT_LARGE,
                                       width=BUTTON_WIDTH, padx=10, pady=10) # Increased pady for button
        self.manual_button.pack(pady=20)      # Increased pady for manual_button
        self.ai_button = tk.Button(root, text="Play AI Turn", command=self.play_ai_turn, font=FONT_LARGE, width=BUTTON_WIDTH)  # New AI button
        self.ai_button.pack(pady=10)

        # Initialize board and UI elements
        self.cells = {}
        self.update_board_display()
        self.update_next_piece_display()
        self.update_score_display()

    def update_board_display(self):
        """Updates the board display."""
        self._create_board_grid()
        self._update_cell_colors()

    def _create_board_grid(self):
        """Creates the board grid."""
        # Clear existing grid if any
        for widget in self.board_frame.winfo_children():
            widget.destroy()
        self.cells = {} # Reset cells dictionary

        # Configure grid to resize with frame
        for i in range(self.game.game_board.rows + 1): # +1 for row numbers
            self.board_frame.rowconfigure(i, weight=1)
        for j in range(self.game.game_board.cols + 1): # +1 for col numbers
            self.board_frame.columnconfigure(j, weight=1)

        for c in range(self.game.game_board.cols):
            col_label = tk.Label(self.board_frame, text=str(c), font=FONT_SMALL)
            col_label.grid(row=0, column=c + 1, padx=1, pady=1, sticky="ew") # sticky to fill cell

        for r in range(self.game.game_board.rows):
            row_label = tk.Label(self.board_frame, text=str(r), font=FONT_SMALL)
            row_label.grid(row=r + 1, column=0, padx=1, pady=1, sticky="ew") # sticky to fill cell
            for c in range(self.game.game_board.cols):
                if (r, c) not in self.cells:
                    cell_label = tk.Label(self.board_frame, width=2, height=1, relief=tk.SOLID,
                                          borderwidth=CELL_BORDER_WIDTH, font=FONT_SMALL)
                    cell_label.grid(row=r + 1, column=c + 1, padx=1, pady=1, sticky="nsew") # sticky to fill cell
                    cell_label.bind("<Button-1>", lambda event, row=r, col=c: self.on_cell_click(row, col))
                    cell_label.bind("<Enter>", lambda event, row=r, col=c: self.on_cell_enter(row, col))
                    cell_label.bind("<Leave>", lambda event, row=r, col=c: self.on_cell_leave(row, col))
                    self.cells[(r, c)] = cell_label

    def on_cell_enter(self, row, col):
        """Handles cell enter events."""
        self.cells[(row, col)].config(bg=HIGHLIGHT_COLOR)

    def on_cell_leave(self, row, col):
        """Handles cell leave events."""
        if (row, col) in self.last_placed_positions:
            self.cells[(row, col)].config(bg=CELL_COLORS["last_placed"])
        else:
            self.cells[(row, col)].config(bg=CELL_COLORS.get(self.game.game_board.board[row][col]))

    def on_cell_click(self, row, col):
        """Handles cell click events."""
        placed_positions = self.game.play(row, col)
        if placed_positions:
            self.last_placed_positions = placed_positions
            self.update_board_display()
            self.update_next_piece_display()
            self.update_score_display()
            self._update_remaining_pieces_label()
            self.status_label.config(text="Piece placed successfully.")
            self._check_game_status()
        else:
            self.status_label.config(text="Invalid move. Try again.")

    def _update_cell_colors(self):
        """Updates the colors of the cells."""
        for r in range(self.game.game_board.rows):
            for c in range(self.game.game_board.cols):
                cell_value = self.game.game_board.board[r][c]
                color = CELL_COLORS.get(cell_value, "white")
                if (r, c) in self.last_placed_positions:
                    color = "green"
                self.cells[(r, c)].config(bg=color)

    def update_next_piece_display(self):
        """Updates the next piece display."""
        self._clear_next_piece_frame()
        next_piece_info = self.game.piece_sequence.peek_next_piece()
        if next_piece_info:
            next_piece_name, next_piece_shape = next_piece_info
            tk.Label(self.next_piece_frame, text=f"Next Piece: {next_piece_name}", font=FONT_MEDIUM).pack()
            self._draw_next_piece_grid(next_piece_shape)
        else:
            tk.Label(self.next_piece_frame, text="No more pieces", font=FONT_MEDIUM).pack()

    def _clear_next_piece_frame(self):
        """Clears the next piece frame."""
        for widget in self.next_piece_frame.winfo_children():
            widget.destroy()

    def _draw_next_piece_grid(self, shape):
        """Draws the next piece grid."""
        piece_grid = tk.Frame(self.next_piece_frame)
        piece_grid.pack()
        for r in range(len(shape)):
            for c in range(len(shape[0])):
                color = "red" if shape[r][c] == 2 else "blue" if shape[r][c] == 1 else "white"
                tk.Label(piece_grid, width=2, height=1, relief=tk.SOLID, borderwidth=CELL_BORDER_WIDTH,
                         bg=color).grid(row=r, column=c, padx=1, pady=1)

    def update_score_display(self):
        """Updates the score label."""
        self.score_label.config(text=f"Score: {self.game.score}")

    def _update_remaining_pieces_label(self):
        """Updates the remaining pieces label."""
        self.remaining_pieces_label.config(text=f"Remaining Pieces: {len(self.game.piece_sequence.sequence)}")

    def manual_play_gui(self):
        """Handles manual piece placement from user input."""
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
            self._update_remaining_pieces_label()
            self.status_label.config(text="Piece placed successfully.")
            self.row_entry.delete(0, tk.END)
            self.col_entry.delete(0, tk.END)
            self._check_game_status()
        else:
            self.status_label.config(text="Invalid move. Try again.")

    def play_ai_turn(self):
        """
        Makes the AI play one step and updates the UI.
        """
        self._check_game_status()
        placed_positions = self.ai_player.play_step()
        if placed_positions:
            self.last_placed_positions = placed_positions
            self.update_board_display()
            self.update_next_piece_display()
            self.update_score_display()
            self._update_remaining_pieces_label()
            self.status_label.config(text="AI placed a piece successfully.")
            self._check_game_status()
        else:
            self.status_label.config(text="AI couldn't find a valid move.")

    def _check_game_status(self):
        """Checks the game status and displays a message if the game ends."""
        game_over_status = self.game.is_game_over()
        if game_over_status == "victory":
            messagebox.showinfo("Game Finished",
                                f"Congratulations! You placed all pieces. Victory!\nScore: {self.game.score}")
            self.manual_button.config(state=tk.DISABLED)
            self.ai_button.config(state=tk.DISABLED)
        elif game_over_status == "defeat":
            messagebox.showinfo("Game Over", f"Sorry! You have lost. Defeat!\nScore: {self.game.score}")
            self.manual_button.config(state=tk.DISABLED)
            self.ai_button.config(state=tk.DISABLED)