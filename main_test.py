import tkinter as tk
from game_board import GameBoard
from piece import PieceSequence, piece_definitions
from search_algorithms import UniformCostSearch, AStarSearch
from game_controller import GameController
from game_gui_test import GameGUI

if __name__ == '__main__':
    rows = 10
    cols = 10
    sequence_length = 30

    game_board = GameBoard(rows, cols)
    game_board.initialize_board_state(fill_density=0.4, symmetric=True, edge_clear=True, sigma=1)

    piece_sequence = PieceSequence(piece_definitions, sequence_length=sequence_length)

    search_algorithm = AStarSearch()
    game_controller = GameController(game_board, piece_sequence, search_algorithm)

    root = tk.Tk()
    gui = GameGUI(root, game_controller)
    root.mainloop()