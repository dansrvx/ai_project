import copy
from logger_config import setup_logger # Importe o modulo de configuração.

logger = setup_logger() # Configura o logger

class PlayTreeNode:
    """
    Represents a node in the play tree, storing information about a move.
    """

    def __init__(self, game_controller, piece_name, piece_shape, position, parent=None):
        self.game_controller = game_controller  # Each node has its own game controller
        self.piece_name = piece_name  # The name of the piece placed at this step
        self.piece_shape = piece_shape  # The shape of the piece placed at this step
        self.position = position  # (row, col) position where the piece was placed
        self.children = []  # List of child nodes (future plays)
        self.parent = parent  # Parent node in the tree
        self.cost = self.calculate_cost()
        self.heuristic = self.calculate_heuristic()
        self.game_status = self.evaluate_game_status()  # Determines if the game can continue, is stuck, or has ended

    def add_child(self, child_node):
        """Adds a child node to the current node."""
        self.children.append(child_node)

    def calculate_cost(self):
        """Calculates the cost of placing the piece, penalizing empty inaccessible spaces."""
        empty_spaces = sum(row.count(0) for row in self.game_controller.game_board.board)
        blocked_spaces = self.count_inaccessible_spaces()
        return (empty_spaces + blocked_spaces)  # Higher penalty for blocked spaces

    def calculate_heuristic(self):
        """Calculates the heuristic value for this node using GameController's scoring system."""
        initial_score = self.parent.game_controller.score if self.parent else 0
        temp_game_controller = copy.deepcopy(self.game_controller)
        temp_game_controller.clear_completed_lines()
        return temp_game_controller.score - initial_score

    def evaluate_game_status(self):
        """Determines the game status using GameController's logic."""
        return self.game_controller.is_game_over()

    def count_inaccessible_spaces(self):
        """Counts the number of small empty gaps that cannot fit any available piece."""
        inaccessible_count = 0
        piece_sizes = self.get_piece_sizes()

        for r in range(self.game_controller.game_board.rows):
            for c in range(self.game_controller.game_board.cols):
                if self.game_controller.game_board.board[r][c] == 0:
                    # Check horizontal gaps
                    if c < self.game_controller.game_board.cols - 1 and self.game_controller.game_board.board[r][
                        c + 1] == 0:
                        gap_size = self.measure_gap(r, c, direction="horizontal")
                        if gap_size not in piece_sizes:
                            inaccessible_count += 1

                    # Check vertical gaps
                    if r < self.game_controller.game_board.rows - 1 and self.game_controller.game_board.board[r + 1][
                        c] == 0:
                        gap_size = self.measure_gap(r, c, direction="vertical")
                        if gap_size not in piece_sizes:
                            inaccessible_count += 1

        return inaccessible_count

    def measure_gap(self, row, col, direction):
        """Measures the size of a continuous empty gap in the specified direction."""
        gap_size = 0
        if direction == "horizontal":
            while col < self.game_controller.game_board.cols and self.game_controller.game_board.board[row][col] == 0:
                gap_size += 1
                col += 1
        elif direction == "vertical":
            while row < self.game_controller.game_board.rows and self.game_controller.game_board.board[row][col] == 0:
                gap_size += 1
                row += 1
        return gap_size

    def get_piece_sizes(self):
        """Returns a set of unique piece sizes available in the game."""
        sizes = set()
        for piece in self.game_controller.piece_sequence.piece_definitions.values():
            sizes.add(len(piece))  # Height of the piece
            sizes.add(len(piece[0]))  # Width of the piece
        return sizes


class PlayTree:
    """
    Generates and manages a tree of possible moves up to a given depth.
    """

    def __init__(self, game_controller, depth):
        """
        Initializes the play tree with a given game controller and depth.
        """
        self.depth = depth  # Maximum depth of the play tree
        root_game_controller = copy.deepcopy(game_controller)  # Ensure the original game state is not modified
        self.root = PlayTreeNode(root_game_controller, None, None, None)  # Root node
        self.build_tree(self.root, 0)

    def build_tree(self, node, current_depth):
        """
        Recursively generates the play tree up to the specified depth.
        """
        if current_depth >= self.depth or not node.game_controller.piece_sequence.sequence or node.game_status:
            return  # Stop if maximum depth is reached, no pieces left, or game is over

        piece_name, piece_shape = node.game_controller.piece_sequence.peek_next_piece()

        for r in range(node.game_controller.game_board.rows - len(piece_shape) + 1):
            for c in range(node.game_controller.game_board.cols - len(piece_shape[0]) + 1):
                if node.game_controller.can_place_piece(piece_shape, r, c):
                    temp_game_controller = copy.deepcopy(node.game_controller)  # Create a new game state for this move
                    temp_game_controller.play(r, c)  # Simulate placing the piece

                    child_node = PlayTreeNode(temp_game_controller, piece_name, piece_shape, (r, c), parent=node)
                    node.add_child(child_node)
                    self.build_tree(child_node, current_depth + 1)

    def get_tree(self):
        """Returns the root of the play tree."""
        return self.root

    def print_tree(self, node=None, depth=0):
        """Prints the play tree structure to the console, including piece shapes and heuristics."""
        if node is None:
            node = self.root

        indent = "  " * depth
        if node.piece_name:
            logger.info(
                f"{indent}- Piece: {node.piece_name} at Position: {node.position} (Cost: {node.cost}, Heuristic: {node.heuristic}), {node.game_status}")
            for row in node.piece_shape:
                logger.info(f"{indent}  {row}")
        else:
            logger.info(f"{indent}- Root Node (Initial State)")

        for child in node.children:
            self.print_tree(child, depth + 1)
