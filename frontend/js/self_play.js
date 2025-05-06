function startSelfPlay() {
    let game = new Chess();
    let board = Chessboard('chessboard', { position: 'start' });

    function playMove() {
        if (game.game_over()) {
            updateMetrics();
            game = new Chess();
            board.position('start');
        }
        $.post('/move', { fen: game.fen() }, function(data) {
            game.move(data.move);
            board.position(game.fen());
            setTimeout(playMove, 1000);
        });
    }

    function updateMetrics() {
        $.get('/self_play_stats', function(data) {
            $('#white-wins').text(data.white_wins);
            $('#black-wins').text(data.black_wins);
            $('#draws').text(data.draws);
            $('#avg-moves').text(data.avg_moves.toFixed(2));
            $('#total-games').text(data.total_games);
        });
    }

    playMove();
    setInterval(updateMetrics, 5000);
}