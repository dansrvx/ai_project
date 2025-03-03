import random
import copy

# Define the shapes of different pieces in the game
piece_definitions = {
    'L': [[1, 0], [1, 0], [1, 1]],  # 'L' piece, normal orientation
    'L_90': [[1, 1, 1], [1, 0, 0]],  # 'L' piece, 90 degrees rotated
    'L_180': [[1, 1], [0, 1], [0, 1]],  # 'L' piece, 180 degrees rotated
    'L_270': [[0, 0, 1], [1, 1, 1]],  # 'L' piece, 270 degrees rotated

    'I': [[1], [1], [1]],  # 'I' piece, normal orientation
    'I_90': [[1, 1, 1]],  # 'I' piece, 90 degrees rotated

    'T': [[1, 1, 1], [0, 1, 0]],  # 'T' piece, normal orientation
    'T_90': [[0, 1], [1, 1], [0, 1]],  # 'T' piece, 90 degrees rotated
    'T_180': [[0, 1, 0], [1, 1, 1]],  # 'T' piece, 180 degrees rotated
    'T_270': [[1, 0], [1, 1], [1, 0]],  # 'T' piece, 270 degrees rotated

    'Square': [[1, 1], [1, 1]],  # 'Square' piece, no rotation
    'Z': [[1, 1, 0], [0, 1, 1]],  # 'Z' piece, normal orientation
    'Z_90': [[0, 1], [1, 1], [1, 0]],  # 'Z' piece, 90 degrees rotated

    'S': [[0, 1, 1], [1, 1, 0]],  # 'S' piece, normal orientation
    'S_90': [[1, 0], [1, 1], [0, 1]],  # 'S' piece, 90 degrees rotated
}


# Class to generate and manage a sequence of pieces
class PieceSequence:
    def __init__(self, piece_definitions, sequence_length=10):
        """
        Initializes the PieceSequence object with piece definitions and the desired sequence length.

        :param piece_definitions: Dictionary containing the shapes of different pieces.
        :param sequence_length: Length of the sequence to generate. Default is 10.
        """
        self.piece_definitions = piece_definitions  # The available piece definitions
        self.sequence_length = sequence_length  # The length of the sequence to generate
        self.sequence = []  # The list to store the generated sequence
        self.generate_sequence()  # Generate the initial sequence

    def generate_sequence(self):
        """
        Generates a random sequence of pieces based on the piece definitions.
        The sequence is stored in self.sequence.
        """
        self.sequence = []  # Clear the sequence before generating a new one
        piece_types = list(self.piece_definitions.keys())  # List of available piece types

        # Generate the sequence by randomly choosing pieces
        for _ in range(self.sequence_length):
            chosen_piece = random.choice(piece_types)  # Randomly select a piece type
            piece_shape = copy.deepcopy(self.piece_definitions[chosen_piece])  # Deep copy to avoid mutation
            self.sequence.append((chosen_piece, piece_shape))  # Add the chosen piece to the sequence

    def get_next_piece(self):
        """
        Returns the next piece in the sequence and removes it from the list.
        If the sequence is empty, it regenerates the sequence first.

        :return: A tuple containing the piece type and its shape.
        """
        if not self.sequence:  # If the sequence is empty
            self.generate_sequence()  # Regenerate the sequence
        return self.sequence.pop(0)  # Pop and return the first piece in the sequence

    def peek_next_piece(self):
        """
        Returns the next piece in the sequence without removing it.
        If the sequence is empty, returns None.

        :return: A tuple containing the piece type and its shape, or None if the sequence is empty.
        """
        if self.sequence:
            return self.sequence[0]  # Return the first piece in the sequence without removing it
        return None  # Return None if the sequence is empty
