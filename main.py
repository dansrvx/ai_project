import tkinter as tk
import argparse
from game_board import GameBoard
from piece import PieceSequence, piece_definitions
from game_controller import GameController
from game_gui import GameGUI
from play_tree import PlayTree

from logger_config import setup_logger 

logger = setup_logger() 

def run_game_headless():
    parser = argparse.ArgumentParser(description="Block Placement Game")
    parser.add_argument('--headless', action='store_true', help="Run in headless mode")
    parser.add_argument('--rows', type=int, default=5, help="Number of rows")
    parser.add_argument('--cols', type=int, default=5, help="Number of columns")
    parser.add_argument('--sequence_length', type=int, default=5, help="Sequence length")
    args = parser.parse_args() 

    """Run the game in headless mode."""
    logger.info(f"Starting headless game with Board {args.rows} x {args.cols}. Sequence: {args.sequence_length}.")
    game_board = GameBoard(args.rows, args.cols)
    game_board.initialize_board_state(fill_density=0.1, symmetric=True, edge_clear=True, sigma=1)
    piece_sequence = PieceSequence(piece_definitions, sequence_length=args.sequence_length)
    game_controller = GameController(game_board, piece_sequence)
    play_tree = PlayTree(game_controller, args.sequence_length)
    play_tree.print_tree()
    game_plan = SearchAlgorithms.a_star_search(play_tree)
    logger.info(f"A* Game Plan: {game_plan}")
    game_plan = SearchAlgorithms.greedy_search(play_tree)
    logger.info(f"Greedy Game Plan: {game_plan}")
    game_plan = SearchAlgorithms.depth_first_search(play_tree)
    logger.info(f"DFS Game Plan: {game_plan}")
    game_plan = SearchAlgorithms.breadth_first_search(play_tree)
    logger.info(f"BFS Game Plan: {game_plan}")
    game_plan = SearchAlgorithms.iterative_deepening_search(play_tree, args.sequence_length)
    logger.info(f"IDS Game Plan: {game_plan}")
    game_plan = SearchAlgorithms.uniform_cost_search(play_tree)
    logger.info(f"UCS Game Plan: {game_plan}")


if __name__ == '__main__':
    #Enable this code to run all the algorithms at same time.
    #python main.py --headless --rows 10 --cols 10 --sequence 10
    # run_game_headless()
    # exit()
    
    #Basic
    root = tk.Tk()
    gui = GameGUI(root)
    root.mainloop()