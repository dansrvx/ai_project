import heapq
import collections
import tracemalloc
import time
import copy
import psutil

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
            - 'cpu' : Return a float representing the current system-wide CPU utilization as a percentage.
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
        final_score = 0

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
                final_score = current_controller.score

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
        cpu = psutil.cpu_percent(execution_time)
        # Find the peak memory usage on the game
        _, peak = tracemalloc.get_traced_memory()
        memory_usage = peak / 1024

        tracemalloc.stop()  # Stop memory tracing
        if (success):
            logger.info(
                f"DFS - Victory found! Running time: {execution_time:.4f}s, Expanded nodes: {expanded_nodes}, Path Length: {len(plan)}, Memory Used: {memory_usage:.2f} KB, CPU Used: {cpu} "
            )
        else:
            logger.info(
                f"DFS - No victory found. Running time: {execution_time:.4f}s, Expanded nodes: {expanded_nodes}, Memory Used: {memory_usage:.2f} KB, CPU Used: {cpu} "
            )
        statistics = {
            'plan': plan,
            'nodes_explored': expanded_nodes,
            'execution_time': execution_time,
            'memory_usage': memory_usage,
            'path_length': path_length,
            'success': success,
            'cpu': cpu,
            'final_score': final_score
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
        final_score = 0

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
                final_score = current_controller.score

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
        cpu = psutil.cpu_percent(execution_time)
        # Find the peak memory usage on the game
        _, peak = tracemalloc.get_traced_memory()
        memory_usage = peak / 1024

        tracemalloc.stop()  # Stop memory tracing
        if (success):
            logger.info(
                f"BFS - Victory found! Running time: {execution_time:.4f}s, Expanded nodes: {expanded_nodes}, Path Length: {len(plan)}, Memory Used: {memory_usage:.2f} KB, CPU Used: {cpu} "
            )
        else:
            logger.info(
                f"BFS - No victory found. Running time: {execution_time:.4f}s, Expanded nodes: {expanded_nodes}, Memory Used: {memory_usage:.2f} KB, CPU Used: {cpu} "
            )
        statistics = {
            'plan': plan,
            'nodes_explored': expanded_nodes,
            'execution_time': execution_time,
            'memory_usage': memory_usage,
            'path_length': path_length,
            'success': success,
            'cpu': cpu,
            'final_score': final_score
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
        final_score = 0

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
                final_score = current_controller.score

                end_time = time.time()
                execution_time = end_time - start_time
                cpu = psutil.cpu_percent(execution_time)

                # Find the peak memory usage on the game
                _, peak = tracemalloc.get_traced_memory()
                memory_usage = peak / 1024
                
                logger.info(
                    f"A* - Victory found! Running time: {execution_time:.4f}s, Expanded nodes: {expanded_nodes}, Path Length: {len(path)}, Memory Used: {memory_usage:.2f} KB, CPU Used: {cpu} "
                )

                statistics = {
                    'plan': plan,
                    'nodes_explored': expanded_nodes,
                    'execution_time': execution_time,
                    'memory_usage': memory_usage,
                    'path_length': path_length,
                    'success': success,
                    'cpu': cpu,            
                    'final_score': final_score
                }
                return statistics
                #break  # Stop the loop after the plan is found.

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
        cpu = psutil.cpu_percent(execution_time)
        # Find the peak memory usage on the game
        _, peak = tracemalloc.get_traced_memory()
        memory_usage = peak / 1024

        tracemalloc.stop()  # Stop memory tracing
        if (success):
            logger.info(
                f"A* - Victory found! Running time: {execution_time:.4f}s, Expanded nodes: {expanded_nodes}, Path Length: {len(plan)}, Memory Used: {memory_usage:.2f} KB, CPU Used: {cpu} "
            )
        else:
            logger.info(
                f"A* - No victory found. Running time: {execution_time:.4f}s, Expanded nodes: {expanded_nodes}, Memory Used: {memory_usage:.2f} KB, CPU Used: {cpu} "
            )

        statistics = {
            'plan': plan,
            'nodes_explored': expanded_nodes,
            'execution_time': execution_time,
            'memory_usage': memory_usage,
            'path_length': path_length,
            'success': success,
            'cpu': cpu,            
            'final_score': final_score
        }
        return statistics

    @staticmethod
    def greedy_search(game_controller):
        """
        Performs Greedy Search to find the best sequence of moves based on diamonds collected as a heuristic.

        :param game_controller: The GameController representing the current game state.
        :return: A dictionary containing the following statistics:
            - 'plan': The game plan (list of (row, col) tuples) leading to a victory, or None if no path to victory is found.
            - 'nodes_explored': The number of nodes explored during the search.
            - 'execution_time': The time required for the execution of the search.
            - 'memory_usage': The peak memory usage during the search.
            - 'path_length': The number of moves required to win (length of the path), or None if no path is found.
            - 'success': A boolean indicating whether a game plan was found (True) or not (False).
        """

        tracemalloc.start()
        start_time = time.time()
        expanded_nodes = 0
        priority_queue = []
        visited_boards = set()  # Store visited board states to avoid cycles

        initial_diamonds = game_controller.calculate_total_diamonds_in_game()
        heapq.heappush(priority_queue, (initial_diamonds, id(game_controller), game_controller, []))  # (heuristic, unique_id, game_controller, path)

        plan = None
        path_length = None
        success = False
        memory_usage = 0
        final_score = None

        while priority_queue:
            heuristic, _, current_controller, path = heapq.heappop(priority_queue)
            expanded_nodes += 1

            # Convert board to tuple for loop detection
            board_tuple = tuple(tuple(row) for row in current_controller.game_board.board)
            if board_tuple in visited_boards:
                continue
            visited_boards.add(board_tuple)

            # Check for victory
            current_diamonds = current_controller.calculate_total_diamonds_in_game()
            if current_diamonds == 0:
                plan = path
                path_length = len(path)
                success = True
                final_score = current_controller.score
                break

            # Check if no more pieces can be placed
            if current_controller.is_defeat():
                continue

            # Generate potential actions
            piece_name, piece = current_controller.piece_sequence.peek_next_piece()

            for r in range(current_controller.game_board.rows - len(piece) + 1):
                for c in range(current_controller.game_board.cols - len(piece[0]) + 1):
                    if current_controller.can_place_piece(piece, r, c):
                        # Create a copy of the game_controller for each step
                        new_controller = copy.deepcopy(current_controller)

                        new_controller.play(r, c)

                        # Calculate new heuristic value (number of diamonds after the move)
                        new_diamonds = new_controller.calculate_total_diamonds_in_game()

                        new_path = path + [(r, c)]  # Add the selected node to path

                        heapq.heappush(priority_queue, (new_diamonds, id(new_controller), new_controller, new_path))

        end_time = time.time()
        execution_time = end_time - start_time
        cpu = psutil.cpu_percent(execution_time)

        # Find the peak memory usage on the game
        _, peak = tracemalloc.get_traced_memory()
        memory_usage = peak / 1024

        tracemalloc.stop()

        if success:
            logger.info(
                f"Greedy - Victory found! Running time: {execution_time:.4f}s, Expanded nodes: {expanded_nodes}, Path Length: {len(plan)}, Memory Used: {memory_usage:.2f} KB, CPU Used: {cpu} "
            )
        else:
            logger.info(
                f"Greedy - No victory found. Running time: {execution_time:.4f}s, Expanded nodes: {expanded_nodes}, Memory Used: {memory_usage:.2f} KB, CPU Used: {cpu} "
            )

        statistics = {
            'plan': plan,
            'nodes_explored': expanded_nodes,
            'execution_time': execution_time,
            'memory_usage': memory_usage,
            'path_length': path_length,
            'success': success,
            'cpu': cpu,            
            'final_score': final_score
        }
        return statistics
    
        
    @staticmethod
    def depth_limited_search(game_controller, depth_limit):
        """
        Performs Depth-Limited Search (DLS) to find a path to victory (collect all diamonds) within a given depth limit
        by dynamically generating the search tree.

        :param game_controller: The GameController representing the current game state.
        :param depth_limit: The maximum depth to search.
        :return: A dictionary containing search statistics and the game plan if found within the depth limit.
        """
        tracemalloc.start()  # Start memory tracing
        start_time = time.time()
        expanded_nodes = 0
        visited_boards = set()
        initial_diamonds = game_controller.calculate_total_diamonds_in_game()
        stack = [(game_controller, [], initial_diamonds, 0)]  # (game_controller, path, diamonds_left, depth)
        plan = None
        path_length = None
        success = False
        memory_usage = 0
        final_score = 0
        solution_depth = -1 # To track if a solution was found within the depth limit

        while stack:
            current_controller, path, diamonds_left, depth = stack.pop()
            expanded_nodes += 1

            # Convert board to tuple for loop detection
            board_tuple = tuple(tuple(row) for row in current_controller.game_board.board)
            if board_tuple in visited_boards:
                continue
            visited_boards.add(board_tuple)

            if diamonds_left == 0:
                plan = path
                path_length = len(path)
                success = True
                final_score = current_controller.score
                solution_depth = depth # Record the depth at which the solution is found
                break # Solution found within depth limit, exit DLS

            if depth >= depth_limit: # Depth limit reached, backtrack
                continue # Do not explore deeper

            if current_controller.is_defeat():
                continue

            piece_name, piece = current_controller.piece_sequence.peek_next_piece()
            for r in range(current_controller.game_board.rows - len(piece) + 1):
                for c in range(current_controller.game_board.cols - len(piece[0]) + 1):
                    if current_controller.can_place_piece(piece, r, c):
                        new_controller = copy.deepcopy(current_controller)
                        piece_copy = copy.deepcopy(piece) # Create a copy of the piece
                        new_controller.play(r, c)
                        new_diamonds = new_controller.calculate_total_diamonds_in_game()
                        new_path = path + [(r, c)]
                        stack.append((new_controller, new_path, new_diamonds, depth + 1))

        end_time = time.time()
        execution_time = end_time - start_time
        cpu = psutil.cpu_percent(execution_time)
        _, peak = tracemalloc.get_traced_memory()
        memory_usage = peak / 1024
        tracemalloc.stop()

        if success:
            logger.info(
                f"DLS (Limit {depth_limit}) - Victory within limit! Time: {execution_time:.4f}s, Nodes: {expanded_nodes}, Depth: {solution_depth}, Memory: {memory_usage:.2f} KB, CPU Used: {cpu} "
            )
        else:
            logger.info(
                f"DLS (Limit {depth_limit}) - No victory within limit. Time: {execution_time:.4f}s, Nodes: {expanded_nodes}, Memory: {memory_usage:.2f} KB, CPU Used: {cpu} "
            )

        statistics = {
            'plan': plan,
            'nodes_explored': expanded_nodes,
            'execution_time': execution_time,
            'memory_usage': memory_usage,
            'path_length': path_length,
            'success': success,
            'final_score': final_score,
            'solution_depth': solution_depth,
            'cpu': cpu,       
            'depth_limit': depth_limit
        }
        return statistics

    
    @staticmethod
    def iterative_deepening_search(game_controller, max_depth):
        """
        Performs Iterative Deepening Search (IDS) by repeatedly calling Depth-Limited Search
        with increasing depth limits.

        :param game_controller: The GameController representing the current game state.
        :param max_depth: The maximum depth to explore.
        :return: A dictionary containing search statistics and the game plan if found within max_depth.
        """
        start_time = time.time()
        total_expanded_nodes = 0
        total_memory_usage = 0
        cumulative_execution_time = 0
        final_plan = None
        final_path_length = None
        final_success = False
        final_score = 0
        final_depth = -1
        depth_limit_reached = -1 # Track the depth limit at which solution was found

        for depth_limit in range(1, max_depth + 1): # Iterate through depth limits from 1 to max_depth
            dls_statistics = SearchAlgorithms.depth_limited_search(game_controller, depth_limit)
            cumulative_execution_time += dls_statistics['execution_time']
            total_expanded_nodes += dls_statistics['nodes_explored']
            total_memory_usage = max(total_memory_usage, dls_statistics['memory_usage']) # Keep track of peak memory

            if dls_statistics['success']: # If DLS found a solution at this depth limit
                final_plan = dls_statistics['plan']
                final_path_length = dls_statistics['path_length']
                final_success = True
                final_score = dls_statistics['final_score']
                final_depth = dls_statistics['solution_depth']
                depth_limit_reached = depth_limit # Record the depth limit where solution was found
                break # Stop IDS as soon as a solution is found


        end_time = time.time()
        execution_time = end_time - start_time # Total time for IDS (though cumulative_execution_time from DLS calls is more accurate for search time)
        cpu = psutil.cpu_percent(execution_time)

        if final_success:
            logger.info(
                f"IDS - Victory found! (Depth Limit: {depth_limit_reached}). Total Time: {cumulative_execution_time:.4f}s, Total Nodes: {total_expanded_nodes}, Path Length: {final_path_length}, Memory Used: {total_memory_usage:.2f} KB, CPU Used: {cpu} "
            )
        else:
            logger.info(
                f"IDS - No victory within max depth {max_depth}. Total Time: {cumulative_execution_time:.4f}s, Total Nodes: {total_expanded_nodes}, Memory Used: {total_memory_usage:.2f} KB, CPU Used: {cpu} "
            )

        statistics = {
            'plan': final_plan,
            'nodes_explored': total_expanded_nodes,
            'execution_time': cumulative_execution_time, # Use cumulative time from DLS calls for search time
            'memory_usage': total_memory_usage,
            'path_length': final_path_length,
            'success': final_success,
            'final_score': final_score,
            'depth_limit_reached': depth_limit_reached,
            'cpu': cpu,       
            'max_depth': max_depth
        }
        return statistics
    
    
    @staticmethod
    def uniform_cost_search(game_controller):
        """
        Performs Uniform Cost Search (UCS) to find a path to victory (collect all diamonds) by
        dynamically generating the search tree, prioritizing paths with the lowest move cost.

        :param game_controller: The GameController representing the current game state.
        :return: A dictionary containing search statistics and the game plan if found.
        """
        tracemalloc.start()  # Start memory tracing
        start_time = time.time()
        expanded_nodes = 0
        visited_boards = set()
        initial_diamonds = game_controller.calculate_total_diamonds_in_game()
        priority_queue = [(0, id(game_controller), game_controller, [], 0)]  # (cost, unique_id, game_controller, path, cost)

        plan = None
        path_length = None
        success = False
        memory_usage = 0
        final_score = 0

        while priority_queue:
            cost, _, current_controller, path, current_cost = heapq.heappop(priority_queue) # Cost is the priority
            expanded_nodes += 1

            # Convert board to tuple for loop detection
            board_tuple = tuple(tuple(row) for row in current_controller.game_board.board)
            if board_tuple in visited_boards:
                continue
            visited_boards.add(board_tuple)

            # Check for victory
            if current_controller.calculate_total_diamonds_in_game() == 0:
                plan = path
                path_length = len(path)
                success = True
                final_score = current_controller.score

                end_time = time.time()
                execution_time = end_time - start_time
                cpu = psutil.cpu_percent(execution_time)
                _, peak = tracemalloc.get_traced_memory()
                memory_usage = peak / 1024

                logger.info(
                    f"UCS - Victory found! Running time: {execution_time:.4f}s, Expanded nodes: {expanded_nodes}, Path Length: {len(plan)}, Memory Used: {memory_usage:.2f} KB, CPU Used: {cpu} "
                )
                break # Solution found, exit UCS

            # Check for defeat (no moves possible)
            if current_controller.is_defeat():
                continue

            # Generate moves
            piece_name, piece = current_controller.piece_sequence.peek_next_piece()
            for r in range(current_controller.game_board.rows - len(piece) + 1):
                for c in range(current_controller.game_board.cols - len(piece[0]) + 1):
                    if current_controller.can_place_piece(piece, r, c):
                        new_controller = copy.deepcopy(current_controller)
                        piece_copy = copy.deepcopy(piece) # Create a copy of the piece
                        new_controller.play(r, c)
                        new_diamonds = new_controller.calculate_total_diamonds_in_game()
                        new_path = path + [(r, c)]
                        new_cost = current_cost + 1 # Increment cost for each move
                        heapq.heappush(priority_queue, (new_cost, id(new_controller), new_controller, new_path, new_cost)) # Push with updated cost


        end_time = time.time()
        execution_time = end_time - start_time
        cpu = psutil.cpu_percent(execution_time)
        _, peak = tracemalloc.get_traced_memory()
        memory_usage = peak / 1024
        tracemalloc.stop()


        if success:
            logger.info(
                f"UCS - Victory found! Running time: {execution_time:.4f}s, Expanded nodes: {expanded_nodes}, Path Length: {len(plan)}, Memory Used: {memory_usage:.2f} KB, CPU Used: {cpu} "
            )
        else:
            logger.info(
                f"UCS - No victory found. Running time: {execution_time:.4f}s, Expanded nodes: {expanded_nodes}, Memory Used: {memory_usage:.2f} KB, CPU Used: {cpu} "
            )

        statistics = {
            'plan': plan,
            'nodes_explored': expanded_nodes,
            'execution_time': execution_time,
            'memory_usage': memory_usage,
            'path_length': path_length,
            'success': success,
            'cpu': cpu,       
            'final_score': final_score
        }
        return statistics