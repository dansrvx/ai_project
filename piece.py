import random
import copy

piece_definitions = {
    'L': [
        [1, 0],
        [1, 0],
        [1, 1]
    ],
    'I': [
        [1],
        [1],
        [1]
    ],
    'T': [
        [1, 1, 1],
        [0, 1, 0]
    ],
    'Square': [
        [1, 1],
        [1, 1]
    ],
    'Z': [
        [1, 1, 0],
        [0, 1, 1]
    ],
    'S': [
        [0, 1, 1],
        [1, 1, 0]
    ],
    'J': [  # Mirror of L
        [0, 1],
        [0, 1],
        [1, 1]
    ],
    'L_reverse': [  # L rotated - included for variety
        [1, 1, 1],
        [1, 0, 0]
    ],
    'T_reverse': [ # T rotated - included for variety
        [1, 0],
        [1, 1],
        [1, 0]
    ]
    # Add more piece types here as needed
}

class PieceSequence:
    def __init__(self, piece_definitions, sequence_length=10):
        self.piece_definitions = piece_definitions
        self.sequence_length = sequence_length
        self.sequence = []
        self.generate_sequence()

    def generate_sequence(self):
        self.sequence = []
        piece_types = list(self.piece_definitions.keys())
        for _ in range(self.sequence_length):
            chosen_piece = random.choice(piece_types)
            piece_shape = copy.deepcopy(self.piece_definitions[chosen_piece])
            self.sequence.append((chosen_piece, piece_shape))

    def get_next_piece(self):
        if not self.sequence:
            self.generate_sequence()
        return self.sequence.pop(0)

    def peek_next_piece(self):
        if self.sequence:
            return self.sequence[0]
        return None