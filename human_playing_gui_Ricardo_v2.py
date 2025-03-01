import tkinter as tk
from tkinter import messagebox
import random
import numpy as np
import scipy.ndimage as ndimage
import random
import copy

class GameBoard:
    def __init__(self, rows, cols):
        """
        Initializes the game board.

        Args:
            rows (int): Number of rows in the board.
            cols (int): Number of columns in the board.
        """
        self.rows = rows
        self.cols = cols
        self.board = [[0 for _ in range(cols)] for _ in range(rows)]

    def display(self):
        """
        Displays the board using filled block characters for filled cells and dots for empty ones.
        Includes row and column numbers for better readability.
        """
        # Print column numbers
        print("  ", end=" ") # Space for row numbers column
        for c in range(self.cols):
            print(f"{c:<2}", end="") # Column numbers aligned to the left with width 2
        print() # New line after column numbers

        print("  ", end=" ") # Space for row numbers column
        for _ in range(self.cols):
            print("--", end="") # Separator line under column numbers
        print("-") # New line and closing separator

        for r in range(self.rows):
            print(f"{r:<2}|", end=" ") # Row numbers aligned to the left with width 2 and separator
            for cell in self.board[r]:
                if cell == 1:
                    print("█", end=" ")  # Filled cell block
                else:
                    print("·", end=" ")  # Empty cell symbol
            print()

    def initialize_board_state(self, fill_density=0.5, symmetric=False, edge_clear=True, sigma=2):
        """
        Initializes the board state with parameters to control the initial fill density,
        symmetry, and edge clearance.

        Args:
            fill_density (float): Controls how full the board will be initially (default 0.3).
            symmetric (bool): If True, the board will be symmetric along the vertical axis.
            edge_clear (bool): If True, ensures that no border cells (edges of the board) are filled.
            sigma (float): The sigma value for the Gaussian filter used to create clusters.
        """
        # Generate random noise for each cell
        noise = np.random.rand(self.rows, self.cols)

        # If symmetry is requested, enforce vertical symmetry by averaging each cell with its mirror cell.
        if symmetric:
            for i in range(self.rows):
                for j in range(self.cols // 2):
                    # Calculate the average value for the cell and its mirror counterpart.
                    avg = (noise[i, j] + noise[i, self.cols - j - 1]) / 2.0
                    noise[i, j] = avg
                    noise[i, self.cols - j - 1] = avg

        # Apply Gaussian smoothing to the noise to create clusters
        smoothed_noise = ndimage.gaussian_filter(noise, sigma=sigma)

        # Create the board by thresholding the smoothed noise with fill_density
        self.board = [
            [1 if smoothed_noise[r, c] < fill_density else 0 for c in range(self.cols)]
            for r in range(self.rows)
        ]

        # If edge_clear is True, ensure the entire border of the board is empty
        if edge_clear:
            # Clear the first and last rows
            for c in range(self.cols):
                self.board[0][c] = 0
                self.board[self.rows - 1][c] = 0
            # Clear the first and last columns
            for r in range(self.rows):
                self.board[r][0] = 0
                self.board[r][self.cols - 1] = 0


# Define the available piece types and their shapes
piece_definitions = {
    'L': [
        [1, 0],
        [1, 0],
        [1, 1]
    ],
    'I': [
        [1],
        [1],
        [1]
    ],
    'T': [
        [0, 1, 0],
        [1, 1, 1]
    ],
    'Square': [
        [1, 1],
        [1, 1]
    ],
    'Z': [
        [1, 1, 0],
        [0, 1, 1]
    ],
    'S': [
        [0, 1, 1],
        [1, 1, 0]
    ],
    'J': [  # Mirror of L
        [0, 1],
        [0, 1],
        [1, 1]
    ],
    'L_reverse': [  # L rotated - included for variety
        [1, 1, 1],
        [1, 0, 0]
    ],
    'T_reverse': [ # T rotated - included for variety
        [1, 1],
        [0, 1],
        [1, 1]
    ]
    # Add more piece types here as needed
}

class PieceSequence:
    def __init__(self, piece_definitions, sequence_length=10):
        """
        Initializes the piece sequence.

        Args:
            piece_definitions (dict): Dictionary mapping piece names to their shape matrices.
            sequence_length (int): The number of pieces in the sequence.
        """
        self.piece_definitions = piece_definitions
        self.sequence_length = sequence_length
        self.sequence = []
        self.generate_sequence()

    def generate_sequence(self):
        """
        Generates a random sequence of pieces.
        Each piece is represented as a tuple (piece_name, piece_shape),
        where piece_shape is a deep copy of the defined shape.
        """
        self.sequence = []
        piece_types = list(self.piece_definitions.keys())
        for _ in range(self.sequence_length):
            # Randomly choose a piece type
            chosen_piece = random.choice(piece_types)
            # Make a deep copy of the piece shape to avoid modifying the original
            piece_shape = copy.deepcopy(self.piece_definitions[chosen_piece])
            self.sequence.append((chosen_piece, piece_shape))

    def get_next_piece(self):
        """
        Retrieves and removes the next piece from the sequence.
        If the sequence is empty, a new sequence is generated.

        Returns:
            tuple: A tuple (piece_name, piece_shape)
        """
        if not self.sequence:
            self.generate_sequence()
        return self.sequence.pop(0)

    def peek_next_piece(self):
        """
        Returns the next piece in the sequence without removing it.

        Returns:
            tuple: A tuple (piece_name, piece_shape) or None if the sequence is empty.
        """
        if self.sequence:
            return self.sequence[0]
        return None


def display_piece_shape(piece_shape):
    """Helper function to display a piece shape nicely in text."""
    for row in piece_shape:
        for cell in row:
            if cell == 1:
                print("█", end=" ")
            else:
                print("  ", end=" ") # Two spaces for empty cell alignment
        print()


class Game:
    def __init__(self, board, piece_sequence):
        """
        Initializes the game with a board and a piece sequence.

        Args:
            board (GameBoard): The game board.
            piece_sequence (PieceSequence): The sequence of pieces to be placed.
        """
        self.board = board
        self.piece_sequence = piece_sequence
        self.score = 0

    def can_place_piece(self, piece, top_left_row, top_left_col):
        """
        Checks if a piece can be placed on the board at the specified top-left position.

        Args:
            piece (list[list[int]]): 2D matrix representing the piece shape.
            top_left_row (int): The top row index where the piece will be placed.
            top_left_col (int): The left column index where the piece will be placed.

        Returns:
            bool: True if the piece can be placed, False otherwise.
        """
        piece_rows = len(piece)
        piece_cols = len(piece[0])

        # Check if the piece fits within the board boundaries
        if top_left_row < 0 or top_left_col < 0:
            return False
        if top_left_row + piece_rows > self.board.rows or top_left_col + piece_cols > self.board.cols:
            return False

        # Check for overlapping filled cells
        for r in range(piece_rows):
            for c in range(piece_cols):
                if piece[r][c] == 1 and self.board.board[top_left_row + r][top_left_col + c] == 1:
                    return False
        return True

    def place_piece(self, piece, top_left_row, top_left_col):
        """
        Places a piece on the board if possible.
        Updates the board and clears any complete rows or columns.

        Args:
            piece (list[list[int]]): 2D matrix representing the piece shape.
            top_left_row (int): The top row index where the piece will be placed.
            top_left_col (int): The left column index where the piece will be placed.

        Returns:
            bool: True if the piece was successfully placed, False otherwise.
        """
        if not self.can_place_piece(piece, top_left_row, top_left_col):
            return False

        piece_rows = len(piece)
        piece_cols = len(piece[0])
        # Place the piece on the board
        for r in range(piece_rows):
            for c in range(piece_cols):
                if piece[r][c] == 1:
                    self.board.board[top_left_row + r][top_left_col + c] = 1

        # After placing, clear any fully completed rows or columns and update score
        lines_cleared = self.clear_completed_lines()
        self.score += lines_cleared * 10
        return True

    def clear_completed_lines(self):
        """
        Clears any row or column that is completely filled.
        A cleared row or column is replaced by empty cells.
        Returns the number of lines cleared.
        """
        lines_cleared = 0
        # Clear full rows
        rows_to_clear = []
        for r in range(self.board.rows):
            if all(cell == 1 for cell in self.board.board[r]):
                rows_to_clear.append(r)

        for r in rows_to_clear:
            self.board.board[r] = [0] * self.board.cols
            lines_cleared += 1

        # Clear full columns
        cols_to_clear = []
        for c in range(self.board.cols):
            if all(self.board.board[r][c] == 1 for r in range(self.board.rows)):
                cols_to_clear.append(c)

        for c in cols_to_clear:
            for r in range(self.board.rows):
                self.board.board[r][c] = 0
            lines_cleared += 1 # Increment lines_cleared for columns as well

        return lines_cleared


    def play_next_piece(self, top_left_row, top_left_col):
        """
        Retrieves the next piece from the sequence and attempts to place it at the specified position.

        Args:
            top_left_row (int): The top row index for the piece placement.
            top_left_col (int): The left column index for the piece placement.

        Returns:
            bool: True if the piece was placed successfully, False otherwise.
        """
        piece_name, piece = self.piece_sequence.get_next_piece()
        if self.place_piece(piece, top_left_row, top_left_col):
            return True
        else:
            return False

    def is_game_over(self):
        """
        Checks if the game is over.
        Returns:
            str: "victory" if all pieces have been placed,
                 "defeat" if none of the remaining pieces can be placed on the board,
                 None if the game is still in progress.
        """
        # Victory condition: no remaining pieces in the sequence
        if not self.piece_sequence.sequence:
            return "victory"

        # Defeat condition: check if any remaining piece can be placed anywhere on the board.
        for (piece_name, piece) in self.piece_sequence.sequence:
            piece_rows = len(piece)
            piece_cols = len(piece[0])
            # Iterate over all possible top-left positions where the piece could fit
            for r in range(self.board.rows - piece_rows + 1):
                for c in range(self.board.cols - piece_cols + 1):
                    if self.can_place_piece(piece, r, c):
                        return None  # A valid move exists, game is not over
        # If no valid placement is found for any piece, it's a defeat.
        return "defeat"


class GameGUI:
    def __init__(self, root, game):
        self.root = root
        self.root.title("Block Placement Game")
        self.game = game

        # Get window width and height after widgets are created but before mainloop starts
        root.update() # Force window to update and get its size
        window_width = root.winfo_width()
        window_height = root.winfo_height()

        # Calculate cell size to fit board in window, with some padding
        board_padding_fraction = 0.1 # 10% padding on each side (total 20% padding)
        available_board_width = window_width * (1 - board_padding_fraction)
        available_board_height = window_height * (0.6 - board_padding_fraction) # Reduce height for other UI elements
        # Reduce height further to account for other UI elements above and below the board.
        # 0.6 is an approximate fraction, adjust as needed.

        cell_size_width = available_board_width / game.board.cols
        cell_size_height = available_board_height / game.board.rows
        self.cell_size = int(min(cell_size_width, cell_size_height)) # Choose smaller to fit in both dimensions and make integer

        if self.cell_size < 5: # Minimum cell size to be somewhat visible
            self.cell_size = 5

        self.board_frame = tk.Frame(root)
        self.board_frame.pack(pady=20)
        self.cells = {} # Store GUI cell elements
        self.row_labels = {} # Store row number labels
        self.col_labels = {} # Store column number labels


        self.next_piece_frame = tk.Frame(root)
        self.next_piece_frame.pack(pady=10)
        self.next_piece_labels = []

        self.score_label = tk.Label(root, text="Score: 0", font=("Arial", 16) )
        self.score_label.pack(pady=10)

        self.status_label = tk.Label(root, text="", font=("Arial", 12))
        self.status_label.pack(pady=5)

        self.input_frame = tk.Frame(root)
        self.input_frame.pack(pady=10)
        tk.Label(self.input_frame, text="Row:", font=("Arial", 12)).pack(side=tk.LEFT)
        self.row_entry = tk.Entry(self.input_frame, width=5, font=("Arial", 12))
        self.row_entry.pack(side=tk.LEFT)
        tk.Label(self.input_frame, text="Col:", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
        self.col_entry = tk.Entry(self.input_frame, width=5, font=("Arial", 12))
        self.col_entry.pack(side=tk.LEFT)

        self.place_button = tk.Button(root, text="Place Piece", command=self.place_piece_gui, font=("Arial", 14))
        self.place_button.pack(pady=10)

        self.update_board_display()
        self.update_next_piece_display()
        self.update_score_display()


    def update_board_display(self):
        """Updates the visual representation of the game board, including row and column numbers."""

        # Column numbers (above the board)
        for c in range(self.game.board.cols):
            if c not in self.col_labels:
                col_label = tk.Label(self.board_frame, text=str(c), font=("Arial", max(self.cell_size // 4, 6)))
                col_label.grid(row=0, column=c + 1, padx=1, pady=1) # row=0 for column numbers, offset columns by 1
                self.col_labels[c] = col_label # Store column labels
            self.col_labels[c].config(text=str(c)) # In case board size is dynamic, update if needed


        # Row numbers (to the left of the board) and board cells
        for r in range(self.game.board.rows):
            # Row number label
            if r not in self.row_labels:
                row_label = tk.Label(self.board_frame, text=str(r), font=("Arial", max(self.cell_size // 4, 6)))
                row_label.grid(row=r + 1, column=0, padx=1, pady=1) # column=0 for row numbers, offset rows by 1
                self.row_labels[r] = row_label # Store row labels
            self.row_labels[r].config(text=str(r)) # Update if needed

            for c in range(self.game.board.cols):
                if (r, c) not in self.cells:
                    cell_label = tk.Label(self.board_frame, width=2, height=1, relief=tk.SOLID, borderwidth=1, font=("Arial", max(self.cell_size // 4, 6))) # Ensure minimum font size
                    cell_label.grid(row=r + 1, column=c + 1, padx=1, pady=1) # Offset both row and column by 1
                    self.cells[(r, c)] = cell_label # Store label in cells dictionary
                cell = self.game.board.board[r][c]
                if cell == 1:
                    self.cells[(r, c)].config(bg="blue") # Filled cell color
                else:
                    self.cells[(r, c)].config(bg="white") # Empty cell color


    def update_next_piece_display(self):
        """Updates the display of the next piece."""
        for label in self.next_piece_labels:
            label.destroy()
        self.next_piece_labels = []

        next_piece_info = self.game.piece_sequence.peek_next_piece()
        if next_piece_info:
            next_piece_name, next_piece_shape = next_piece_info

            name_label = tk.Label(self.next_piece_frame, text=f"Next Piece: {next_piece_name}", font=("Arial", 12))
            name_label.pack()
            self.next_piece_labels.append(name_label)

            piece_grid_frame = tk.Frame(self.next_piece_frame)
            piece_grid_frame.pack()
            self.next_piece_labels.append(piece_grid_frame)

            for r in range(len(next_piece_shape)):
                for c in range(len(next_piece_shape[0])):
                    cell_val = next_piece_shape[r][c]
                    color = "blue" if cell_val == 1 else "white"
                    piece_cell_label = tk.Label(piece_grid_frame, width=2, height=1, relief=tk.SOLID, borderwidth=1, bg=color)
                    piece_cell_label.grid(row=r, column=c, padx=1, pady=1)
                    self.next_piece_labels.append(piece_cell_label)
        else:
            no_piece_label = tk.Label(self.next_piece_frame, text="No more pieces", font=("Arial", 12))
            no_piece_label.pack()
            self.next_piece_labels.append(no_piece_label)


    def update_score_display(self):
        """Updates the score label in the GUI."""
        self.score_label.config(text=f"Score: {self.game.score}")

    def place_piece_gui(self):
        """Handles the piece placement when the button is pressed in GUI."""
        try:
            row = int(self.row_entry.get())
            col = int(self.col_entry.get())
        except ValueError:
            self.status_label.config(text="Invalid input: Row and Col must be integers.")
            return

        if not (0 <= row < self.game.board.rows and 0 <= col < self.game.board.cols):
            self.status_label.config(text=f"Invalid input: Row and Col must be within board bounds (0 to {self.game.board.rows - 1} and 0 to {self.game.board.cols - 1}).")
            return

        next_piece_info = self.game.piece_sequence.peek_next_piece()
        if not next_piece_info: # Should not happen if game over is checked correctly, but for safety
            return

        next_piece_name, next_piece_shape = next_piece_info

        if self.game.play_next_piece(row, col):
            self.update_board_display()
            self.update_next_piece_display()
            self.update_score_display()
            self.status_label.config(text="Piece placed successfully.")
            self.row_entry.delete(0, tk.END) # Clear input fields
            self.col_entry.delete(0, tk.END)

            game_over_status = self.game.is_game_over()
            if game_over_status == "victory":
                messagebox.showinfo("Game Over", "Congratulations! You placed all pieces. Victory!\nScore: " + str(self.game.score), font=("Arial", 14))
                self.place_button.config(state=tk.DISABLED) # Disable further play
            elif game_over_status == "defeat":
                messagebox.showinfo("Game Over", "Game Over. No more valid moves. Defeat!\nScore: " + str(self.game.score), font=("Arial", 14))
                self.place_button.config(state=tk.DISABLED) # Disable further play


        else:
            self.status_label.config(text="Could not place piece at the specified location. Try again.")


if __name__ == '__main__':
    # Initialize game parameters
    rows = 10  # Board size is still adjustable here
    cols = 10
    sequence_length = 15

    # Create game board and initialize its state
    game_board = GameBoard(rows, cols)
    game_board.initialize_board_state(fill_density=0.5, symmetric=False, edge_clear=True, sigma=1)

    # Create piece sequence
    piece_sequence = PieceSequence(piece_definitions, sequence_length=sequence_length)

    # Initialize the game
    game = Game(game_board, piece_sequence)

    # Initialize Tkinter root
    root = tk.Tk()
    # No need to set root.geometry anymore, window will adjust to content

    gui = GameGUI(root, game)

    # Start the GUI event loop
    root.mainloop()