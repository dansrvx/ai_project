import tkinter as tk
from tkinter import messagebox

from uri_template import expand

import game_controller as game_controller
from play_tree import PlayTree
from search_algorithms import SearchAlgorithms
from logger_config import setup_logger, board_to_string
from game_board import GameBoard
from piece import PieceSequence, piece_definitions

logger = setup_logger()

# --- Global UI settings ---
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 1000
FONT_LARGE = ("Arial", 13)
FONT_MEDIUM = ("Arial", 11)
FONT_SMALL = ("Arial", 9)
BUTTON_WIDTH = 18  # Adjusted button width
BUTTON_HEIGHT = 1
PARAMETER_LABEL_WIDTH = 15  # Width for parameter labels
STATISTICS_TEXT_WIDTH = 30  # Width for statistics texts
CELL_BORDER_WIDTH = 1
CELL_COLORS = {0: "white", 1: "blue", 2: "red", "last_placed": "green"}
HIGHLIGHT_COLOR = "yellow"

INTERFACE_ROWS = 4
INTERFACE_COLS = 2

# --- Layout configuration ---
ROW_0_HEIGHT = 5  # Row 0 occupies 5% of the vertical space
ROW_1_HEIGHT = 30  # Row 1 occupies 15% of the vertical space
ROW_2_HEIGHT = 50  # Row 2 occupies 60% of the vertical space
ROW_3_HEIGHT = 15  # Row 2 occupies 20% of the vertical space

COLUMN_0_WIDTH = 70
COLUMN_1_WIDTH = 30

GAME_BUTTON_STYLE = {
    "bg": "#155724", "fg": "white", "activebackground": "#0b3d20"
}
PLAN_BUTTON_STYLE = {
    "bg": "#003366", "fg": "white", "activebackground": "#002244"
}

MAX_BOARD_SIZE = 15
MAX_SEQUENCE = 10

