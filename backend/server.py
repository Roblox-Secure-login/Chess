from flask import Flask, request, jsonify
from chess_ai import get_ai_move
from train import generate_self_play_games
import chess

app = Flask(__name__)

@app.route('/move', methods=['POST'])
def make_move():
    data = request.json
    fen = data['fen']
    move = get_ai_move(fen)
    return jsonify({'move': move})

@app.route('/self_play_stats', methods=['GET'])
def self_play_stats():
    games = generate_self_play_games(num_games=10)  # Simulate stats
    white_wins, black_wins, draws, total_moves = 0, 0, 0, 0
    for game, result in games:
        total_moves += len(game)
        if result == 1:
            white_wins += 1
        elif result == -1:
            black_wins += 1
        else:
            draws += 1
    total_games = len(games)
    avg_moves = total_moves / total_games if total_games > 0 else 0
    return jsonify({
        'white_wins': white_wins,
        'black_wins': black_wins,
        'draws': draws,
        'avg_moves': avg_moves,
        'total_games': total_games
    })

if __name__ == '__main__':
    app.run(debug=True)