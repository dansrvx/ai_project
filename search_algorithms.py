import heapq
import collections
import tracemalloc
import time
import copy

from logger_config import setup_logger

logger = setup_logger() 

class SearchAlgorithms:
    """
    Implements various search algorithms to find the best move in the play tree.
    """

    import tracemalloc

    import tracemalloc

    @staticmethod
    def depth_first_search(game_controller):
        """
        Performs Depth-First Search (DFS) to find a path to a victory (collect all diamonds) by
        dynamically generating the search tree.
        :param game_controller: The GameController representing the current game state.
        :return: A dictionary containing the following statistics:
            - 'plan': The game plan (list of (row, col) tuples) leading to a victory, or None if no path to victory is found.
            - 'nodes_explored': The number of nodes explored during the search.
            - 'execution_time': The time required for the execution of the search.
            - 'memory_usage': The peak memory usage during the search.
            - 'path_length': The number of moves required to win (length of the path), or None if no path is found.
            - 'success': A boolean indicating whether a game plan was found (True) or not (False).
        """
        tracemalloc.start()  # Start memory tracing
        start_time = time.time()
        expanded_nodes = 0
        visited_boards = set()
        initial_diamonds = game_controller.calculate_total_diamonds_in_game()
        stack = [(game_controller, [], initial_diamonds)]  # (game_controller, path, diamonds_left)

        plan = None
        path_length = None
        success = False
        memory_usage = 0
        victory = False

        while stack and not victory:
            current_controller, path, diamonds_left = stack.pop()
            expanded_nodes += 1

            # Convert board to tuple for loop detection
            board_tuple = tuple(tuple(row) for row in current_controller.game_board.board)
            if board_tuple in visited_boards:
                continue
            visited_boards.add(board_tuple)

            # Check if the branch results in a victory path.
            if diamonds_left == 0:
                plan = path
                path_length = len(path)
                success = True
                victory = True

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
        # Find the peak memory usage on the game
        _, peak = tracemalloc.get_traced_memory()
        memory_usage = peak / 1024

        tracemalloc.stop()  # Stop memory tracing
        if (success):
            logger.info(
                f"DFS - Victory found! Running time: {execution_time:.4f}s, Expanded nodes: {expanded_nodes}, Path Length: {len(plan)}, Memory Used: {memory_usage:.2f} KB"
            )
        else:
            logger.info(
                f"DFS - No victory found. Running time: {execution_time:.4f}s, Expanded nodes: {expanded_nodes}, Memory Used: {memory_usage:.2f} KB"
            )
        statistics = {
            'plan': plan,
            'nodes_explored': expanded_nodes,
            'execution_time': execution_time,
            'memory_usage': memory_usage,
            'path_length': path_length,
            'success': success
        }
        return statistics

    @staticmethod
    def breadth_first_search(game_controller):
        """
        Performs Breadth-First Search (BFS) to find a path to a victory (collect all diamonds) by
        dynamically generating the search tree.
        :param game_controller: The GameController representing the current game state.
        :return: A dictionary containing the following statistics:
            - 'plan': The game plan (list of (row, col) tuples) leading to a victory, or None if no path to victory is found.
            - 'nodes_explored': The number of nodes explored during the search.
            - 'execution_time': The time required for the execution of the search.
            - 'memory_usage': The peak memory usage during the search.
            - 'path_length': The number of moves required to win (length of the path), or None if no path is found.
            - 'success': A boolean indicating whether a game plan was found (True) or not (False).
        """
        tracemalloc.start()  # Start memory tracing
        start_time = time.time()
        expanded_nodes = 0
        visited_boards = set()
        initial_diamonds = game_controller.calculate_total_diamonds_in_game()
        queue = collections.deque([(game_controller, [], initial_diamonds)])  # (game_controller, path, diamonds_left)

        plan = None
        path_length = None
        success = False
        memory_usage = 0
        victory = False

        while queue and not victory:
            current_controller, path, diamonds_left = queue.popleft()
            expanded_nodes += 1

            # Convert board to tuple for loop detection
            board_tuple = tuple(tuple(row) for row in current_controller.game_board.board)
            if board_tuple in visited_boards:
                continue
            visited_boards.add(board_tuple)

            # Check if the branch results in a victory path.
            if diamonds_left == 0:
                plan = path
                path_length = len(path)
                success = True
                victory = True

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
                        queue.append((new_controller, new_path, new_diamonds))

        end_time = time.time()
        execution_time = end_time - start_time
        # Find the peak memory usage on the game
        _, peak = tracemalloc.get_traced_memory()
        memory_usage = peak / 1024

        tracemalloc.stop()  # Stop memory tracing
        if (success):
            logger.info(
                f"BFS - Victory found! Running time: {execution_time:.4f}s, Expanded nodes: {expanded_nodes}, Path Length: {len(plan)}, Memory Used: {memory_usage:.2f} KB"
            )
        else:
            logger.info(
                f"BFS - No victory found. Running time: {execution_time:.4f}s, Expanded nodes: {expanded_nodes}, Memory Used: {memory_usage:.2f} KB"
            )
        statistics = {
            'plan': plan,
            'nodes_explored': expanded_nodes,
            'execution_time': execution_time,
            'memory_usage': memory_usage,
            'path_length': path_length,
            'success': success
        }
        return statistics

    import heapq
    import tracemalloc

    @staticmethod
    def a_star_search(game_controller):
        """
        Performs A* search to find a path to a victory (collect all diamonds) by
        dynamically generating the search tree.
        :param game_controller: The GameController representing the current game state.
        :return: A dictionary containing the following statistics:
            - 'plan': The game plan (list of (row, col) tuples) leading to a victory, or None if no path to victory is found.
            - 'nodes_explored': The number of nodes explored during the search.
            - 'execution_time': The time required for the execution of the search.
            - 'memory_usage': The peak memory usage during the search.
            - 'path_length': The number of moves required to win (length of the path), or None if no path is found.
            - 'success': A boolean indicating whether a game plan was found (True) or not (False).
        """
        tracemalloc.start()  # Start memory tracing
        start_time = time.time()
        expanded_nodes = 0
        visited_boards = set()
        initial_diamonds = game_controller.calculate_total_diamonds_in_game()
        # Use a tiebreaker to push to the heap
        priority_queue = [(0, id(game_controller), game_controller, [], 0)]  # (f_score, unique_id, game_controller, path, cost)

        plan = None
        path_length = None
        success = False
        memory_usage = 0

        while priority_queue:
            f_score, _, current_controller, path, cost = heapq.heappop(priority_queue)
            expanded_nodes += 1

            # Convert board to tuple for loop detection
            board_tuple = tuple(tuple(row) for row in current_controller.game_board.board)
            if board_tuple in visited_boards:
                continue
            visited_boards.add(board_tuple)

            # Check if the branch results in a victory path.
            if current_controller.calculate_total_diamonds_in_game() == 0:
                plan = path
                path_length = len(path)
                success = True

                end_time = time.time()
                execution_time = end_time - start_time

                # Find the peak memory usage on the game
                _, peak = tracemalloc.get_traced_memory()
                memory_usage = peak / 1024

                logger.info(
                    f"A* - Victory found! Running time: {execution_time:.4f}s, Expanded nodes: {expanded_nodes}, Path Length: {len(path)}, Memory Used: {memory_usage:.2f} KB"
                )
                break  # Stop the loop after the plan is found.

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
                        new_cost = cost + 1  # Increment the cost by 1 on each move

                        # Calculate heuristic: diamonds_collected - cost_so_far
                        heuristic = initial_diamonds - new_diamonds + new_cost

                        f_score = heuristic  # A* evaluation function: f(n) = g(n) + h(n)
                        heapq.heappush(priority_queue, (f_score, id(new_controller), new_controller, new_path, new_cost))

        end_time = time.time()
        execution_time = end_time - start_time
        # Find the peak memory usage on the game
        _, peak = tracemalloc.get_traced_memory()
        memory_usage = peak / 1024

        tracemalloc.stop()  # Stop memory tracing
        if (success):
            logger.info(
                f"A* - Victory found! Running time: {execution_time:.4f}s, Expanded nodes: {expanded_nodes}, Path Length: {len(plan)}, Memory Used: {memory_usage:.2f} KB"
            )
        else:
            logger.info(
                f"A* - No victory found. Running time: {execution_time:.4f}s, Expanded nodes: {expanded_nodes}, Memory Used: {memory_usage:.2f} KB"
            )

        statistics = {
            'plan': plan,
            'nodes_explored': expanded_nodes,
            'execution_time': execution_time,
            'memory_usage': memory_usage,
            'path_length': path_length,
            'success': success
        }
        return statistics

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