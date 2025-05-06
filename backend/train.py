import chess
import numpy as np
from chess_ai import NeuralNetwork

def generate_self_play_games(num_games=100):
    nn = NeuralNetwork()
    games = []
    for _ in range(num_games):
        board = chess.Board()
        game = []
        while not board.is_game_over():
            state = np.zeros((8, 8))
            for square, piece in board.piece_map().items():
                row, col = divmod(square, 8)
                state[row, col] = 1 if piece.color == chess.WHITE else -1
            move = get_ai_move(board.fen())
            game.append((state.flatten(), move))
            board.push(chess.Move.from_uci(move))
        result = board.result()
        games.append((game, 1 if result == '1-0' else -1 if result == '0-1' else 0))
    return games

def train_model():
    nn = NeuralNetwork()
    games = generate_self_play_games()
    X, y_value = [], []
    for game, result in games:
        for state, _ in game:
            X.append(state)
            y_value.append(result)
    X = np.array(X)
    y_value = np.array(y_value)
    nn.model.fit(X, y_value, epochs=10, batch_size=32)
    nn.model.save('model/nn_model.h5')

if __name__ == '__main__':
    train_model()