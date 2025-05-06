import chess
import numpy as np
from collections import defaultdict
import tensorflow as tf
from tensorflow.keras import layers, models

class NeuralNetwork:
    def __init__(self):
        self.model = self.build_model()
    
    def build_model(self):
        model = models.Sequential([
            layers.Dense(128, activation='relu', input_shape=(64,)),  # 8x8 board
            layers.Dense(64, activation='relu'),
            layers.Dense(2, activation='softmax')  # [value, policy]
        ])
        model.compile(optimizer='adam', loss='mse')
        return model
    
    def evaluate(self, board):
        # Convert board to 8x8 array (1 for white, -1 for black, 0 for empty)
        state = np.zeros((8, 8))
        for square, piece in board.piece_map().items():
            row, col = divmod(square, 8)
            state[row, col] = 1 if piece.color == chess.WHITE else -1
        state = state.flatten()
        pred = self.model.predict(np.array([state]), verbose=0)
        return pred[0][0], pred[0][1]  # value, policy score

class MCTS:
    def __init__(self, nn, simulations=100):
        self.nn = nn
        self.simulations = simulations
        self.Q = defaultdict(float)  # Total value of action
        self.N = defaultdict(int)    # Visit count
        self.P = defaultdict(float)  # Prior probability
    
    def search(self, board):
        for _ in range(self.simulations):
            self.simulate(board.copy(), [])
        # Select move with highest visit count
        legal_moves = list(board.legal_moves)
        best_move = max(legal_moves, key=lambda m: self.N[(board.fen(), str(m))])
        return best_move
    
    def simulate(self, board, path):
        if board.is_game_over():
            result = board.result()
            return 1 if result == '1-0' else -1 if result == '0-1' else 0
        
        fen = board.fen()
        legal_moves = list(board.legal_moves)
        if not legal_moves:
            return 0
        
        # Neural network evaluation
        value, policy = self.nn.evaluate(board)
        for move in legal_moves:
            move_str = str(move)
            self.P[(fen, move_str)] = policy / len(legal_moves)  # Simplified
        
        # Select move using UCB
        ucb_scores = []
        for move in legal_moves:
            move_str = str(move)
            q = self.Q[(fen, move_str)] / (self.N[(fen, move_str)] + 1)
            u = 1.4 * self.P[(fen, move_str)] * np.sqrt(self.N.get(fen, 0) + 1) / (1 + self.N[(fen, move_str)])
            ucb_scores.append(q + u)
        
        move = legal_moves[np.argmax(ucb_scores)]
        board.push(move)
        value = -self.simulate(board, path + [move])
        move_str = str(move)
        self.Q[(fen, move_str)] += value
        self.N[(fen, move_str)] += 1
        self.N[fen] = self.N.get(fen, 0) + 1
        return value

def get_ai_move(fen):
    board = chess.Board(fen)
    nn = NeuralNetwork()
    mcts = MCTS(nn)
    move = mcts.search(board)
    return str(move)