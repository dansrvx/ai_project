import copy
import numpy as np

from logger_config import setup_logger 

logger = setup_logger()


# Class to represent the game board and its operations
class GameBoard:
    def __init__(self, rows, cols):
        """
        Initializes the game board with the specified number of rows and columns.

        Args:
            rows (int): The number of rows on the board.
            cols (int): The number of columns on the board.
        """
        self.rows = rows  # Number of rows in the board
        self.cols = cols  # Number of columns in the board
        self.board = [[0 for _ in range(cols)] for _ in range(rows)]  # Initialize the board with all cells set to 0

    def initialize_board_state(self, fill_density=0.3, symmetric=False, edge_clear=True, sigma=2, diamond_rate=20):
        """
        Initializes the board state with parameters to control the initial fill density,
        symmetry, edge clearance, and places diamonds on the board based on diamond_rate.

        Args:
            fill_density (float): Controls how full the board will be initially (default is 0.3).
            symmetric (bool): If True, the board will be symmetric along the vertical axis.
            edge_clear (bool): If True, ensures that no border cells (edges of the board) are filled.
            sigma (float): The sigma value for the Gaussian filter (not used in this function, but could be used for clustering).
            diamond_rate (int): The rate of diamond appearance, affecting the probability of placing a diamond.
        """
        # Generate a random noise matrix for board initialization
        noise = np.random.rand(self.rows, self.cols)

        # Apply symmetry to the noise if requested
        if symmetric:
            for i in range(self.rows):
                for j in range(self.cols // 2):
                    avg = (noise[i, j] + noise[i, self.cols - j - 1]) / 2.0  # Average the values to create symmetry
                    noise[i, j] = avg
                    noise[i, self.cols - j - 1] = avg

        # Initialize the board with 1s and 0s based on the fill density
        self.board = [
            [1 if noise[r, c] < fill_density else 0 for c in range(self.cols)]
            for r in range(self.rows)
        ]

        # Ensure the edges of the board are empty (0)
        if edge_clear:
            for c in range(self.cols):
                self.board[0][c] = 0
                self.board[self.rows - 1][c] = 0
            for r in range(self.rows):
                self.board[r][0] = 0
                self.board[r][self.cols - 1] = 0

        # Place diamonds on cells with value 1 based on the diamond_rate
        for row in range(1, self.rows - 1):  # Avoid edges
            for col in range(1, self.cols - 1):  # Avoid edges
                if self.board[row][col] == 1 and np.random.randint(0, 100) < diamond_rate:
                    self.board[row][col] = 2  # Place a diamond (value 2) in the cell

    def get_copy_with_new_board(self, new_board):
        """
        Returns a copy of the GameBoard with a new board state.

        Args:
            new_board (list): The new board state to copy into the GameBoard.

        Returns:
            GameBoard: A new GameBoard object with the provided new board state.
        """
        new_game_board = GameBoard(self.rows, self.cols)  # Create a new GameBoard object
        new_game_board.board = new_board  # Set the new board state
        return new_game_board  # Return the new GameBoard

    def __deepcopy__(self, memo):
        """
        Creates a deep copy of the GameBoard object.

        Args:
            memo (dict): A memo dictionary to track already copied objects (used for deep copy).

        Returns:
            GameBoard: A new GameBoard object that is a deep copy of the current one.
        """
        new_board = GameBoard(self.rows, self.cols)  # Create a new GameBoard object
        new_board.board = copy.deepcopy(self.board, memo)  # Deep copy the board
        return new_board  # Return the deep copied GameBoard

    def calculate_total_diamonds(self):
        """
        Calculates the total number of diamonds present on the game board.
        Returns 0 if the board is empty or invalid.

        :return: The total number of diamonds (int), or 0 if the board is empty or invalid.
        """
        if not self.board or not isinstance(self.board, list):
            return 0  # Return 0 if the board is empty or not a list

        if not all(isinstance(row, list) for row in self.board):
            return 0  # Return 0 if any row is not a list

        total_diamonds = 0
        for row in self.board:
            total_diamonds += row.count(2)  # Count the occurrences of '2' (diamonds) in each row
        return total_diamonds
