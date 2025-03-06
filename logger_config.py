import logging
import os

def setup_logger(log_file='search_log.log'):
    """Configures the logger to write to a file and to the console."""
    logger = logging.getLogger(__name__.split('.')[0]) # Get the root logger
    if not logger.handlers: # Check if there are already handlers
        logger.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        log_file_path = os.path.abspath(log_file)
        file_handler = logging.FileHandler(log_file_path)
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger

def board_to_string(board):
    """Converts the board into a string representation."""
    board_str = ""
    for row in board:
        board_str += " ".join(map(str, row)) + "\n"
    return board_str