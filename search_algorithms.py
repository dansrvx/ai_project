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


class SearchAlgorithms:
    """
    Implements various search algorithms to find the best move in the play tree.
    """

    @staticmethod
    def a_star_search(play_tree):
        """
        Performs A* search to find the best sequence of moves in the play tree based on cost and heuristic.
        Only considers paths from the root to leaf nodes, ensuring no cycles or returns.

        :param play_tree: The root of the play tree.
        :return: A list of (row, col) tuples representing the sequence of best moves found using A*.
        """
        priority_queue = []
        heapq.heappush(priority_queue,
                       (0, id(play_tree.root), play_tree.root, []))  # (cost + heuristic, unique id, node, path)
        best_path = []
        best_score = float('-inf')

        while priority_queue:
            _, _, node, path = heapq.heappop(priority_queue)

            if not node.children:  # Only consider paths leading to leaf nodes
                score = node.heuristic - node.cost  # A* formula: f(n) = h(n) - g(n)
                if score > best_score:
                    best_score = score
                    best_path = path + [node.position]  # Store the path to the best leaf node

            for child in node.children:
                heapq.heappush(priority_queue,
                               (child.heuristic - child.cost, id(child), child, path + [child.position]))

        return best_path


