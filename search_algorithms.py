import heapq
'''
import heapq
from abc import ABC, abstractmethod

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
        #def heuristic(remaining_pieces):
        #    return len(remaining_pieces)
        def heuristic(state):
            """Função heurística que considera a pontuação potencial."""
            if not state.remaining_pieces:
                return 0
            piece_name, piece = state.remaining_pieces[0]
            actions = state.get_possible_actions(piece)
            if not actions:
                return len(state.remaining_pieces) * 100 #Penaliza estados que não tem ações.
            best_score = 0
            for row, col in actions:
                score = state.calculate_potential_score(piece, row, col)
                best_score = max(best_score, score)
            return -best_score + len(state.remaining_pieces)

        start_state = game_state
        priority_queue = [(heuristic(start_state), 0, 0, start_state, [])]  # (f(n), g(n), counter, state, path)
        visited = set()
        counter = 0 # Adicione um contador para desempatar

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
                #h = heuristic(successor.remaining_pieces)
                h = heuristic(successor)
                new_f = new_g + h
                new_path = path + [(piece_name, row, col)]
                counter += 1 #incrementa o counter
                heapq.heappush(priority_queue, (new_f, new_g, counter, successor, new_path)) #adiciona o counter

        return None
'''

import heapq
import collections
import time

from logger_config import setup_logger # Importe o modulo de configuração.

logger = setup_logger() # Configura o logger

