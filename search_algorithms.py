import heapq
from abc import ABC, abstractmethod
from collections import deque
import copy

class SearchAlgorithm(ABC):
    @abstractmethod
    def search(self, game_state):
        pass

class UniformCostSearch(SearchAlgorithm):
    def search(self, game_state):
        start_state = game_state
        priority_queue = [(0, start_state, [])]
        visited = set()

        while priority_queue:
            cost, current_state, path = heapq.heappop(priority_queue)
            board_tuple = tuple(map(tuple, current_state.board))

            if board_tuple in visited:
                continue
            visited.add(board_tuple)

            if current_state.is_goal():
                return path

            piece_name, piece = current_state.remaining_pieces[0]
            actions = current_state.get_possible_actions(piece)

            for row, col in actions:
                successor = current_state.generate_successor(piece, row, col)
                new_cost = cost + 1
                new_path = path + [(piece_name, row, col)]
                heapq.heappush(priority_queue, (new_cost, successor, new_path))

        return None

class AStarSearch(SearchAlgorithm):
    def search(self, game_state):
        def heuristic(state):
            """Heuristic function that considers potential score and remaining pieces."""
            if not state.remaining_pieces:
                return 0
            piece_name, piece = state.remaining_pieces[0]
            actions = state.get_possible_actions(piece)
            if not actions:
                return len(state.remaining_pieces) * 100 # Penalize states with no actions.
            best_score = 0
            for row, col in actions:
                score = state.calculate_potential_score(piece, row, col)
                best_score = max(best_score, score)
            return -best_score + len(state.remaining_pieces)

        start_state = game_state
        priority_queue = [(heuristic(start_state), 0, 0, start_state, [])]  # (f(n), g(n), counter, state, path)
        visited = set()
        counter = 0 # Counter to break ties in priority queue

        while priority_queue:
            f, g, _, current_state, path = heapq.heappop(priority_queue)
            board_tuple = tuple(map(tuple, current_state.board))

            if board_tuple in visited:
                continue
            visited.add(board_tuple)

            if current_state.is_goal():
                return path

            piece_name, piece = current_state.remaining_pieces[0]
            actions = current_state.get_possible_actions(piece)

            for row, col in actions:
                successor = current_state.generate_successor(piece, row, col)
                new_g = g + 1
                h = heuristic(successor)
                new_f = new_g + h
                new_path = path + [(piece_name, row, col)]
                counter += 1 # Increment counter
                heapq.heappush(priority_queue, (new_f, new_g, counter, successor, new_path)) # Add counter

        return None

class BreadthFirstSearch(SearchAlgorithm):
    def search(self, initial_state):
        """
        Performs Breadth-First Search to find a solution that maximizes score (specifically diamonds collected).
        Modified to use TreeNode for state representation and path tracking.
        """
        root_node = TreeNode(initial_state) # Create root TreeNode
        queue = deque([(root_node, [])])  # Queue of (TreeNode, path_to_node) - MODIFIED to use TreeNode
        visited = {self._board_to_tuple(initial_state.board)} # Keep track of visited board states
        best_score_solution = None
        max_score_reached = -1 # Initialize with a score lower than any possible score

        while queue:
            current_node, path = queue.popleft() # Get TreeNode from queue - MODIFIED
            current_state = current_node.state # Access GameState from TreeNode - MODIFIED

            if current_state.is_goal():
                accumulated_score = self._calculate_score_from_path(initial_state, path) # Calculate score for the path
                if accumulated_score > max_score_reached: # Found a better score
                    max_score_reached = accumulated_score
                    best_score_solution = path
                continue # Continue searching for potentially better solutions

            piece_name, piece = current_state.remaining_pieces[0]
            possible_actions = current_state.get_possible_actions(piece)

            # Evaluate each action and add to queue, prioritize by score
            scored_actions = [] # List to hold (score, action) tuples
            for row, col in possible_actions:
                successor_state, score_increase = current_state.generate_successor_with_score(piece, row, col) # Get state and score
                scored_actions.append((score_increase, (successor_state, row, col, (row, col)))) # Include move (row, col) in scored_actions

            # Sort actions by score in descending order (higher score first)
            scored_actions.sort(key=lambda item: item[0], reverse=True)

            for score_increase, (successor_state, row, col, move_coords) in scored_actions: # Unpack move_coords
                successor_board_tuple = self._board_to_tuple(successor_state.board)

                if successor_board_tuple not in visited:
                    visited.add(successor_board_tuple)
                    # Store the action (move_coords) when creating the child TreeNode:
                    child_node = TreeNode(successor_state, parent=current_node, action=(piece_name, move_coords[0], move_coords[1])) # Store action
                    new_path = path + [(piece_name, move_coords[0], move_coords[1])] # Append move coords to path
                    queue.append((child_node, new_path)) # Queue TreeNode and updated path - MODIFIED

        return best_score_solution # Return the path that led to the best score found


    def _board_to_tuple(self, board):
        """
        Helper function to convert a board (list of lists) to a tuple of tuples for hashability.
        """
        return tuple(tuple(row) for row in board)

    def _calculate_score_from_path(self, initial_state, path):
        """Calculates the total score for a given path of moves."""
        current_state = copy.deepcopy(initial_state)
        total_score = 0
        for piece_name, row, col in path:
            piece = current_state.piece_definitions[piece_name] # Assuming piece_definitions is accessible
            successor_state, score_increase = current_state.generate_successor_with_score(piece, row, col)
            total_score += score_increase
            current_state = successor_state  # Move to the next state
        return total_score


