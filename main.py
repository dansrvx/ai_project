import tkinter as tk
from game_board import GameBoard
from piece import PieceSequence, piece_definitions
from search_algorithms import AStarSearch, BreadthFirstSearch, UniformCostSearch, DFSearch  # Keep all, DFSearch
from game_controller import GameController
from game_gui import GameGUI


def create_difficulty_selection_window(root):
    """Creates the difficulty selection window."""
    difficulty_window = tk.Toplevel(root)
    difficulty_window.title("Select Difficulty")

    # Difficulty levels and their corresponding parameters - MODIFIED DIFFICULTY LEVELS
    difficulties = {
        "Easy": {"rows": 5, "cols": 5, "sequence_length": 15, "fill_density": 0.4}, # MODIFIED
        "Intermediate": {"rows": 7, "cols": 7, "sequence_length": 15, "fill_density": 0.4}, # MODIFIED
        "Hard": {"rows": 10, "cols": 10, "sequence_length": 15, "fill_density": 0.4}, # MODIFIED
    }

    selected_difficulty = tk.StringVar(value="Intermediate")  # Default difficulty - MODIFIED to Intermediate

    # Create radio buttons for each difficulty level
    for difficulty_name, params in difficulties.items():
        radio_button = tk.Radiobutton(
            difficulty_window,
            text=difficulty_name,
            variable=selected_difficulty,
            value=difficulty_name,
            font=("Arial", 14)
        )
        radio_button.pack(anchor=tk.W, padx=20, pady=5)

    def start_game():
        """Starts the game based on selected difficulty."""
        difficulty = selected_difficulty.get()
        params = difficulties[difficulty]
        difficulty_window.destroy()  # Close difficulty selection window
        start_main_game_gui(root, params) # Start the main game GUI with selected parameters

    start_button = tk.Button(
        difficulty_window,
        text="Start Game",
        command=start_game,
        font=("Arial", 16),
        padx=20,
        pady=10
    )
    start_button.pack(pady=20)

    return difficulty_window


def start_main_game_gui(root, game_params):
    """Starts the main game GUI with specified parameters."""
    game_board = GameBoard(game_params["rows"], game_params["cols"])
    game_board.initialize_board_state(
        fill_density=game_params["fill_density"], symmetric=True, edge_clear=True, sigma=1
    )

    piece_sequence = PieceSequence(piece_definitions, sequence_length=game_params["sequence_length"])

    search_algorithm = BreadthFirstSearch()  # Default to BFS for score maximizing. You can change to DFSearch, AStarSearch, UniformCostSearch
    game_controller = GameController(game_board, piece_sequence, search_algorithm)

    gui = GameGUI(root, game_controller)
    root.deiconify() # Ensure main root window is shown (if it was hidden)


if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw() # Hide the main root window initially
    difficulty_selection_window = create_difficulty_selection_window(root)
    root.mainloop() # Start Tkinter main loop