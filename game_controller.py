import copy
from game_state import GameState


class GameController:
    def __init__(self, game_board, piece_sequence, search_algorithm):
        self.game_board = game_board
        self.piece_sequence = piece_sequence
        self.search_algorithm = search_algorithm
        self.score = 0

    def play_game(self):
        initial_state = GameState(self.game_board, self.piece_sequence.sequence)
        solution = self.search_algorithm.search(initial_state)

        if solution:
            for piece_name, row, col in solution:
                piece = self.piece_sequence.piece_definitions[piece_name]
                self.place_piece(piece, row, col)
                self.piece_sequence.sequence.pop(0)
            return True
        else:
            return False

    def can_place_piece(self, piece, top_left_row, top_left_col):
        piece_rows = len(piece)
        piece_cols = len(piece[0])

        # Check if the piece fits within the board boundaries
        if top_left_row < 0 or top_left_col < 0:
            return False
        if top_left_row + piece_rows > self.game_board.rows or top_left_col + piece_cols > self.game_board.cols:
            return False

        # Check for overlapping filled cells
        for r in range(piece_rows):
            for c in range(piece_cols):
                if piece[r][c] == 1 and self.game_board.board[top_left_row + r][top_left_col + c] == 1:
                    return False
        return True

    def place_piece(self, piece, top_left_row, top_left_col):
        if not self.can_place_piece(piece, top_left_row, top_left_col):
            return False
        piece_rows = len(piece)
        piece_cols = len(piece[0])
        for r in range(piece_rows):
            for c in range(piece_cols):
                if piece[r][c] == 1:
                    self.game_board.board[top_left_row + r][top_left_col + c] = 1
        self.clear_completed_lines()
        return True

    def clear_completed_lines(self):
        """
        Clears completed rows and columns, calculating the score based on diamonds.
        """
        lines_cleared = 0
        diamond_score = 0
        rows_to_clear = [r for r in range(len(self.game_board.board)) if
                         all(cell == 1 or cell == 2 for cell in self.game_board.board[r])]
        cols_to_clear = [c for c in range(len(self.game_board.board[0])) if all(
            self.game_board.board[r][c] == 1 or self.game_board.board[r][c] == 2 for r in
            range(len(self.game_board.board)))]

        for r in rows_to_clear:
            diamond_score += self.game_board.board[r].count(2) * 10  # Count diamonds in the row
            self.game_board.board[r] = [0] * len(self.game_board.board[0])
            lines_cleared += 1

        for c in cols_to_clear:
            diamond_score += sum(1 for r in range(len(self.game_board.board)) if
                                 self.game_board.board[r][c] == 2) * 10  # Count diamonds in the column
            for r in range(len(self.game_board.board)):
                self.game_board.board[r][c] = 0
            lines_cleared += 1

        self.score += (lines_cleared * 10) + diamond_score  # Update total score
        return lines_cleared

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
            for r in range(self.game_board.rows - piece_rows + 1):
                for c in range(self.game_board.cols - piece_cols + 1):
                    if self.can_place_piece(piece, r, c):
                        return None  # A valid move exists, game is not over
        # If no valid placement is found for any piece, it's a defeat.
        return "defeat"

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

    def manual_play(self, row, col):
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
            return placed_positions
        else:
            return None