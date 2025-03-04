import tkinter as tk
from game_board import GameBoard
from piece import PieceSequence, piece_definitions
from game_controller import GameController
from game_gui import GameGUI
from play_tree import PlayTree

if __name__ == '__main__':
    rows = 6
    cols = 6
    sequence_length = 10

    game_board = GameBoard(rows, cols)
    game_board.initialize_board_state(fill_density=0.35, symmetric=True, edge_clear=True, sigma=1)
    piece_sequence = PieceSequence(piece_definitions, sequence_length=sequence_length)
    game_controller = GameController(game_board, piece_sequence)

    root = tk.Tk()
    gui = GameGUI(root, game_controller)
    root.mainloop()