class SearchAlgorithms:
    """
    Implements various search algorithms to find the best move in the play tree.
    """

    @staticmethod
    def depth_first_search(play_tree):
        """
        Performs Depth-First Search (DFS) to find a path to a victory in the play tree.
        This function explores paths as deep as possible before backtracking.

        :param play_tree: The root of the play tree.
        :return: The sequence of moves (list of (row, col) tuples) leading to a victory,
                 or None if no path to victory is found.
        """
        start_time = time.time()
        stack = [(play_tree.root, [])]  # Stack of (node, path_to_node)
        visited_boards = set()
        expanded_nodes = 0  # Contador de nós expandidos
        best_score = float('-inf')

        while stack:
            current_node, path = stack.pop()
            expanded_nodes += 1
            board_tuple = tuple(tuple(row) for row in current_node.game_controller.game_board.board)

            if board_tuple in visited_boards:
                continue
            visited_boards.add(board_tuple)

            if current_node.game_status == "victory":
                score = current_node.heuristic
                if score > best_score:
                    best_score = score

                end_time = time.time()
                execution_time = end_time - start_time
                logger.info(
                    f"Depth-First Search - Tempo: {execution_time:.4f}s, Nós expandidos: {expanded_nodes}, Pontuação:{best_score} Comprimento: {len(path + [current_node.position] if current_node.position else path)}"
                )

                return path + [current_node.position] if current_node.position else path  # Return the path to victory

            for child in reversed(current_node.children):  # Reverse to maintain left-to-right order
                new_path = path + [current_node.position] if current_node.position else path
                stack.append((child, new_path))

        end_time = time.time()
        execution_time = end_time - start_time
        logger.info(
            f"Depth-First Search - Tempo: {execution_time:.4f}s, Nós expandidos: {expanded_nodes}, Comprimento: None"
        )
        return None  # No path to victory found

    @staticmethod
    def breadth_first_search(play_tree):
        """
        Performs Breadth-First Search (BFS) to find the shortest path to a victory in the play tree.
        This function explores all possible moves level by level.

        :param play_tree: The root of the play tree.
        :return: The sequence of moves (list of (row, col) tuples) leading to a victory,
                 or None if no path to victory is found.
        """
        start_time = time.time()
        queue = collections.deque([(play_tree.root, [])])  # Queue of (node, path_to_node)
        visited_boards = set()
        expanded_nodes = 0  # Contador de nós expandidos
        best_score = float('-inf')

        while queue:
            current_node, path = queue.popleft()
            expanded_nodes += 1
            board_tuple = tuple(tuple(row) for row in current_node.game_controller.game_board.board)

            if board_tuple in visited_boards:
                continue
            visited_boards.add(board_tuple)

            if current_node.game_status == "victory":
                score = current_node.heuristic
                if score > best_score:
                    best_score = score
                end_time = time.time()
                execution_time = end_time - start_time
                logger.info(
                    f"Breadth-First Search - Tempo: {execution_time:.4f}s, Nós expandidos: {expanded_nodes}, Pontuação: {best_score}, Comprimento: {len(path + [current_node.position] if current_node.position else path)}"
                )
                return path + [current_node.position] if current_node.position else path # Return the path to victory

            for child in current_node.children:
                new_path = path + [current_node.position] if current_node.position else path
                queue.append((child, new_path))
                end_time = time.time()
        execution_time = end_time - start_time
        logger.info(
                    f"Breadth-First Search - Tempo: {execution_time:.4f}s, Nós expandidos: {expanded_nodes}, Comprimento: {len(path + [current_node.position] if current_node.position else path)}"
        )
        return None # No path to victory found

    @staticmethod
    def a_star_search(play_tree):
        """
        Performs A* search to find the best sequence of moves in the play tree based on cost and heuristic.
        Only considers paths that result in a victory.

        :param play_tree: The root of the play tree.
        :return: A list of (row, col) tuples representing the sequence of best moves leading to victory, or [] if no such path exists.
        """
        start_time = time.time()
        expanded_nodes = 0
        priority_queue = []
        heapq.heappush(priority_queue,
                       ((play_tree.root.heuristic - play_tree.root.cost)*-1, id(play_tree.root), play_tree.root, []))  # (cost + heuristic, unique id, node, path)
        best_path = []
        best_score = float('-inf')

        while priority_queue:
            _, _, node, path = heapq.heappop(priority_queue)
            expanded_nodes += 1

            if node.game_status == "victory":  # Only consider paths that lead to a win
                score = node.heuristic - node.cost  # A* formula: f(n) = h(n) - g(n)
                if score > best_score:
                    best_score = score
                    best_path = path + [node.position]  # Store the path to the best victory node

            for child in node.children:
                heapq.heappush(priority_queue,
                               ((child.heuristic - child.cost)*-1, id(child), child, path + [child.position]))

        end_time = time.time()
        execution_time = end_time - start_time
        logger.info(f"A* Search - Tempo: {execution_time:.4f}s, Nós expandidos: {expanded_nodes}, Pontuação: {best_score}, Comprimento: {len(best_path)}")
        
        return best_path

    @staticmethod
    def greedy_search(play_tree):
        """
        Performs Greedy Search to find the best sequence of moves in the play tree based on heuristic only.
        Only considers paths that result in a victory.

        :param play_tree: The root of the play tree.
        :return: A list of (row, col) tuples representing the sequence of best moves leading to victory, or [] if no such path exists.
        """
        expanded_nodes = 0
        start_time = time.time()
        priority_queue = []
        heapq.heappush(priority_queue,
                            (-play_tree.root.heuristic, id(play_tree.root), play_tree.root, []))  # (heuristic, unique id, node, path)
        best_path = []
        best_score = float('-inf')

        while priority_queue:
            _, _, node, path = heapq.heappop(priority_queue)
            expanded_nodes += 1

            if node.game_status == "victory":  # Only consider paths that lead to a win
                score = node.heuristic  # Greedy Search: f(n) = h(n)
                if score > best_score:
                    best_score = score
                    best_path = path + [node.position]  # Store the path to the best victory node

            for child in node.children:
                heapq.heappush(priority_queue,
                                    (-child.heuristic, id(child), child, path + [child.position]))

        end_time = time.time()
        execution_time = end_time - start_time
        logger.info(f"Greedy Search - Tempo: {execution_time:.4f}s, Nós expandidos: {expanded_nodes}, Pontuação: {best_score}, Comprimento: {len(best_path)}")
        return best_path    
    
    @staticmethod
    def depth_limited_search(play_tree, depth_limit):
        """
        Performs Depth-Limited Search (DLS) to find a path to victory within a given depth limit.

        :param play_tree: The root of the play tree.
        :param depth_limit: The maximum depth to search.
        :return: The sequence of moves (list of (row, col) tuples) leading to a victory within the depth limit,
                 or None if no path to victory is found within the limit.
        """
        start_time = time.time()
        stack = [(play_tree.root, [], 0)]  # Stack of (node, path_to_node, current_depth)
        visited_boards = set()
        expanded_nodes = 0
        solution_depth = -1

        while stack:
            node, path, depth = stack.pop()
            board_tuple = tuple(tuple(row) for row in node.game_controller.game_board.board)
            expanded_nodes += 1

            if board_tuple in visited_boards:
                continue
            visited_boards.add(board_tuple)

            if node.game_status == "victory":
                solution_depth = depth
                end_time = time.time()
                execution_time = end_time - start_time
                logger.info(
                    f"Depth-Limited Search - Tempo: {execution_time:.4f}s, Nós expandidos: {expanded_nodes}, Profundidade da solução: {solution_depth}, Comprimento: {len(path + [node.position] if node.position else path)}, Limite de profundidade: {depth_limit}"
                )
                return path + [node.position] if node.position else path # Return path to victory

            if depth < depth_limit:
                for child in node.children:
                    new_path = path + [node.position] if node.position else path
                    stack.append((child, new_path, depth + 1))

        end_time = time.time()
        execution_time = end_time - start_time
        logger.info(
                f"Depth-Limited Search - Tempo: {execution_time:.4f}s, Nós expandidos: {expanded_nodes}, Profundidade da solução: {solution_depth}, Comprimento: None, Limite de profundidade: {depth_limit}"
        )
        return None  # No path to victory within depth limit

    
    @staticmethod
    def iterative_deepening_search(play_tree, max_depth):
        """
        Performs Iterative Deepening Search (IDS) by repeatedly calling Depth-Limited Search
        with increasing depth limits.

        :param play_tree: The root of the play tree.
        :param max_depth: The maximum depth to explore.
        :return: The sequence of moves (list of (row, col) tuples) leading to a victory,
                 or None if no path to victory is found within the max depth.
        """
        start_time = time.time()
        for depth_limit in range(max_depth + 1): # Iterate through depth limits from 0 to max_depth
            result = SearchAlgorithms.depth_limited_search(play_tree, depth_limit)
            if result:
                end_time = time.time()
                execution_time = end_time - start_time
                logger.info(
                    f"Iterative Deepening Search - Tempo: {execution_time:.4f}s"
                )
                return result # Return the path if found at the current depth limit
            end_time = time.time()
            execution_time = end_time - start_time
            logger.info(
                    f"Iterative Deepening Search - Tempo: {execution_time:.4f}s"
            )
        return None # No path to victory found within max_depth