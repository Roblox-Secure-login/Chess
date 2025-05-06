let board = null;
let game = new Chess();

function onDragStart(source, piece, position, orientation) {
    if (game.game_over()) return false;
    if ((game.turn() === 'w' && piece.search(/^b/) !== -1) ||
        (game.turn() === 'b' && piece.search(/^w/) !== -1)) {
        return false;
    }
}

function onDrop(source, target) {
    let move = game.move({
        from: source,
        to: target,
        promotion: 'q'
    });

    if (move === null) return 'snapback';

    // Get AI move
    $.post('/move', { fen: game.fen() }, function(data) {
        game.move(data.move);
        board.position(game.fen());
        visualizeNN(data.move); // Visualize neural network evaluation
    });
}

function onSnapEnd() {
    board.position(game.fen());
}

function resetBoard() {
    game = new Chess();
    board.position(game.fen());
}

function initBoard() {
    let config = {
        draggable: true,
        position: 'start',
        onDragStart: onDragStart,
        onDrop: onDrop,
        onSnapEnd: onSnapEnd
    };
    board = Chessboard('chessboard', config);
}

$(document).ready(function() {
    initBoard();
});