class GameGUI:
    """
    Initializes the game GUI with a grid layout and sliders for percentage parameters.
    """

    def __init__(self, root):
        """
        Initializes the GameGUI with the root Tk window and defines all attributes.
        Organizes UI elements using the grid geometry manager.
        """
        self.root = root
        self.root.title("Wood Block Puzzle - By DM, AO, RP [MECD AI Project]")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.resizable(False, False)

        # --- Game-related attributes ---
        self.game = None
        # self.last_placed_positions = [] delete last placed piece highlight
        # self.play_tree = None
        self.game_plan = None
        self.algorithm_statistics = []

        # --- UI Elements - Frames ---
        self.general_frame = None
        self.score_bar_frame = None  # Frame for the score bar
        self.game_configuration_frame = None
        self.parameter_frame = None
        self.statistics_frame = None  # Frame for game statistics
        self.game_area_frame = None  # Frame to hold board and next piece display
        self.board_frame = None
        self.next_piece_frame = None
        self.input_frame = None
        self.game_button_frame = None  # Frame for manual/AI play buttons
        self.manual_play_frame = None
        self.plan_button_frame = None  # Frame for AI planning buttons
        self.plan_frame = None
        self.algorithm_statistics_frame = None


        # --- UI Elements - Labels ---
        self.score_label = None
        self.remaining_pieces_label = None
        self.status_label = None
        self.next_piece_label = None
        self.total_diamonds_label = None
        self.plan_label = None
        self.statistic_labels = None

        # --- UI Elements - Input Fields and Variables (Parameter Selection) ---
        self.row_entry = None
        self.col_entry = None
        self.density_slider = None
        self.density_label = None
        self.diamond_slider = None
        self.diamond_label = None
        self.sequence_entry = None
        self.symmetric_var = tk.BooleanVar(value=True)
        self.symmetric_check = None

        # --- UI Elements - Input Fields (Gameplay) ---
        self.row_entry_play = None
        self.col_entry_play = None

        # --- UI Elements - Buttons ---
        self.accept_button = None
        self.manual_button = None
        self.ai_button = None
        self.dfs_button = None
        self.bfs_button = None
        self.a_star_button = None
        self.a_greedy_button = None
        self.ids_button = None
        self.restart_button = None

        # Game board cells
        self.cells = {}

        # --- Initialize UI elements ---
        self.initialize_ui()

    def initialize_ui(self):
        """
        Initializes and arranges all UI elements using the grid geometry manager.
        """
        padding_x = 5
        padding_y = 2


        self.general_frame = tk.Frame(self.root, height=WINDOW_HEIGHT-20, width=WINDOW_WIDTH-20, borderwidth=5,  relief=tk.FLAT)
        self.general_frame.pack(fill=tk.BOTH, expand=True)
        self.general_frame.grid_rowconfigure(0, weight=ROW_0_HEIGHT)
        self.general_frame.grid_rowconfigure(1, weight=ROW_1_HEIGHT)
        self.general_frame.grid_rowconfigure(2, weight=ROW_2_HEIGHT)
        self.general_frame.grid_rowconfigure(3, weight=ROW_3_HEIGHT)
        self.general_frame.grid_columnconfigure(0, weight=1)


        self.score_bar_frame = tk.Frame(self.general_frame, borderwidth=5, relief=tk.GROOVE)
        self.score_bar_frame.grid(row=0, column=0, padx=padding_x, pady=padding_y, sticky="nsew")
        self.score_bar_frame.grid_propagate(False)

        self.game_configuration_frame = tk.Frame(self.general_frame, borderwidth=5, relief=tk.GROOVE)
        self.game_configuration_frame.grid(row=1, column=0, padx=padding_x, pady=padding_y, sticky="nsew")
        self.game_configuration_frame.grid_propagate(False)

        self.game_area_frame = tk.Frame(self.general_frame, borderwidth=5, relief=tk.GROOVE)
        self.game_area_frame.grid(row=2, column=0, padx=padding_x, pady=padding_y, sticky="nsew")
        self.game_area_frame.grid_propagate(False)

        self.input_frame = tk.Frame(self.general_frame, borderwidth=5, relief=tk.GROOVE)
        self.input_frame.grid(row=3, column=0, padx=padding_x, pady=padding_y, sticky="nsew")
        self.input_frame.grid_propagate(False)

        self.initialize_score_bar()
        self.initialize_configuration_area()
        self.initialize_game_area()
        self.initialize_button_frames()
        self.initialize_status_label()

        # --- Initial UI State ---
        self.cells = {}  # Reset cells for the new board
        self.disable_board_and_buttons()
        self.update_board_display()
        self.update_next_piece_display()
        self.update_score_display()
        self.update_remaining_pieces_label()
        self.update_total_diamonds_label()

        # Initialize parameter selection UI
        self.parameter_frame.tkraise()  # Make sure parameter frame is visible at start

    def initialize_score_bar(self):
        """
        Initializes the score bar at the top of the GUI.
        """
        self.score_bar_frame.grid_rowconfigure(0, weight=1)
        self.score_bar_frame.grid_columnconfigure(0, weight=1)
        self.score_bar_frame.grid_columnconfigure(1, weight=1)
        self.score_bar_frame.grid_columnconfigure(2, weight=1)

        self.score_label = tk.Label(self.score_bar_frame, text="Score: 0", font=FONT_MEDIUM)
        self.score_label.grid(row=0, column=0, padx=10, pady=1, sticky="nsw")

        self.remaining_pieces_label = tk.Label(self.score_bar_frame, text="Remaining Pieces: 0", font=FONT_MEDIUM)
        self.remaining_pieces_label.grid(row=0, column=1, padx=10, pady=1, sticky="ns")

        self.total_diamonds_label = tk.Label(self.score_bar_frame, text="Total Diamonds: 0", font=FONT_MEDIUM)
        self.total_diamonds_label.grid(row=0, column=2, padx=10, pady=1, sticky="nse")


    def initialize_configuration_area(self):
        self.game_configuration_frame.grid_rowconfigure(0, weight=1)
        self.game_configuration_frame.grid_columnconfigure(0, weight=4)
        self.game_configuration_frame.grid_columnconfigure(1, weight=2)
        self.game_configuration_frame.grid_propagate(False)

        self.initialize_parameter_selection()
        self.initialize_statistics_frame()

    def initialize_parameter_selection(self):
        """
        Initializes the parameter selection frame and input fields with a 6x3 grid layout,
        occupying the full width and with column widths adjusted to 30%, 50%, 20%.
        """
        padding = 3

        self.parameter_frame = tk.Frame(self.game_configuration_frame, borderwidth=5, relief=tk.GROOVE)
        self.parameter_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.parameter_frame.grid_propagate(False)

        self.parameter_frame.grid_rowconfigure(0, weight=1)
        self.parameter_frame.grid_rowconfigure(1, weight=1)
        self.parameter_frame.grid_rowconfigure(2, weight=2)
        self.parameter_frame.grid_rowconfigure(3, weight=2)
        self.parameter_frame.grid_rowconfigure(4, weight=1)
        self.parameter_frame.grid_rowconfigure(5, weight=1)
        self.parameter_frame.grid_rowconfigure(6, weight=2)

        self.parameter_frame.grid_columnconfigure(0, weight=25)
        self.parameter_frame.grid_columnconfigure(1, weight=50)
        self.parameter_frame.grid_columnconfigure(2, weight=25)

        # --- Parameter Input Fields, using a 6x3 grid ---

        # Board Rows
        tk.Label(self.parameter_frame, text="Board Rows:", font=FONT_MEDIUM, anchor="w").grid(row=0, column=0, sticky="nsew", padx=padding, pady=padding)
        self.row_entry = tk.Entry(self.parameter_frame, width=5, font=FONT_MEDIUM)
        self.row_entry.insert(0, "5")
        tk.Label(self.parameter_frame, text="(Max: "+str(MAX_BOARD_SIZE)+")", font=FONT_SMALL, anchor="center").grid(row=0, column=2, sticky="nsew", padx=padding, pady=padding)  # Center alignment
        self.row_entry.grid(row=0, column=1, sticky="nsew", padx=padding, pady=padding)

        # Board Columns
        tk.Label(self.parameter_frame, text="Board Columns:", font=FONT_MEDIUM, anchor="w").grid(row=1, column=0, sticky="nsew", padx=padding, pady=padding)
        self.col_entry = tk.Entry(self.parameter_frame, width=5, font=FONT_MEDIUM)
        self.col_entry.insert(0, "5")
        tk.Label(self.parameter_frame, text="(Max: "+str(MAX_BOARD_SIZE)+")", font=FONT_SMALL, anchor="center").grid(row=1, column=2, sticky="nsew", padx=padding, pady=padding)  # Center alignment
        self.col_entry.grid(row=1, column=1, sticky="nsew", padx=padding, pady=padding)

        # Fill Density
        tk.Label(self.parameter_frame, text="Fill Density:", font=FONT_MEDIUM, anchor="w").grid(row=2, column=0, sticky="nsew", padx=padding, pady=padding)
        self.density_slider = tk.Scale(self.parameter_frame, from_=0, to=100, orient=tk.HORIZONTAL, command=self.update_density_label, length=150)
        self.density_slider.set(30)
        self.density_label = tk.Label(self.parameter_frame, text="30%", font=FONT_SMALL, anchor="center")
        tk.Label(self.parameter_frame, text="(0% - 100%)", font=FONT_SMALL, anchor="center").grid(row=2, column=2, sticky="nsew", padx=padding, pady=padding)  # Center alignment# Center alignment
        self.density_slider.grid(row=2, column=1, sticky="nsew", padx=padding, pady=padding)

        # Diamond Rate
        tk.Label(self.parameter_frame, text="Diamond Rate:", font=FONT_MEDIUM, anchor="w").grid(row=3, column=0, sticky="nsew", padx=padding, pady=padding)
        self.diamond_slider = tk.Scale(self.parameter_frame, from_=0, to=100, orient=tk.HORIZONTAL, command=self.update_diamond_label, length=150)
        self.diamond_slider.set(20)
        self.diamond_label = tk.Label(self.parameter_frame, text="20%", font=FONT_SMALL, anchor="center")
        tk.Label(self.parameter_frame, text="(0% - 100%)", font=FONT_SMALL, anchor="center").grid(row=3, column=2, sticky="nsew", padx=padding, pady=padding)  # Center alignment# Center alignment
        self.diamond_slider.grid(row=3, column=1, sticky="nsew", padx=padding, pady=padding)

        # Sequence Length
        tk.Label(self.parameter_frame, text="Sequence Length:", font=FONT_MEDIUM, anchor="w").grid(row=4, column=0, sticky="nsew", padx=padding, pady=padding)
        self.sequence_entry = tk.Entry(self.parameter_frame, width=5, font=FONT_MEDIUM)
        self.sequence_entry.insert(0, "5")
        tk.Label(self.parameter_frame, text="(Max: 20)", font=FONT_SMALL, anchor="center").grid(row=4, column=2, sticky="nsew", padx=padding, pady=padding)
        self.sequence_entry.grid(row=4, column=1, sticky="nsew", padx=padding, pady=padding)

        # Symmetric Board
        tk.Label(self.parameter_frame, text="Symmetric Board:", font=FONT_MEDIUM, anchor="w").grid(row=5, column=0, sticky="nsew", padx=padding, pady=padding)
        self.symmetric_var = tk.BooleanVar(value=True)
        self.symmetric_check = tk.Checkbutton(self.parameter_frame, text="", variable=self.symmetric_var, anchor="w")  # Removed the text, using only the check mark
        tk.Label(self.parameter_frame, text="False/True", font=FONT_SMALL, anchor="center").grid(row=5, column=2, sticky="nsew", padx=padding, pady=padding)
        self.symmetric_check.grid(row=5, column=1, sticky="nsew", padx=padding, pady=padding)

        # Start Game Button
        self.accept_button = tk.Button(self.parameter_frame, text="Start Game", command=self.accept_parameters, font=FONT_LARGE, **GAME_BUTTON_STYLE)
        self.accept_button.grid(row=6, column=0, columnspan=3, pady=10, sticky="ew")  # Span all three columns

    def initialize_statistics_frame(self):
        """
        Initializes the statistics frame.
        """
        self.algorithm_statistics = {}  # Initialize dictionary to store statistics
        self.statistic_labels = {}  # Dictionary to store statistic values.

        self.statistics_frame = tk.Frame(self.game_configuration_frame, borderwidth=5, relief=tk.GROOVE)
        self.statistics_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        # Configure grid rows
        self.statistics_frame.grid_rowconfigure(0, weight=2)  # Row for plan
        self.statistics_frame.grid_rowconfigure(1, weight=6)  # Row for table
        self.statistics_frame.grid_columnconfigure(0, weight=1)  # Full Width
        self.statistics_frame.grid_propagate(False)  # Prevent automatic resizing

        # Plan Label
        self.plan_frame = tk.Frame(self.statistics_frame, borderwidth=5, relief=tk.GROOVE)
        self.plan_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.plan_frame.grid_rowconfigure(0, weight=1)
        self.plan_frame.grid_columnconfigure(0, weight=1)
        self.plan_frame.grid_propagate(False)
        self.plan_label = tk.Label(self.plan_frame, text="Game Plan: N/A", font=FONT_SMALL, anchor="w")
        self.plan_label.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        self.algorithm_statistics_frame = tk.Frame(self.statistics_frame, borderwidth=5, relief=tk.GROOVE)
        self.algorithm_statistics_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.algorithm_statistics_frame.grid_rowconfigure(0, weight=2)
        self.algorithm_statistics_frame.grid_rowconfigure(1, weight=2)
        self.algorithm_statistics_frame.grid_rowconfigure(2, weight=2)
        self.algorithm_statistics_frame.grid_rowconfigure(3, weight=2)
        self.algorithm_statistics_frame.grid_rowconfigure(4, weight=2)
        columns = ["Algorithm", "Time (s)", "Memory (KB)", "Nodes", "Moves", "Success"]
        for i in range(len(columns)):
            self.algorithm_statistics_frame.grid_columnconfigure(i, weight=1)
            header_label = tk.Label(self.algorithm_statistics_frame, text=columns[i], font=FONT_SMALL, relief=tk.FLAT, padx=2, pady=2)
            header_label.grid(row=0, column=i, sticky="nsew", padx=5, pady=5)


    def initialize_game_area(self):
        """
        Initializes the game area frame and calls methods to set up the board and next piece displays.
        """
        self.game_area_frame.grid_rowconfigure(0, weight=1)
        self.game_area_frame.grid_columnconfigure(0, weight=4)
        self.game_area_frame.grid_columnconfigure(1, weight=2)
        self.game_area_frame.grid_propagate(False)

        # Call methods to initialize the board and next piece displays
        self.initialize_board_display()
        self.initialize_next_piece_display()

    def initialize_board_display(self):
        """
        Initializes the board display frame.
        """
        self.board_frame = tk.Frame(self.game_area_frame, borderwidth=5, relief=tk.GROOVE)
        self.board_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.board_frame.grid_rowconfigure(0, weight=1)  # Allows to center the content
        self.board_frame.grid_columnconfigure(0, weight=1)  # Allows to center the content
        self.board_frame.grid_propagate(False)



    def initialize_next_piece_display(self):
        """
        Initializes the next piece display frame.
        """
        self.next_piece_frame = tk.Frame(self.game_area_frame, borderwidth=5, relief=tk.GROOVE)
        self.next_piece_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        self.next_piece_frame.rowconfigure(0, weight=4)
        self.next_piece_frame.rowconfigure(1, weight=1)
        self.next_piece_frame.rowconfigure(2, weight=1)
        self.next_piece_frame.columnconfigure(0, weight=1)
        self.next_piece_frame.grid_propagate(False)

    def initialize_button_frames(self):
        """
        Initializes the button frames for manual/AI control and AI planning.
        """
        self.input_frame.grid_rowconfigure(0, weight=1)
        self.input_frame.grid_columnconfigure(0, weight=4)
        self.input_frame.grid_columnconfigure(1, weight=2)
        self.input_frame.grid_propagate(False)

        # Initialize the buttons of every part
        self.initialize_game_buttons()
        self.initialize_plan_buttons()

    def initialize_game_buttons(self):
        """
        Initializes the manual/AI control buttons within the specified frame.
        """
        self.game_button_frame = tk.Frame(self.input_frame, borderwidth=5, relief=tk.GROOVE)
        self.game_button_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        self.game_button_frame.grid_rowconfigure(0, weight=10)
        self.game_button_frame.grid_rowconfigure(1, weight=1)
        self.game_button_frame.grid_rowconfigure(2, weight=1)
        self.game_button_frame.grid_columnconfigure(0, weight=1)
        self.game_button_frame.grid_propagate(False)

        self.manual_play_frame = tk.Frame(self.game_button_frame, bd=2, relief=tk.FLAT)
        self.manual_play_frame.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        self.manual_play_frame.grid_rowconfigure(0, weight=1)
        self.manual_play_frame.grid_columnconfigure(0, weight=1)
        self.manual_play_frame.grid_columnconfigure(1, weight=1)
        self.manual_play_frame.grid_columnconfigure(2, weight=1)
        self.manual_play_frame.grid_columnconfigure(3, weight=1)
        self.manual_play_frame.grid_columnconfigure(4, weight=1)
        self.manual_play_frame.grid_propagate(False)

        tk.Label(self.manual_play_frame, text="Row:", font=FONT_MEDIUM).grid(row=0, column=0, sticky="nsew")
        self.row_entry_play = tk.Entry(self.manual_play_frame, width=5, font=FONT_MEDIUM)
        self.row_entry_play.grid(row=0, column=1, sticky="nsew", padx=5, pady=1)

        tk.Label(self.manual_play_frame, text="Col:", font=FONT_MEDIUM).grid(row=0, column=2, sticky="nsew")
        self.col_entry_play = tk.Entry(self.manual_play_frame, width=5, font=FONT_MEDIUM)
        self.col_entry_play.grid(row=0, column=3, sticky="nsew", padx=5, pady=1)

        self.manual_button = tk.Button(self.manual_play_frame, text="Play Manually", command=self.manual_play_gui, font=FONT_LARGE, **GAME_BUTTON_STYLE)
        self.manual_button.grid(row=0, column=4, sticky="nsew", padx=5, pady=1)

        self.ai_button = tk.Button(self.game_button_frame, text="Play AI", command=self.play_ai_turn, font=FONT_LARGE, state=tk.DISABLED, **GAME_BUTTON_STYLE)
        self.ai_button.grid(row=1, column=0, sticky="nsew", padx=5, pady=1)

        self.restart_button = tk.Button(self.game_button_frame, text="Restart Game", command=self.restart_game, font=FONT_LARGE, **GAME_BUTTON_STYLE)
        self.restart_button.grid(row=2, column=0, sticky="nsew", padx=5, pady=1)

    def initialize_plan_buttons(self):
        """
        Initializes the AI planning buttons within the specified frame.
        """
        # Configure grid rows and columns to expand
        self.plan_button_frame = tk.Frame(self.input_frame, borderwidth=5, relief=tk.GROOVE)
        self.plan_button_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.plan_button_frame.grid_rowconfigure(0, weight=1)
        self.plan_button_frame.grid_rowconfigure(1, weight=1)
        self.plan_button_frame.grid_rowconfigure(2, weight=1)
        self.plan_button_frame.grid_columnconfigure(0, weight=1)
        self.plan_button_frame.grid_columnconfigure(1, weight=1)
        self.plan_button_frame.grid_propagate(False)

        self.dfs_button = tk.Button(self.plan_button_frame, text="DFS Plan", command=lambda: self.get_game_plan('DFS'), font=FONT_LARGE, **PLAN_BUTTON_STYLE)
        self.dfs_button.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)  # Use grid within this frame
        self.bfs_button = tk.Button(self.plan_button_frame, text="BFS Plan", command=lambda: self.get_game_plan('BFS'), font=FONT_LARGE, **PLAN_BUTTON_STYLE)
        self.bfs_button.grid(row=0, column=1, sticky="nsew", padx=2, pady=2)  # Use grid within this frame
        self.a_star_button = tk.Button(self.plan_button_frame, text="A* Plan", command=lambda: self.get_game_plan('A*'), font=FONT_LARGE, **PLAN_BUTTON_STYLE)
        self.a_star_button.grid(row=1, column=0, sticky="nsew", padx=2, pady=2)  # Use grid within this frame
        self.a_greedy_button = tk.Button(self.plan_button_frame, text="Greedy Plan", command=lambda: self.get_game_plan('Greedy'), font=FONT_LARGE, **PLAN_BUTTON_STYLE)
        self.a_greedy_button.grid(row=1, column=1, sticky="nsew", padx=2, pady=2)  # Use grid within this frame
        self.ids_button = tk.Button(self.plan_button_frame, text="IDS Plan", command=lambda: self.get_game_plan('IDS'), font=FONT_LARGE, **PLAN_BUTTON_STYLE)
        self.ids_button.grid(row=2, column=0, sticky="nsew", padx=2, pady=2)  # Use grid within this frame and span columns


    def initialize_status_label(self):
        """
        Initializes the status label at the bottom of the GUI.
        """
        self.status_label = tk.Label(self.next_piece_frame, text="Game Status", font=FONT_MEDIUM)
        self.status_label.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)  # Span two columns
        self.next_piece_label = tk.Label(self.next_piece_frame, text="Next piece", font=FONT_MEDIUM)
        self.next_piece_label.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)

    def update_density_label(self, value):
        """
        Updates the fill density label to show the selected percentage.
        """
        self.density_label.config(text=f"{value}%", anchor="center")  # center alignment to display correct values

    def update_diamond_label(self, value):
        """
        Updates the diamond rate label to show the selected percentage.
        """
        self.diamond_label.config(text=f"{value}%", anchor="center") #center alignment to display correct values

    def accept_parameters(self):
        """
        Handles the acceptance of game parameters, initializes the game, and enables UI elements.
        Keeps the parameter selection frame visible but disables its input elements.
        """
        try:
            rows = int(self.row_entry.get())
            cols = int(self.col_entry.get())
            fill_density = self.density_slider.get() / 100.0  # Get value from slider (0-100) and convert to 0.0-1.0
            diamond_rate = self.diamond_slider.get()
            sequence_length = int(self.sequence_entry.get())
            symmetric = self.symmetric_var.get()
        except ValueError:
            messagebox.showerror("Error", "Invalid input: Please enter valid numbers.")
            return

        # Basic input validation
        if not (0 < rows <= MAX_BOARD_SIZE and 0 < cols <= MAX_BOARD_SIZE):
            messagebox.showerror("Error", "Board dimensions must be between 1 and " + str(MAX_BOARD_SIZE) + ".")
            return
        if not (0 <= fill_density <= 1 and 0 <= diamond_rate <= 100):
            messagebox.showerror("Error", "Fill Density must be between 0 and 1, and Diamond Rate between 0 and 100.")
            return
        if not (0 < sequence_length <= MAX_SEQUENCE):
            messagebox.showerror("Error", "Sequence length must be between 1 and " + str(MAX_SEQUENCE) + ".")
            return

        # Initialize game board and piece sequence
        game_board = GameBoard(rows, cols)
        game_board.initialize_board_state(fill_density=fill_density, symmetric=symmetric, edge_clear=True, sigma=1, diamond_rate=diamond_rate)
        piece_sequence = PieceSequence(piece_definitions, sequence_length=sequence_length)
        self.game = game_controller.GameController(game_board, piece_sequence)

        # self.play_tree = self.calculate_tree()  # Recalculate the play tree

        # Enable game buttons and board interactions
        self.enable_game_buttons()

        # Update board display and other UI elements
        self.update_board_display()
        self.update_next_piece_display()
        self.update_score_display()
        self.update_remaining_pieces_label()
        self.update_total_diamonds_label()

        # Disable parameter input elements and the accept button, but keep the frame visible
        self.disable_parameter_inputs()

        logger.info(f"Game initialized with rows={rows}, cols={cols}, fill_density={fill_density}, diamond_rate={diamond_rate}, sequence_length={sequence_length}, symmetric={symmetric}")

    def disable_parameter_inputs(self):
        """
        Disables parameter input elements after game initialization.
        """
        self.row_entry.config(state=tk.DISABLED)
        self.col_entry.config(state=tk.DISABLED)
        self.density_slider.config(state=tk.DISABLED)
        self.diamond_slider.config(state=tk.DISABLED)
        self.sequence_entry.config(state=tk.DISABLED)
        self.symmetric_check.config(state=tk.DISABLED)
        self.accept_button.config(state=tk.DISABLED)

    def calculate_tree(self):
        """
        Calculates the play tree for the current game state.
        """
        if self.game:
            tree = PlayTree(self.game, len(self.game.piece_sequence.sequence))
            tree.print_tree()
            return tree
        else:
            logger.warning("Game not initialized. Cannot calculate play tree.")
            return None  # Or handle the case where the game hasn't been initialized yet.

    def get_game_plan(self, algorithm):
        """
        Calculates and stores the game plan using the specified algorithm and stores statistics.
        """
        if not self.game:
            messagebox.showerror("Error", "Game not initialized. Please set game parameters first.")
            return

        search_algorithm = {
            'DFS': SearchAlgorithms.depth_first_search,
            'BFS': SearchAlgorithms.breadth_first_search,
            'A*': SearchAlgorithms.a_star_search,
            'Greedy': SearchAlgorithms.greedy_search,
            'IDS': SearchAlgorithms.iterative_deepening_search
        }.get(algorithm)

        if not search_algorithm:
            logger.error(f"Invalid algorithm: {algorithm}")
            return

        statistics = search_algorithm(self.game)

        if statistics['plan']:
            self.game_plan = statistics['plan']
            logger.info(f"{algorithm} Game Plan calculated: {self.game_plan}")
            self.algorithm_statistics[algorithm] = statistics  # Overwrite if it exists
            self.show_game_over_message("Game plan calculated successfully")
            self.update_statistics_frame()
        else:
            self.game_plan = None
            logger.info(f"No {algorithm} Game Plan found.")
            self.algorithm_statistics[algorithm] = None
            self.show_game_over_message("Sorry! The AI could not found a successful game plan. You can play manually!")
        self.update_ai_button_state()

    def update_statistics_frame(self):
        """
        Updates the statistics frame with the latest algorithm statistics and game plan.
        """
        # Update Plan label
        last_algorithm = list(self.algorithm_statistics.keys())[-1] if self.algorithm_statistics else None
        if last_algorithm:
            self.plan_label.config(text=f"Game Plan: {self.game_plan}")
        else:
            self.plan_label.config(text=f"Game Plan: N/A")

        # Remove previous data to add the new one
        for widget in self.statistics_frame.winfo_children():
            if widget.grid_info()['row'] > 1:
                widget.destroy()

        row_num = 2

        # Populate table with statistics
        for algorithm, statistics in self.algorithm_statistics.items():
            if statistics:
                data = [
                    algorithm,
                    f"{statistics['execution_time']:.4f}",
                    f"{statistics['memory_usage']:.2f}",
                    str(statistics['nodes_explored']),
                    str(statistics['path_length']),
                    str(statistics['success'])
                ]

                for i, value in enumerate(data):
                    data_label = tk.Label(self.algorithm_statistics_frame, text=value, font=FONT_SMALL, borderwidth=1, relief="solid")
                    data_label.grid(row=row_num, column=i, sticky="nsew", padx=1, pady=1)
                row_num += 1

    def update_ai_button_state(self):
        """
        Enables or disables the AI button based on the availability of a game plan.
        """
        if self.game_plan:  # If a valid game plan exists, enable AI button
            self.ai_button.config(state=tk.NORMAL)
        else:
            self.ai_button.config(state=tk.DISABLED)

    def update_board_display(self):
        """
        Updates the board display.
        """
        if self.game:
            self.create_board_grid()
            self.update_cell_colors()

    def create_board_grid(self):
        """
        Creates the board grid with row and column labels integrated into a single grid.
        """
        # Destroy old cells before creating a new board
        for cell in self.cells.values():
            cell.destroy()
        self.cells = {}

        # Access board from the game controller
        board = self.game.game_board.board
        rows = self.game.game_board.rows
        cols = self.game.game_board.cols

        # Configure grid rows and columns
        for i in range(rows + 1):
            self.board_frame.grid_rowconfigure(i, weight=1)  # Each row can expand
        for j in range(cols + 1):
            self.board_frame.grid_columnconfigure(j, weight=1)  # Each col can expand

        # Create column labels
        for c in range(cols):
            col_label = tk.Label(self.board_frame, text=str(c), font=FONT_SMALL)
            col_label.grid(row=0, column=c + 1, padx=0, pady=0, sticky="nsew")

        # Create row labels and cells
        for r in range(rows):
            row_label = tk.Label(self.board_frame, text=str(r), font=FONT_SMALL)
            row_label.grid(row=r + 1, column=0, padx=0, pady=0, sticky="nsew")
            for c in range(cols):
                if (r, c) not in self.cells:
                    cell_label = tk.Label(self.board_frame, width=2, height=1, relief=tk.SOLID,
                                          borderwidth=CELL_BORDER_WIDTH, font=FONT_SMALL)
                    cell_label.grid(row=r + 1, column=c + 1, padx=1, pady=1, sticky="nsew")
                    cell_label.bind("<Button-1>", lambda event, row=r, col=c: self.on_cell_click(row, col))
                    cell_label.bind("<Enter>", lambda event, row=r, col=c: self.on_cell_enter(row, col))
                    cell_label.bind("<Leave>", lambda event, row=r, col=c: self.on_cell_leave(row, col))
                    self.cells[(r, c)] = cell_label

    def on_cell_enter(self, row, col):
        """
        Handles cell enter events (hover effect).
        """
        if self.game:
            self.cells[(row, col)].config(bg=HIGHLIGHT_COLOR)

    def on_cell_leave(self, row, col):
        """
        Handles cell leave events (reverts hover effect).
        """
        if self.game:
            self.update_cell_color(row, col)

    def on_cell_click(self, row, col):
        """
        Handles cell click events.
        """
        if self.game:
            if self.manual_play(row, col):
                self.update_ui_after_move()

    def update_cell_colors(self):
        """
        Updates the colors of the cells on the board based on the game state.
        """
        if self.game:
            # Access board from the game controller
            board = self.game.game_board.board
            for r in range(self.game.game_board.rows):
                for c in range(self.game.game_board.cols):
                    self.update_cell_color(r, c)

    def update_cell_color(self, row, col):
        """
        Updates the color of a specific cell based on its value and whether it was last placed.
        """
        '''
        if self.game:            
            if (row, col) in self.last_placed_positions:
                color = CELL_COLORS["last_placed"]
            else:
                # Access board from the game controller
                board = self.game.game_board.board
                cell_value = board[row][col]
                color = CELL_COLORS.get(cell_value, "white")
            self.cells[(row, col)].config(bg=color)
        '''
        # Access board from the game controller
        board = self.game.game_board.board
        cell_value = board[row][col]
        color = CELL_COLORS.get(cell_value, "white")
        self.cells[(row, col)].config(bg=color)

    def update_next_piece_display(self):
        """
        Updates the next piece display.
        """
        if self.game:
            self.clear_next_piece_frame()
            next_piece_info = self.game.piece_sequence.peek_next_piece()
            if next_piece_info:
                next_piece_name, next_piece_shape = next_piece_info
                self.next_piece_label.config(text=f"Next Piece: {next_piece_name}")
                self.draw_next_piece_grid(next_piece_shape)
            else:
                self.next_piece_label.config(text="No more pieces")

    def clear_next_piece_frame(self):
        """
        Clears the next piece frame.
        """
        if self.game:
            for widget in self.next_piece_frame.winfo_children():
                if widget.grid_info()["row"] == 0:  # Solo los widgets en la fila 0
                    widget.destroy()

    def draw_next_piece_grid(self, shape):
        """
        Draws the next piece grid.
        """
        if self.game:
            piece_grid = tk.Frame(self.next_piece_frame)
            piece_grid.grid(row=0, column=0, padx=1, pady=1)
            for r in range(len(shape)):
                piece_grid.grid_rowconfigure(r, weight=1)
                for c in range(len(shape[0])):
                    piece_grid.grid_columnconfigure(c, weight=1)
                    color = "red" if shape[r][c] == 2 else "blue" if shape[r][c] == 1 else "white"
                    tk.Label(piece_grid, width=2, height=1, relief=tk.SOLID, borderwidth=CELL_BORDER_WIDTH,
                             bg=color).grid(row=r, column=c, padx=1, pady=1)

    def update_score_display(self):
        """
        Updates the score label.
        """
        if self.game:
            self.score_label.config(text=f"Score: {self.game.score}")
            logger.info(f"Score: {self.game.score}")

    def update_remaining_pieces_label(self):
        """
        Updates the remaining pieces label.
        """
        if self.game:
            self.remaining_pieces_label.config(text=f"Remaining Pieces: {len(self.game.piece_sequence.sequence)}")
            logger.info(f"Remaining Pieces: {len(self.game.piece_sequence.sequence)}")

    def update_total_diamonds_label(self):
        """
        Updates the total diamonds label.
        """
        if self.game:
            self.total_diamonds_label.config(text=f"Total Diamonds: {self.game.total_diamonds}")
            logger.info(f"Total Diamonds: {self.game.total_diamonds}")

    def manual_play_gui(self):
        """
        Handles manual piece placement from user input.
        """
        if not self.game:
            messagebox.showerror("Error", "Game not initialized. Please set game parameters first.")
            return

        self.check_game_status()
        try:
            row = int(self.row_entry_play.get())
            col = int(self.col_entry_play.get())
        except ValueError:
            self.status_label.config(text="Invalid input: Row and Column must be integers.")
            return

        if self.manual_play(row, col):
            self.update_ui_after_move()
            self.row_entry_play.delete(0, tk.END)
            self.col_entry_play.delete(0, tk.END)

    def manual_play(self, row, col):
        """
        Attempts to place a piece manually at the given row and column.
        """
        if self.game:
            placed_positions = self.game.play(row, col)
            if placed_positions:
                # self.last_placed_positions = placed_positions
                self.status_label.config(text="Piece placed successfully.")
                logger.info("Piece placed successfully.")
                return True
            else:
                self.status_label.config(text="Invalid move. Try again.")
                logger.info("Invalid move. Try again.")
                return False
        return False

    def play_ai_turn(self):
        """
        Makes the AI play one step and updates the UI.
        Ends the game and shows a message if no game plan is found.
        """
        if not self.game:
            messagebox.showerror("Error", "Game not initialized. Please set game parameters first.")
            return

        self.check_game_status()

        if not self.game_plan:
            self.show_game_over_message("AI has no precalculated plan. Please select a planning algorithm first.")
            self.disable_game_buttons()
            return

        next_move = self.game_plan.pop(0)
        if self.manual_play(next_move[0], next_move[1]):
            self.update_ui_after_move()
            logger.info(f"AI played move {next_move}. Remaining game plan: {self.game_plan}")
        else:
            self.status_label.config(text="AI couldn't find a valid move in the generated game plan. Game Over.")
            self.disable_game_buttons()
            self.show_game_over_message("AI couldn't find a valid move in the generated game plan. Game Over.")

    def update_ui_after_move(self):
        """
        Updates the UI elements after a move has been made.
        """
        if self.game:
            self.update_board_display()
            self.update_next_piece_display()
            self.update_score_display()
            self.update_remaining_pieces_label()
            self.update_total_diamonds_label()
            logger.info(f"Board:\n{board_to_string(self.game.game_board.board)}")
            self.check_game_status()

    def check_game_status(self):
        """
        Checks the game status and displays a message if the game ends.
        """
        if self.game:
            game_over_status = self.game.is_game_over()
            if game_over_status == "victory":
                self.show_game_over_message("Congratulations! You collected all the diamonds. Victory!")
                self.disable_game_buttons()
            elif game_over_status == "defeat":
                self.show_game_over_message("Sorry! You have lost. Defeat!")
                self.disable_game_buttons()
            else:
                logger.info("The player can keep playing")

    def show_game_over_message(self, message):
        """
        Displays a game over message.
        """
        messagebox.showinfo("Game Over", f"{message}\nScore: {self.game.score}")
        logger.info(f"{message}\nScore: {self.game.score}")

    def disable_game_buttons(self):
        """
        Disables the game buttons.
        """
        self.manual_button.config(state=tk.DISABLED)
        self.ai_button.config(state=tk.DISABLED)
        self.dfs_button.config(state=tk.DISABLED)
        self.bfs_button.config(state=tk.DISABLED)
        self.a_star_button.config(state=tk.DISABLED)
        self.a_greedy_button.config(state=tk.DISABLED)
        self.ids_button.config(state=tk.DISABLED)
        # Disable the board interaction as well
        self.disable_board()

    def enable_game_buttons(self):
        """
        Enables the game buttons.
        """
        self.manual_button.config(state=tk.NORMAL)
        self.dfs_button.config(state=tk.NORMAL)
        self.bfs_button.config(state=tk.NORMAL)
        self.a_star_button.config(state=tk.NORMAL)
        self.a_greedy_button.config(state=tk.NORMAL)
        self.ids_button.config(state=tk.NORMAL)
        # Enable board interaction
        self.enable_board()

    def disable_board(self):
        """
        Disable board interaction.
        """
        if self.game and hasattr(self, 'cells'):
            for r in range(self.game.game_board.rows):
                for c in range(self.game.game_board.cols):
                    if (r, c) in self.cells:
                        self.cells[(r, c)].unbind("<Button-1>")
                        self.cells[(r, c)].unbind("<Enter>")
                        self.cells[(r, c)].unbind("<Leave>")

    def enable_board(self):
        """
        Enable board interaction.
        """
        if self.game and hasattr(self, 'cells'):
            for r in range(self.game.game_board.rows):
                for c in range(self.game.game_board.cols):
                    if (r, c) in self.cells:
                        self.cells[(r, c)].bind("<Button-1>",
                                                lambda event, row=r, col=c: self.on_cell_click(row, col))
                        self.cells[(r, c)].bind("<Enter>", lambda event, row=r, col=c: self.on_cell_enter(row, col))
                        self.cells[(r, c)].bind("<Leave>", lambda event, row=r, col=c: self.on_cell_leave(row, col))

    def disable_board_and_buttons(self):
        """
        Disables all game buttons and the board interaction.
        """
        self.disable_game_buttons()
        if hasattr(self, 'cells'):
            self.disable_board()

    def enable_parameter_inputs(self):
        """
        Enables parameter input elements.
        """
        self.row_entry.config(state=tk.NORMAL)
        self.col_entry.config(state=tk.NORMAL)
        self.density_slider.config(state=tk.NORMAL)
        self.diamond_slider.config(state=tk.NORMAL)
        self.sequence_entry.config(state=tk.NORMAL)
        self.symmetric_check.config(state=tk.NORMAL)
        self.accept_button.config(state=tk.NORMAL)

    def restart_game(self):
        """
        Restarts the game with the same parameters.
        """
        # Re-enable parameter input elements
        self.enable_parameter_inputs()

        # Reset the game state
        self.game = None
        self.game_plan = None

        # Re-initialize the UI
        self.cells = {}  # Reset cells for the new board
        self.disable_board_and_buttons()
        self.update_board_display()
        self.update_next_piece_display()
        self.update_score_display()
        self.update_remaining_pieces_label()
        self.update_total_diamonds_label()

        # Clear the board and generate the pieces.
        # self.accept_parameters()

        logger.info("Game restarted.")