class DFSearch(SearchAlgorithm): # Depth First Search algorithm
    def search(self, initial_state):
        """
        Performs Depth-First Search to find a solution.
        This implementation now correctly reconstructs the path using actions stored in TreeNodes.
        Note: Basic DFS is NOT designed to find optimal solutions in terms of score for this game.
        It finds *a* solution quickly, but not necessarily the best one. For score optimization, BFS is more suitable.
        """
        root_node = TreeNode(initial_state)
        stack = [root_node] # Use list as stack for DFS - LIFO, replacing deque for simplicity in DFS
        visited = set([self._board_to_tuple(initial_state.board)]) # Visited states to prevent loops
        solution_path = None # Store solution path here

        while stack:
            current_node = stack.pop() # Pop from stack (LIFO for DFS)
            current_state = current_node.state

            if current_state.is_goal():
                solution_path = self._reconstruct_path(current_node) # Reconstruct path upon finding goal
                break # Stop searching once a solution is found (DFS finds first solution, not necessarily optimal)

            piece_name, piece = current_state.remaining_pieces[0]
            possible_actions = current_state.get_possible_actions(piece)

            for row, col in possible_actions:
                successor_state = current_state.generate_successor(piece, row, col)
                successor_board_tuple = self._board_to_tuple(successor_state.board)

                if successor_board_tuple not in visited:
                    visited.add(successor_board_tuple)
                    # Store the action (row, col) in the TreeNode
                    child_node = TreeNode(state=successor_state, parent=current_node, action=(piece_name, row, col))
                    current_node.add_child(child_node)
                    stack.append(child_node)

        return solution_path # Return the solution path found by DFS (or None if no solution)


    def _board_to_tuple(self, board):
        """Helper function to convert a board to a hashable tuple."""
        return tuple(tuple(row) for row in board)

    def _reconstruct_path(self, node):
        """Reconstructs the path from the goal node back to the root, using stored actions."""
        path = []
        current_node = node
        while current_node.parent is not None:
            if current_node.action: # Check if action is not None (for root node, action is None)
                path.insert(0, current_node.action) # Insert action at the beginning of path
            current_node = current_node.parent
        return path


# Random AI player (for comparison or as a baseline)
class AIPlayer:
    """
    A simple AI player that makes random valid moves.
    """
    def __init__(self, game_controller):
        self.game_controller = game_controller

    def play_step(self):
        """Plays one step using random valid move."""
        piece_name, piece = self.game_controller.piece_sequence.peek_next_piece()
        possible_moves = self._find_possible_moves(piece)
        if possible_moves:
            row, col = possible_moves[0] # Choose the first valid move (which is random due to move order)
            return self.game_controller.play(row, col)
        return None

    def _find_possible_moves(self, piece):
        """Finds all possible valid positions."""
        possible_positions = []
        piece_rows, piece_cols = len(piece), len(piece[0])
        for r in range(self.game_controller.game_board.rows):
            for c in range(self.game_controller.game_board.cols):
                if self.game_controller.can_place_piece(piece, r, c):
                    possible_positions.append((r, c))
        return possible_positions


# BFS AI Player - using the score-maximizing BFS algorithm
class BFS_AIPlayer:
    """AI player using Breadth-First Search for score maximization."""
    def __init__(self, game_controller, search_algorithm=None): # Inject search algorithm
        self.game_controller = game_controller
        self.search_algorithm = search_algorithm if search_algorithm is not None else BreadthFirstSearch() # Default to BFS

    def play_step(self):
        """Plays one step using the configured BFS algorithm to find the next move."""
        current_game_state = self.game_controller.get_game_state()
        solution_path = self.search_algorithm.search(current_game_state)

        if solution_path:
            next_move = solution_path[0]
            piece_name, row, col = next_move
            return self.game_controller.play(row, col)
        return None

# DF AI Player - using Depth-First Search algorithm
class DF_AIPlayer:
    """AI player using Depth-First Search."""
    def __init__(self, game_controller, search_algorithm=None): # Inject search algorithm
        self.game_controller = game_controller
        self.search_algorithm = search_algorithm if search_algorithm is not None else DFSearch() # Default to DFS

    def play_step(self):
        """Plays one step using the configured DFS algorithm to find the next move."""
        current_game_state = self.game_controller.get_game_state()
        solution_path = self.search_algorithm.search(current_game_state)

        if solution_path:
            next_move = solution_path[0]
            piece_name, row, col = next_move
            return self.game_controller.play(row, col)
        return None


# TreeNode class - put it here as it's used by DFS and BFS and might be used by other search algos
class TreeNode:
    def __init__(self, state, parent=None, action=None):
        """
        TreeNode for search algorithms. Stores the game state, parent node, and the action taken to reach this state.

        Args:
            state (GameState): The game state represented by this node.
            parent (TreeNode, optional): The parent node in the search tree. Defaults to None for the root node.
            action (tuple, optional): The action (piece_name, row, col) that led to this state from the parent. Defaults to None for the root node.
        """
        self.state = state
        self.parent = parent
        self.children = []
        self.action = action # Now storing the action!

    def add_child(self, child_node):
        """Adds a child node to this node."""
        self.children.append(child_node)
        child_node.parent = self