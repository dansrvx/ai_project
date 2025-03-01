import tkinter as tk
from tkinter import messagebox
import game_controller as game_controller

class GameGUI:
    def __init__(self, root, game_controller):
        self.root = root
        self.root.title("Block Placement Game")
        self.game = game_controller

        # Get window width and height after widgets are created but before mainloop starts
        root.update() # Force window to update and get its size
        window_width = root.winfo_width()
        window_height = root.winfo_height()

        # Calculate cell size to fit board in window, with some padding
        board_padding_fraction = 0.1 # 10% padding on each side (total 20% padding)
        available_board_width = window_width * (1 - board_padding_fraction)
        available_board_height = window_height * (0.6 - board_padding_fraction) # Reduce height for other UI elements
        # Reduce height further to account for other UI elements above and below the board.
        # 0.6 is an approximate fraction, adjust as needed.

        cell_size_width = available_board_width / self.game.game_board.cols
        cell_size_height = available_board_height / self.game.game_board.rows
        self.cell_size = int(min(cell_size_width, cell_size_height)) # Choose smaller to fit in both dimensions and make integer

        if self.cell_size < 5: # Minimum cell size to be somewhat visible
            self.cell_size = 5

        self.board_frame = tk.Frame(root)
        self.board_frame.pack(pady=20)
        self.cells = {} # Store GUI cell elements
        self.row_labels = {} # Store row number labels
        self.col_labels = {} # Store column number labels


        self.next_piece_frame = tk.Frame(root)
        self.next_piece_frame.pack(pady=10)
        self.next_piece_labels = []

        self.score_label = tk.Label(root, text="Score: 0", font=("Arial", 16) )
        self.score_label.pack(pady=10)
        
        self.remain_pieces_label = tk.Label(root, text="Remaining Pieces: " + str(len(self.game.piece_sequence.sequence)) , font=("Arial", 12) )
        self.remain_pieces_label.pack(pady=10)

        self.status_label = tk.Label(root, text="", font=("Arial", 12))
        self.status_label.pack(pady=5)

        self.input_frame = tk.Frame(root)
        self.input_frame.pack(pady=10)
        tk.Label(self.input_frame, text="Row:", font=("Arial", 12)).pack(side=tk.LEFT)
        self.row_entry = tk.Entry(self.input_frame, width=5, font=("Arial", 12))
        self.row_entry.pack(side=tk.LEFT)
        tk.Label(self.input_frame, text="Col:", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
        self.col_entry = tk.Entry(self.input_frame, width=5, font=("Arial", 12))
        self.col_entry.pack(side=tk.LEFT)

        self.manual_button = tk.Button(root, text="Jogar Manualmente", command=self.manual_play_gui, font=("Arial", 14))
        self.manual_button.pack(pady=10)

        self.astar_button = tk.Button(root, text="Jogar com A*", command=self.astar_play_gui, font=("Arial", 14))
        self.astar_button.pack(pady=10)

        self.update_board_display()
        self.update_next_piece_display()
        self.update_score_display()


    def update_board_display(self):
        """Updates the visual representation of the game board, including row and column numbers."""

        # Column numbers (above the board)
        for c in range(self.game.game_board.cols):
            if c not in self.col_labels:
                col_label = tk.Label(self.board_frame, text=str(c), font=("Arial", max(self.cell_size // 4, 6)))
                col_label.grid(row=0, column=c + 1, padx=1, pady=1) # row=0 for column numbers, offset columns by 1
                self.col_labels[c] = col_label # Store column labels
            self.col_labels[c].config(text=str(c)) # In case board size is dynamic, update if needed


        # Row numbers (to the left of the board) and board cells
        for r in range(self.game.game_board.rows):
            # Row number label
            if r not in self.row_labels:
                row_label = tk.Label(self.board_frame, text=str(r), font=("Arial", max(self.cell_size // 4, 6)))
                row_label.grid(row=r + 1, column=0, padx=1, pady=1) # column=0 for row numbers, offset rows by 1
                self.row_labels[r] = row_label # Store row labels
            self.row_labels[r].config(text=str(r)) # Update if needed

            for c in range(self.game.game_board.cols):
                if (r, c) not in self.cells:
                    cell_label = tk.Label(self.board_frame, width=2, height=1, relief=tk.SOLID, borderwidth=1, font=("Arial", max(self.cell_size // 4, 6))) # Ensure minimum font size
                    cell_label.grid(row=r + 1, column=c + 1, padx=1, pady=1) # Offset both row and column by 1
                    self.cells[(r, c)] = cell_label # Store label in cells dictionary
                cell = self.game.game_board.board[r][c]
                if cell == 1:
                    self.cells[(r, c)].config(bg="blue") # Filled cell color
                else:
                    self.cells[(r, c)].config(bg="white") # Empty cell color


    def update_next_piece_display(self):
        """Updates the display of the next piece."""
        for label in self.next_piece_labels:
            label.destroy()
        self.next_piece_labels = []

        next_piece_info = self.game.piece_sequence.peek_next_piece()
        if next_piece_info:
            next_piece_name, next_piece_shape = next_piece_info

            name_label = tk.Label(self.next_piece_frame, text=f"Next Piece: {next_piece_name}", font=("Arial", 12))
            name_label.pack()
            self.next_piece_labels.append(name_label)

            piece_grid_frame = tk.Frame(self.next_piece_frame)
            piece_grid_frame.pack()
            self.next_piece_labels.append(piece_grid_frame)

            for r in range(len(next_piece_shape)):
                for c in range(len(next_piece_shape[0])):
                    cell_val = next_piece_shape[r][c]
                    color = "blue" if cell_val == 1 else "white"
                    piece_cell_label = tk.Label(piece_grid_frame, width=2, height=1, relief=tk.SOLID, borderwidth=1, bg=color)
                    piece_cell_label.grid(row=r, column=c, padx=1, pady=1)
                    self.next_piece_labels.append(piece_cell_label)
        else:
            no_piece_label = tk.Label(self.next_piece_frame, text="No more pieces", font=("Arial", 12))
            no_piece_label.pack()
            self.next_piece_labels.append(no_piece_label)
            game_over_status = self.game.is_game_over()
            if game_over_status == "victory":
                messagebox.showinfo("Game Over", "Congratulations! You placed all pieces. Victory!\nScore: " + str(self.game.score))
                #self.place_button.config(state=tk.DISABLED) # Disable further play
            elif game_over_status == "defeat":
                messagebox.showinfo("Game Over", "Game Over. No more valid moves. Defeat!\nScore: " + str(self.game.score))
                #self.place_button.config(state=tk.DISABLED) # Disable further play


    def update_score_display(self):
        """Updates the score label in the GUI."""
        self.score_label.config(text=f"Score: {self.game.score}")

    def update_remaining_pieces_display(self):
        """Updates the remaining pieces in the GUI."""
        self.remain_pieces_label.config(text=f"Remaining Pieces: {len(self.game.piece_sequence.sequence)}")        

    def manual_play_gui(self):
        try:
            row = int(self.row_entry.get())
            col = int(self.col_entry.get())
        except ValueError:
            self.status_label.config(text="Entrada inválida: Linha e Coluna devem ser inteiros.")
            return

        if self.game.manual_play(row, col):
            self.update_board_display()
            self.update_next_piece_display()
            self.update_score_display()
            self.update_remaining_pieces_display()
            self.status_label.config(text="Peça colocada com sucesso.")
            self.row_entry.delete(0, tk.END)
            self.col_entry.delete(0, tk.END)
            game_over_status = self.game.is_game_over()
            if game_over_status == "victory":
                messagebox.showinfo("Game Over", "Parabéns! Você colocou todas as peças. Vitória!\nPontuação: " + str(self.game.score))
                self.manual_button.config(state=tk.DISABLED)
                self.astar_button.config(state=tk.DISABLED)
            elif game_over_status == "defeat":
                messagebox.showinfo("Game Over", "Fim de jogo. Não há mais movimentos válidos. Derrota!\nPontuação: " + str(self.game.score))
                self.manual_button.config(state=tk.DISABLED)
                self.astar_button.config(state=tk.DISABLED)
        else:
            self.status_label.config(text="Não foi possível colocar a peça na localização especificada. Tente novamente.")

    def astar_play_gui(self):
        if self.game.play_game():
            self.update_board_display()
            self.update_next_piece_display()
            self.update_score_display()
            self.update_remaining_pieces_display()
            game_over_status = self.game.is_game_over()
            if game_over_status == "victory":
                messagebox.showinfo("Game Over", "Parabéns! Você colocou todas as peças. Vitória!\nPontuação: " + str(self.game.score))
                self.manual_button.config(state=tk.DISABLED)
                self.astar_button.config(state=tk.DISABLED)
            elif game_over_status == "defeat":
                messagebox.showinfo("Game Over", "Fim de jogo. Não há mais movimentos válidos. Derrota!\nPontuação: " + str(self.game.score))
                self.manual_button.config(state=tk.DISABLED)
                self.astar_button.config(state=tk.DISABLED)
        else:
            messagebox.showinfo("Game Over", "Não foi possível encontrar uma solução.")
            self.manual_button.config(state=tk.DISABLED)
            self.astar_button.config(state=tk.DISABLED)