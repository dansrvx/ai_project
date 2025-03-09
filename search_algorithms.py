import heapq
import collections
import time
import copy

from logger_config import setup_logger

logger = setup_logger() 

class SearchAlgorithms:
    """
    Implements various search algorithms to find the best move in the play tree.
    """

    @staticmethod
    def depth_first_search(game_controller):
        """
        Performs Depth-First Search (DFS) to find a path to a victory (collect all diamonds) by
        dynamically generating the search tree.
        :param game_controller: The GameController representing the current game state.
        :return: The game plan (list of (row, col) tuples) leading to a victory,
                 or None if no path to victory is found.
        """
        start_time = time.time()
        expanded_nodes = 0
        visited_boards = set()
        initial_diamonds = game_controller.calculate_total_diamonds_in_game()
        stack = [(game_controller, [], initial_diamonds)]  # (game_controller, path, diamonds_left)
        # first_move = None
        while stack:
            current_controller, path, diamonds_left = stack.pop()
            expanded_nodes += 1

            # Convert board to tuple for loop detection
            board_tuple = tuple(tuple(row) for row in current_controller.game_board.board)
            if board_tuple in visited_boards:
                continue
            visited_boards.add(board_tuple)

            # Check if the branch results in a victory path.
            if diamonds_left == 0:
                # if(len(path)>0):
                #    first_move = path[0]
                # else:
                #    first_move = None

                end_time = time.time()
                execution_time = end_time - start_time
                logger.info(
                    f"DFS - Victory found! Running time: {execution_time:.4f}s, Expanded nodes: {expanded_nodes}, Path Length: {len(path)}"
                )
                return path
            # No possible moves to create
            if current_controller.is_defeat():
                continue

            # Generate moves
            piece_name, piece = current_controller.piece_sequence.peek_next_piece()
            for r in range(current_controller.game_board.rows - len(piece) + 1):
                for c in range(current_controller.game_board.cols - len(piece[0]) + 1):
                    if current_controller.can_place_piece(piece, r, c):
                        # Create a copy of the game_controller for each step
                        new_controller = copy.deepcopy(current_controller)
                        # Create a copy of the piece to allow it to place
                        piece_copy = copy.deepcopy(piece)

                        new_controller.play(r, c)
                        new_diamonds = new_controller.calculate_total_diamonds_in_game()
                        # Add the path for the other functions to work correctly
                        new_path = path + [(r, c)]
                        stack.append((new_controller, new_path, new_diamonds))

        end_time = time.time()
        execution_time = end_time - start_time
        logger.info(
            f"DFS - No victory found. Running time: {execution_time:.4f}s, Expanded nodes: {expanded_nodes}"
        )
        return None

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
        expanded_nodes = 0
        best_score = float('-inf')

        while queue:
            current_node, path = queue.popleft()
            expanded_nodes += 1
            board_tuple = tuple(tuple(row) for row in current_node.game_controller.game_board.board)
            game_score = current_node.game_controller.score
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
                    f"Breadth-First Search - Running time: {execution_time:.4f}s, Expanded nodes: {expanded_nodes}, Score: {game_score}, Length: {len(path + [current_node.position] if current_node.position else path)}"
                )
                return path + [current_node.position] if current_node.position else path # Return the path to victory

            for child in current_node.children:
                new_path = path + [current_node.position] if current_node.position else path
                queue.append((child, new_path))
                end_time = time.time()
        execution_time = end_time - start_time
        logger.info(
                    f"Breadth-First Search - Running time: {execution_time:.4f}s, Expanded nodes: {expanded_nodes}, Length: {len(path + [current_node.position] if current_node.position else path)}"
        )
        return None # No path to victory found

    @staticmethod
    def a_star_search_old(play_tree):
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
                       ((play_tree.root.heuristic + play_tree.root.cost), id(play_tree.root), play_tree.root, []))  # (cost + heuristic, unique id, node, path)
        best_path = []
        best_score = float('-inf')
        score = 0
        while priority_queue:
            _, _, node, path = heapq.heappop(priority_queue)
            expanded_nodes += 1
            game_score = node.game_controller.score

            if node.game_status == "victory":  # Only consider paths that lead to a win
                score = node.heuristic + node.cost  # A* formula: f(n) = h(n) - g(n)
                if score > best_score:
                    best_score = score
                    best_path = path + [node.position]  # Store the path to the best victory node
                #end_time = time.time()
                #execution_time = end_time - start_time
                #logger.info(f"A* Search - Running time: {execution_time:.4f}s, Expanded nodes: {expanded_nodes}, Score: {game_score}, Length: {len(best_path)}")                    
                #return best_path 
            

            for child in node.children:
                heapq.heappush(priority_queue,
                               ((child.heuristic + child.cost), id(child), child, path + [child.position]))

        end_time = time.time()
        execution_time = end_time - start_time
        logger.info(f"A* Search - Running time: {execution_time:.4f}s, Expanded nodes: {expanded_nodes}, Score: {game_score}, Length: {len(best_path)}")                    
                
        return best_path

    @staticmethod
    def a_star_search(play_tree):
        """
        Performs A* search to find the best sequence of moves in the play tree based on cost (empty spaces) and heuristic (score).
        Only considers paths that result in a victory.
        :param play_tree: The root of the play tree.
        :return: A list of (row, col) tuples representing the sequence of best moves leading to victory, or [] if no such path exists.
        """
        start_time = time.time()
        expanded_nodes = 0
        priority_queue = []
        root = play_tree.root
        heapq.heappush(priority_queue, (root.cost + root.heuristic, id(root), root, [], root.cost)) # Corrected f(n)
        best_path = []
        best_cost = float('inf')
        best_final_score = 0
        while priority_queue:
            _, _, node, path, cost_so_far = heapq.heappop(priority_queue)
            expanded_nodes += 1
            game_score = node.game_controller.score
            if node.game_status == "victory":
                if cost_so_far < best_cost:
                    best_cost = cost_so_far
                    best_path = path + [node.position]
                    best_final_score = game_score
            for child in node.children:
                new_cost = cost_so_far + child.cost
                estimated_total_cost = new_cost + child.heuristic # Corrected f(n)
                heapq.heappush(priority_queue, (estimated_total_cost, id(child), child, path + [child.position], new_cost))
        end_time = time.time()
        execution_time = end_time - start_time
        if best_path:
            logger.info(f"A* Search - Running time: {execution_time:.4f}s, Expanded nodes: {expanded_nodes}, Score: {best_final_score}, Best cost: {best_cost}, Length: {len(best_path)}")
        else:
            logger.info(f"A* Search - Running time: {execution_time:.4f}s, Expanded nodes: {expanded_nodes}, No solution found.")
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
        root = play_tree.root
        heapq.heappush(priority_queue, (-root.heuristic, id(root), root, []))  # (heuristic, unique id, node, path)
        best_path = []
        best_heuristic_score = float('-inf') #renamed variable for clarity.
        while priority_queue:
            _, _, node, path = heapq.heappop(priority_queue)
            expanded_nodes += 1
            game_score = node.game_controller.score
            if node.game_status == "victory":  # Only consider paths that lead to a win
                score = node.heuristic  # Greedy Search: f(n) = h(n)
                if score > best_heuristic_score:
                    best_heuristic_score = score
                    best_path = path + [node.position]  # Store the path to the best victory node
            for child in node.children:
                heapq.heappush(priority_queue, (-child.heuristic, id(child), child, path + [child.position]))
        end_time = time.time()
        execution_time = end_time - start_time
        if best_path:
            logger.info(f"Greedy Search - Running time: {execution_time:.4f}s, Expanded nodes: {expanded_nodes}, Heuristic Score: {best_heuristic_score}, Length: {len(best_path)}")
        else:
            logger.info(f"Greedy Search - Running time: {execution_time:.4f}s, Expanded nodes: {expanded_nodes}, No solution found.")
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
            game_score = node.game_controller.score

            if board_tuple in visited_boards:
                continue
            visited_boards.add(board_tuple)

            if node.game_status == "victory":
                solution_depth = depth
                end_time = time.time()
                execution_time = end_time - start_time
                logger.info(
                    f"Depth-Limited Search - Running time: {execution_time:.4f}s, Expanded nodes: {expanded_nodes}, Score: {game_score}, Solution depth: {solution_depth}, Length: {len(path + [node.position] if node.position else path)}, Depth limit: {depth_limit}"
                )
                return path + [node.position] if node.position else path # Return path to victory

            if depth < depth_limit:
                for child in node.children:
                    new_path = path + [node.position] if node.position else path
                    stack.append((child, new_path, depth + 1))

        end_time = time.time()
        execution_time = end_time - start_time
        logger.info(
                f"Depth-Limited Search - Running time: {execution_time:.4f}s, Expanded nodes: {expanded_nodes}, Score: {game_score}, Solution depth: {solution_depth}, Length: None, Depth limit: {depth_limit}"
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
                    f"Iterative Deepening Search - Running time: {execution_time:.4f}s"
                )
                return result # Return the path if found at the current depth limit
            end_time = time.time()
            execution_time = end_time - start_time
            logger.info(
                    f"Iterative Deepening Search - Running time: {execution_time:.4f}s"
            )
        return None # No path to victory found within max_depth