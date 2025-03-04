import copy

class GameState:
    def __init__(self, game_board, remaining_pieces):
        self.game_board = game_board
        self.board = copy.deepcopy(game_board.board)
        self.remaining_pieces = copy.deepcopy(remaining_pieces)

    def generate_successor(self, piece, row, col):
        new_board = copy.deepcopy(self.board)
        piece_rows = len(piece)
        piece_cols = len(piece[0])
        for r in range(piece_rows):
            for c in range(piece_cols):
                if piece[r][c] == 1:
                    new_board[row + r][col + c] = 1
        new_remaining_pieces = self.remaining_pieces[1:]
        return GameState(self.game_board.get_copy_with_new_board(new_board), new_remaining_pieces)

    def generate_successor_with_score(self, piece, row, col): # Modified to return score
        new_board = copy.deepcopy(self.board)
        piece_rows = len(piece)
        piece_cols = len(piece[0])
        for r in range(piece_rows):
            for c in range(piece_cols):
                if piece[r][c] == 1:
                    new_board[row + r][col + c] = 1 # Place piece
                elif piece[r][c] == 2:
                    new_board[row + r][col + c] = 2 # Place diamond if part of piece
        score_increase = self.clear_lines_score(new_board) # Calculate score increase from clearing lines
        new_remaining_pieces = self.remaining_pieces[1:]
        return GameState(self.game_board.get_copy_with_new_board(new_board), new_remaining_pieces), score_increase # Return new state and score

    def is_goal(self):
        return not self.remaining_pieces

    def get_possible_actions(self, piece):
        actions = []
        piece_rows = len(piece)
        piece_cols = len(piece[0])
        for r in range(self.game_board.rows - piece_rows + 1):
            for c in range(self.game_board.cols - piece_cols + 1):
                if self.can_place_piece(piece, r, c):
                    actions.append((r, c))
        return actions

    def can_place_piece(self, piece, top_left_row, top_left_col):
        piece_rows = len(piece)
        piece_cols = len(piece[0])
        if top_left_row < 0 or top_left_col < 0:
            return False
        if top_left_row + piece_rows > self.game_board.rows or top_left_col + piece_cols > self.game_board.cols:
            return False
        for r in range(piece_rows):
            for c in range(piece_cols):
                if piece[r][c] == 1 and self.board[top_left_row + r][top_left_col + c] == 1:
                    return False
        return True

    def calculate_potential_score(self, piece, row, col):
        """Calcula a pontuação potencial de colocar a peça na posição especificada."""
        temp_board = copy.deepcopy(self.board)
        piece_rows = len(piece)
        piece_cols = len(piece[0])
        for r in range(piece_rows):
            for c in range(piece_cols):
                if piece[r][c] == 1:
                    temp_board[row + r][col + c] = 1
        lines_cleared = self.clear_lines(temp_board)
        return lines_cleared * 10

    def clear_lines_score(self, board):
        """Checks and clears completed lines, returns score from diamonds in cleared lines."""
        lines_cleared = 0
        diamond_score = 0
        rows_to_clear = [r for r in range(len(board)) if all(cell in [1, 2] for cell in board[r])] # Check for 1 or 2
        cols_to_clear = [c for c in range(len(board[0])) if all(board[r][c] in [1, 2] for r in range(len(board)))] # Check for 1 or 2

        for r in rows_to_clear:
            diamond_score += board[r].count(2) * 10 # Add diamond score for row
            board[r] = [0] * len(board[0])
            lines_cleared += 1
        for c in cols_to_clear:
            for r in range(len(board)):
                if board[r][c] == 2: # Count diamonds in column
                    diamond_score += 10 # Add diamond score for column
                board[r][c] = 0
            lines_cleared += 1
        return (lines_cleared * 10) + diamond_score # Return total score (lines + diamonds)