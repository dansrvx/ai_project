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

        # Check for overlapping filled cells or diamonds
        for r in range(piece_rows):
            for c in range(piece_cols):
                if piece[r][c] == 1 and (self.game_board.board[top_left_row + r][top_left_col + c] == 1 or
                                         self.game_board.board[top_left_row + r][top_left_col + c] == 2):
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
        """Clears completed rows and columns, calculating the score based on diamonds."""
        rows_cleared, diamond_score_rows = self._clear_rows()
        cols_cleared, diamond_score_cols = self._clear_cols()
        total_lines_cleared = rows_cleared + cols_cleared
        total_diamond_score = diamond_score_rows + diamond_score_cols
        self.score += (total_lines_cleared * 10) + total_diamond_score
        return total_lines_cleared

    def _clear_rows(self):
        """Clears completed rows and calculates diamond score."""
        rows_to_clear = [r for r in range(self.game_board.rows) if all(cell == 1 or cell == 2 for cell in self.game_board.board[r])]
        diamond_score = 0
        for r in rows_to_clear:
            diamond_score += self.game_board.board[r].count(2) * 10
            self.game_board.board[r] = [0] * self.game_board.cols
        return len(rows_to_clear), diamond_score

    def _clear_cols(self):
        """Clears completed columns and calculates diamond score."""
        cols_to_clear = [c for c in range(self.game_board.cols) if all(self.game_board.board[r][c] == 1 or self.game_board.board[r][c] == 2 for r in range(self.game_board.rows))]
        diamond_score = 0
        for c in cols_to_clear:
            diamond_score += sum(1 for r in range(self.game_board.rows) if self.game_board.board[r][c] == 2) * 10
            for r in range(self.game_board.rows):
                self.game_board.board[r][c] = 0
        return len(cols_to_clear), diamond_score

    def is_game_over(self):
        """Checks if the game is over."""
        if not self.piece_sequence.sequence:
            return "victory"
        if self._is_defeat():
            return "defeat"
        return None

    def _is_defeat(self):
        """Checks if the game is lost."""
        for _, piece in self.piece_sequence.sequence:
            piece_rows, piece_cols = len(piece), len(piece[0])
            for r in range(self.game_board.rows - piece_rows + 1):
                for c in range(self.game_board.cols - piece_cols + 1):
                    if self.can_place_piece(piece, r, c):
                        return False  # Found a valid move
        return True  # No valid moves found

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