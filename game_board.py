import copy
import numpy as np

class GameBoard:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.board = [[0 for _ in range(cols)] for _ in range(rows)]

    def initialize_board_state(self, fill_density=0.3, symmetric=False, edge_clear=True, sigma=2, diamond_rate=20):
        """
        Initializes the board state with parameters to control the initial fill density,
        symmetry, and edge clearance. Also adds diamonds to the board based on diamond_rate,
        only on cells that were previously defined as 1.

        Args:
            fill_density (float): Controls how full the board will be initially (default 0.3).
            symmetric (bool): If True, the board will be symmetric along the vertical axis.
            edge_clear (bool): If True, ensures that no border cells (edges of the board) are filled.
            sigma (float): The sigma value for the Gaussian filter used to create clusters.
            diamond_rate (int): The rate of diamond appearance, affecting the probability of placing a diamond.
        """
        noise = np.random.rand(self.rows, self.cols)

        if symmetric:
            for i in range(self.rows):
                for j in range(self.cols // 2):
                    avg = (noise[i, j] + noise[i, self.cols - j - 1]) / 2.0
                    noise[i, j] = avg
                    noise[i, self.cols - j - 1] = avg

        self.board = [
            [1 if noise[r, c] < fill_density else 0 for c in range(self.cols)]
            for r in range(self.rows)
        ]

        if edge_clear:
            for c in range(self.cols):
                self.board[0][c] = 0
                self.board[self.rows - 1][c] = 0
            for r in range(self.rows):
                self.board[r][0] = 0
                self.board[r][self.cols - 1] = 0

        # Diamond placement only on cells with value 1
        for row in range(1, self.rows - 1):  # Avoid edges
            for col in range(1, self.cols - 1):  # Avoid edges
                if self.board[row][col] == 1 and np.random.randint(0, 100) < diamond_rate:
                    self.board[row][col] = 2

    def clear_completed_lines(self):
        lines_cleared = 0
        rows_to_clear = [r for r in range(self.rows) if all(cell == 1 for cell in self.board[r])]
        cols_to_clear = [c for c in range(self.cols) if all(self.board[r][c] == 1 for r in range(self.rows))]

        for r in rows_to_clear:
            self.board[r] = [0] * self.cols
            lines_cleared += 1

        for c in cols_to_clear:
            for r in range(self.rows):
                self.board[r][c] = 0
            lines_cleared += 1

        return lines_cleared

    def get_copy_with_new_board(self, new_board):
        """Retorna uma cópia do GameBoard com um novo tabuleiro."""
        new_game_board = GameBoard(self.rows, self.cols)
        new_game_board.board = new_board
        return new_game_board
    
    def __deepcopy__(self, memo):
        new_board = GameBoard(self.rows, self.cols)
        new_board.board = copy.deepcopy(self.board, memo)
        return new_board