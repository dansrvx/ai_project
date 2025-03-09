import copy
from logger_config import setup_logger

logger = setup_logger()


class GameController:
    """
    Manages the game logic, including piece placement, board updates, and game state checks.
    """

    def __init__(self, game_board, piece_sequence):
        """
        Initializes the game controller with a board, a sequence of pieces, and a search algorithm.
        """
        self.game_board = game_board
        self.piece_sequence = piece_sequence
        self.score = 0
        self.total_diamonds = self.calculate_total_diamonds_in_game()  # Initialize total_diamonds

    def can_place_piece(self, piece, top_left_row, top_left_col):
        """
        Checks if a piece can be placed at a given position without overlapping filled cells (1 or 2)
        or going out of bounds.
        """
        piece_rows = len(piece)
        piece_cols = len(piece[0])

        # Ensure the piece fits within the board boundaries
        if (top_left_row < 0 or top_left_col < 0 or
                top_left_row + piece_rows > self.game_board.rows or
                top_left_col + piece_cols > self.game_board.cols):
            return False

        # Check for overlapping filled cells
        for r in range(piece_rows):
            for c in range(piece_cols):
                piece_value = piece[r][c]
                board_value = self.game_board.board[top_left_row + r][top_left_col + c]

                # If the piece has a 1 or 2, it can only be placed over a 0 (empty space)
                if piece_value in [1, 2] and board_value != 0:
                    return False

        return True

    def place_piece(self, piece, top_left_row, top_left_col):
        """
        Places a piece on the board if the placement is valid and updates the game state.
        """
        if not self.can_place_piece(piece, top_left_row, top_left_col):
            return False

        piece_rows = len(piece)
        piece_cols = len(piece[0])

        for r in range(piece_rows):
            for c in range(piece_cols):
                if piece[r][c] == 1:
                    self.game_board.board[top_left_row + r][top_left_col + c] = 1
                elif piece[r][c] == 2:
                    self.game_board.board[top_left_row + r][top_left_col + c] = 2

        self.clear_completed_lines()
        return True

    def clear_completed_lines(self):
        """
        Clears completed rows and columns, updating the score based on the number of diamonds.
        """
        rows_cleared, diamond_score_rows = self.clear_rows()
        cols_cleared, diamond_score_cols = self.clear_cols()

        total_lines_cleared = rows_cleared + cols_cleared
        total_diamond_score = diamond_score_rows + diamond_score_cols

        self.score += (total_lines_cleared * 10) + total_diamond_score
        self.update_total_diamonds() # Update total_diamonds after clearing lines
        return total_lines_cleared

    def clear_rows(self):
        """
        Clears completed rows and calculates diamond-based score.
        """
        rows_to_clear = [r for r in range(self.game_board.rows) if
                         all(cell in [1, 2] for cell in self.game_board.board[r])]
        diamond_score = sum(self.game_board.board[r].count(2) * 10 for r in rows_to_clear)

        for r in rows_to_clear:
            self.game_board.board[r] = [0] * self.game_board.cols

        return len(rows_to_clear), diamond_score

    def clear_cols(self):
        """
        Clears completed columns and calculates diamond-based score.
        """
        cols_to_clear = [c for c in range(self.game_board.cols) if
                         all(self.game_board.board[r][c] in [1, 2] for r in range(self.game_board.rows))]
        diamond_score = sum(
            1 for c in cols_to_clear for r in range(self.game_board.rows) if self.game_board.board[r][c] == 2) * 10

        for c in cols_to_clear:
            for r in range(self.game_board.rows):
                self.game_board.board[r][c] = 0

        return len(cols_to_clear), diamond_score

    def is_game_over(self):
        """
        Determines if the game is over by checking victory or defeat conditions.
        """
        if not self.piece_sequence.sequence:
            return "victory"
        if self.is_defeat():
            return "defeat"
        return None

    def is_defeat(self):
        """
        Checks if there are no valid moves left, leading to defeat.
        """
        piece_name, piece = self.piece_sequence.peek_next_piece()
        piece_rows, piece_cols = len(piece), len(piece[0])

        for r in range(self.game_board.rows - piece_rows + 1):
            for c in range(self.game_board.cols - piece_cols + 1):
                if self.can_place_piece(piece, r, c):
                    logger.info(f"There is a valid move in ({r}, {c})")
                    return False  # A valid move exists
        return True  # No valid moves available

    def play(self, row, col):
        """
        Attempts to place the next piece at the specified position.
        Returns the positions of placed cells if successful, otherwise returns None.
        """
        piece_name, piece = self.piece_sequence.peek_next_piece()
        placed_positions = []

        if self.place_piece(piece, row, col):
            piece_rows = len(piece)
            piece_cols = len(piece[0])

            for r in range(piece_rows):
                for c in range(piece_cols):
                    if piece[r][c] == 1:
                        placed_positions.append((row + r, col + c))

            self.piece_sequence.get_next_piece()
            self.update_total_diamonds()  # Update total_diamonds after placing a piece
            return placed_positions

        return None

    def calculate_total_diamonds_in_game(self):
        """
        Calculates the total number of diamonds in the game (board + piece sequence).
        """
        board_diamonds = self.game_board.calculate_total_diamonds()
        sequence_diamonds = self.piece_sequence.calculate_total_diamonds()
        return board_diamonds + sequence_diamonds

    def update_total_diamonds(self):
        """
        Updates the total_diamonds attribute with the current number of diamonds in the game.
        """
        self.total_diamonds = self.calculate_total_diamonds_in_game()
        logger.info(f"Total Diamonds Updated: {self.total_diamonds}")