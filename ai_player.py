import copy


class AIPlayer:
    """
    AI Player that plays the block game using different informed search algorithms.
    """

    def __init__(self, game_controller, search_algorithm="greedy"):
        """
        Initializes the AI Player with access to the game controller and a chosen search algorithm.
        """
        self.game_controller = game_controller
        self.search_algorithm = search_algorithm

    def heuristic(self, board, diamonds_obtained, lines_cleared):
        """
        Evaluates the board state using a heuristic function.
        """
        empty_spaces = sum(row.count(0) for row in board)
        return -(empty_spaces) + (lines_cleared * 10) + (diamonds_obtained * 10)

    def get_best_move(self):
        """
        Finds the best possible move based on the selected search algorithm.
        """
        if self.search_algorithm == "greedy":
            return self.greedy_search()
        # Additional algorithms can be added here
        return None

    def greedy_search(self):
        """
        Implements Greedy Best-First Search to select the best move.
        """
        best_move = None
        best_score = float('-inf')

        piece_name, piece = self.game_controller.piece_sequence.peek_next_piece()

        for r in range(self.game_controller.game_board.rows - len(piece) + 1):
            for c in range(self.game_controller.game_board.cols - len(piece[0]) + 1):
                if self.game_controller.can_place_piece(piece, r, c):

                    # Simulate placing the piece
                    simulated_board = copy.deepcopy(self.game_controller.game_board.board)
                    for pr in range(len(piece)):
                        for pc in range(len(piece[0])):
                            if piece[pr][pc] == 1:
                                simulated_board[r + pr][c + pc] = 1

                    # Check cleared lines and diamonds
                    lines_cleared, diamonds_obtained = self.evaluate_move(simulated_board)

                    # Compute heuristic score
                    score = self.heuristic(simulated_board, diamonds_obtained, lines_cleared)

                    # Update best move
                    if score > best_score:
                        best_score = score
                        best_move = (r, c)

        return best_move

    def evaluate_move(self, board):
        """
        Evaluates the result of placing a piece by checking cleared lines and diamonds.
        """
        lines_cleared = 0
        diamonds_obtained = 0

        # Check rows
        for r in range(len(board)):
            if all(cell in [1, 2] for cell in board[r]):
                lines_cleared += 1
                diamonds_obtained += board[r].count(2)
                board[r] = [0] * len(board[r])

        # Check columns
        for c in range(len(board[0])):
            if all(board[r][c] in [1, 2] for r in range(len(board))):
                lines_cleared += 1
                diamonds_obtained += sum(1 for r in range(len(board)) if board[r][c] == 2)
                for r in range(len(board)):
                    board[r][c] = 0

        return lines_cleared, diamonds_obtained

    def play_step(self):
        """
        Makes the AI play one step and returns placed positions.
        """
        best_move = self.get_best_move()
        if best_move:
            row, col = best_move
            placed_positions = self.game_controller.play(row, col)
            return placed_positions
        return None