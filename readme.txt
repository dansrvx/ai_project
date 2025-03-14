      
# Wood Block Puzzle AI Solver

## Summary

This project implements a wood block puzzle game with AI-powered solvers.  The game involves placing various shaped blocks onto a grid to clear lines and collect diamonds.  The project includes a graphical user interface (GUI) built with Tkinter for interactive gameplay, as well as headless mode for automated solving and algorithm benchmarking.  Several search algorithms are implemented to solve the puzzle: Depth-First Search (DFS), Breadth-First Search (BFS), A* Search, Greedy Search, Iterative Deepening Search (IDS), and Uniform Cost Search (UCS).

## Features

*   Interactive GUI:  Play the game manually through a user-friendly interface built with Tkinter.
*   Configurable Game Board:  Customize the game board size, fill density, diamond rate, and piece sequence length.
*   AI Solvers: Utilize various search algorithms to automatically solve the puzzle.
*   Headless Mode: Run the game and AI solvers without a GUI for testing and performance analysis.
*   Logging:  Comprehensive logging of game events, algorithm performance, and debugging information.
*   Game Statistics: track the time , the moves , the score and the CPU usage of all the algorithms
*   Game Configuration: The user can select if they want a symmetric game board

## File Structure

*   `main.py`:  The main entry point of the application.  Handles GUI initialization or headless execution based on command-line arguments.
*   `game_board.py`: Defines the `GameBoard` class, responsible for representing the game board and its state.
*   `piece.py`: Defines the `PieceSequence` class, responsible for generating and managing the sequence of pieces.
*   `game_controller.py`: Defines the `GameController` class, which manages the game logic, including piece placement, board updates, and game state checks.
*   `game_gui.py`: Defines the `GameGUI` class, which implements the graphical user interface using Tkinter.
*   `search_algorithms.py`:  Implements the search algorithms (DFS, BFS, A*, Greedy, IDS, UCS) to solve the puzzle.
*   `logger_config.py`:  Configures the logging system for the application.
*   `README.txt`: This file, providing an overview of the project.
*   `requirements.txt`:  A list of Python packages required to run the project.

## Requirements

*   Python 3.7+
*   Tkinter (usually included with Python installations, but may require separate installation on some systems)
*   Libraries listed in `requirements.txt` (install using `pip install -r requirements.txt`)

## Installation

1.  Clone the repository:

    ```bash
    git clone <repository_url>
    cd <project_directory>
    ```

2.  Create a virtual environment (recommended):

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Linux/macOS
    venv\Scripts\activate  # On Windows
    ```

3.  Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

### Running the GUI

To start the game with the graphical user interface, simply run the `main.py` script:

```bash
python main.py

    Start the GUI by running python main.py.

    Configure the game board parameters (rows, columns, fill density, diamond rate, and sequence length).

    Click "Start Game" to initialize the game.

    Click the buttons of the planning algorithm to get the game plan (DFS, BFS, A*, Greedy, IDS or UCS).

    The user can play manually if the calculation of the game plan fails.

    If a game plan is available (after calling the algorithms to make the plan), click the "Play AI" button to let the AI automatically play the game.

    The "Restart Game" button will return the board to the initial state, where the user can change the parameters.

Logging

The project uses a logger to track the game state. All events are saved at search_log.log.
Credits

    This project was created by DM, AO, RP [MECD AI Project]