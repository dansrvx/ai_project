import tkinter as tk
import argparse
import time  # Import the time module

from game_board import GameBoard
from piece import PieceSequence, piece_definitions
from game_controller import GameController
from game_gui import GameGUI
from play_tree import PlayTree
from search_algorithms import SearchAlgorithms

from logger_config import setup_logger

logger = setup_logger()

def run_game_headless():
    parser = argparse.ArgumentParser(description="Block Placement Game")
    parser.add_argument('--headless', action='store_true', help="Run in headless mode")
    parser.add_argument('--rows', type=int, default=5, help="Number of rows")
    parser.add_argument('--cols', type=int, default=5, help="Number of columns")
    parser.add_argument('--sequence_length', type=int, default=5, help="Sequence length")
    parser.add_argument('--fill_density', type=float, default=0.1, help="Initial board fill density (0.0 to 1.0)")
    parser.add_argument('--diamond_rate', type=float, default=0.2, help="Diamond appearance rate (0 to 1)")
    args = parser.parse_args()

    """Run the game in headless mode with configurable fill density, diamond rate and timeout."""
    logger.info(f"Starting headless game with Board {args.rows} x {args.cols}. Sequence: {args.sequence_length}, Fill Density: {args.fill_density}, Diamond Rate: {args.diamond_rate}.")
    game_board = GameBoard(args.rows, args.cols)
    game_board.initialize_board_state(fill_density=args.fill_density, symmetric=True, edge_clear=True, sigma=1, diamond_rate=args.diamond_rate)
    piece_sequence = PieceSequence(piece_definitions, sequence_length=args.sequence_length)
    game_controller = GameController(game_board, piece_sequence)

    game_plan = SearchAlgorithms.a_star_search(game_controller)
    logger.info(f"A* Game Plan: {game_plan}")
    game_plan = SearchAlgorithms.greedy_search(game_controller)
    logger.info(f"Greedy Game Plan: {game_plan}")
    game_plan = SearchAlgorithms.depth_first_search(game_controller)
    logger.info(f"DFS Game Plan: {game_plan}")
    game_plan = SearchAlgorithms.breadth_first_search(game_controller)
    logger.info(f"BFS Game Plan: {game_plan}")
    game_plan = SearchAlgorithms.iterative_deepening_search(game_controller, args.sequence_length)
    logger.info(f"IDS Game Plan: {game_plan}")
    game_plan = SearchAlgorithms.uniform_cost_search(game_controller)
    logger.info(f"UCS Game Plan: {game_plan}")


if __name__ == '__main__':
    #Enable this code to run all the algorithms at same time with timeout.
    #python main.py --headless --rows 10 --cols 10 --sequence_length 10 --fill_density 0.3 --diamond_rate 0.3
    run_game_headless()
    exit()

    #Basic GUI execution
    #root = tk.Tk()
    #gui = GameGUI(root)
    #root.mainloop()