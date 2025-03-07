import heapq
import collections
import time

from logger_config import setup_logger

logger = setup_logger() 

class SearchAlgorithms:
    """
    Implements various search algorithms to find the best move in the play tree.
    """

    @staticmethod
    def depth_first_search(play_tree):
        """
        Performs Depth-First Search (DFS) to find a path to a victory in the play tree.
        This function explores paths as deep as possible before backtracking.
        """
        start_time = time.time()
        stack = [(play_tree.root, [], 0)]  # Stack of (node, path_to_node, cost)
        visited_boards = set()
        expanded_nodes = 0  
        best_score = float('-inf')
        best_cost = float('inf')
        best_path = None

        while stack:
            current_node, path, cost = stack.pop()
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
                    best_cost = cost
                    best_path = path + [current_node.position] if current_node.position else path

            for child in reversed(current_node.children):  # Reverse to maintain left-to-right order
                new_path = path + [current_node.position] if current_node.position else path
                new_cost = cost + child.cost
                stack.append((child, new_path, new_cost))

        end_time = time.time()
        execution_time = end_time - start_time
        if best_path:
            logger.info(
                f"Depth-First Search - Running time: {execution_time:.4f}s, Expanded nodes: {expanded_nodes}, Score:{best_score}, Cost: {best_cost}, Length: {best_path}"
            )
            return best_path
        else:
            logger.info(
                f"Depth-First Search - Running time: {execution_time:.4f}s, Expanded nodes: {expanded_nodes}, Score: None, Cost: None, Length: None"
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
        queue = collections.deque([(play_tree.root, [], 0)])  # Queue of (node, path_to_node, cost)
        visited_boards = set()
        expanded_nodes = 0
        best_score = float('-inf')
        best_cost = float('inf')
        best_path = None

        while queue:
            current_node, path, cost = queue.popleft()
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
                    best_cost = cost
                    best_path = path + [current_node.position] if current_node.position else path

            for child in current_node.children:
                new_path = path + [current_node.position] if current_node.position else path
                new_cost = cost + child.cost
                queue.append((child, new_path, new_cost))

        end_time = time.time()
        execution_time = end_time - start_time
        if best_path:
            logger.info(
                f"Breadth-First Search - Running time: {execution_time:.4f}s, Expanded nodes: {expanded_nodes}, Score: {best_score}, Cost: {best_cost}, Length: {best_path}"
            )
            return best_path
        else:
            logger.info(
                f"Breadth-First Search - Running time: {execution_time:.4f}s, Expanded nodes: {expanded_nodes}, Score: None, Cost: None, Length: None"
            )
            return None # No path to victory found

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
        heapq.heappush(priority_queue, (-root.heuristic + root.cost, id(root), root, [], root.cost, set())) # Changed f(n) and initial push
        best_path = []
        best_cost = float('inf')
        best_final_score = float('-inf') # Initialize to negative infinity for maximization
        visited_paths = {} # Track visited paths and states
        while priority_queue:
            f_n, _, node, path, cost_so_far, visited_states = heapq.heappop(priority_queue) # Get f(n)
            expanded_nodes += 1
            game_score = node.game_controller.score
            board_tuple = tuple(tuple(row) for row in node.game_controller.game_board.board)
            logger.debug(f"A* Node: Cost={cost_so_far}, Heuristic={node.heuristic}, Total={-f_n}, Game Score={game_score}, Board={node.game_controller.game_board.board}") # Log adicional
            if node.game_status == "victory":
                if node.heuristic > best_final_score: # Use heuristic for comparison
                    best_cost = cost_so_far
                    best_path = path #+ [node.position]
                    best_final_score = node.heuristic # Store heuristic (score)
            for child in node.children:
                new_cost = cost_so_far + child.cost
                estimated_total_cost = child.heuristic - new_cost # Changed f(n) calculation
                child_board_tuple = tuple(tuple(row) for row in child.game_controller.game_board.board)
                child_path_tuple = tuple(path + [child.position]) # Create a tuple of the path

                # Check if the path and state have been visited
                if child_path_tuple in visited_paths and visited_paths[child_path_tuple] == child_board_tuple:
                    continue
                
                new_visited_states = visited_states.copy()
                new_visited_states.add(child_board_tuple)
                
                heapq.heappush(priority_queue, (-estimated_total_cost, id(child), child, path + [child.position], new_cost, new_visited_states)) # Changed push
                visited_paths[child_path_tuple] = child_board_tuple # Add path and state to visited paths
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
                    best_path = path #+ [node.position]  # Store the path to the best victory node
            for child in node.children:
                heapq.heappush(priority_queue, (-child.heuristic, id(child), child, path + [child.position]))
        end_time = time.time()
        execution_time = end_time - start_time
        if best_path:
            logger.info(f"Greedy Search - Running time: {execution_time:.4f}s, Expanded nodes: {expanded_nodes}, Score: {best_heuristic_score}, Length: {len(best_path)}") # Changed to best heuristic score
        else:
            logger.info(f"Greedy Search - Running time: {execution_time:.4f}s, Expanded nodes: {expanded_nodes}, No solution found.")
        return best_path
        
    @staticmethod
    def depth_limited_search(play_tree, depth_limit):
        """
        Performs Depth-Limited Search (DLS) to find a path to victory within a given depth limit.
        """
        start_time = time.time()
        stack = [(play_tree.root, [], 0, 0)]  # Stack of (node, path, depth, cost)
        visited_boards = set()
        expanded_nodes = 0
        best_solution = None

        while stack:
            node, path, depth, cost = stack.pop()
            expanded_nodes += 1
            board_tuple = tuple(tuple(row) for row in node.game_controller.game_board.board)
            if board_tuple in visited_boards:
                continue
            visited_boards.add(board_tuple)

            if node.game_status == "victory":
                best_solution = (path + [node.position] if node.position else path, node.game_controller.score, cost)
                break

            if depth < depth_limit:
                for child in node.children:
                    new_path = path + [node.position] if node.position else path
                    new_cost = cost + child.cost
                    stack.append((child, new_path, depth + 1, new_cost))

        end_time = time.time()
        execution_time = end_time - start_time
        if best_solution:
            path, score, cost = best_solution
            logger.info(f"DLS - Running time: {execution_time:.4f}s, Expanded nodes: {expanded_nodes}, Score: {score}, Cost: {cost}, Length: {path}, Depth limit: {depth_limit}")
            return path
        else:
            logger.info(f"DLS - Running time: {execution_time:.4f}s, Expanded nodes: {expanded_nodes}, Score: None, Cost: None, Length: None, Depth limit: {depth_limit}")
            return None

    
    @staticmethod
    def iterative_deepening_search(play_tree, max_depth):
        """
        Performs Iterative Deepening Search (IDS) by repeatedly calling Depth-Limited Search
        with increasing depth limits.
        """
        start_time = time.time()
        expanded_nodes = 0
        best_solution = None
        best_depth = None
        total_cost = 0

        for depth_limit in range(max_depth + 1):
            result = SearchAlgorithms.depth_limited_search(play_tree, depth_limit)
            if result:
                best_solution = (result, play_tree.root.game_controller.score, total_cost)
                best_depth = depth_limit
                break
            # Calculate total cost (sum of costs from each DLS call)
            # Assuming each node has a 'cost' attribute
            if play_tree.root.children:
                total_cost += sum(child.cost for child in play_tree.root.children)

        end_time = time.time()
        execution_time = end_time - start_time
        if best_solution:
            path, score, cost = best_solution
            logger.info(f"IDS - Running time: {execution_time:.4f}s, Expanded nodes: {expanded_nodes}, Score: {score}, Cost: {cost}, Length: {path}, Best depth: {best_depth}, Max depth: {max_depth}")
            return path
        else:
            logger.info(f"IDS - Running time: {execution_time:.4f}s, Expanded nodes: {expanded_nodes}, Score: None, Cost: None, Length: None, Max depth: {max_depth}")
            return None
