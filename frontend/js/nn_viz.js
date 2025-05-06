function visualizeNN(move) {
    const canvas = document.getElementById('nn-viz-canvas');
    const ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Simulate neural network move evaluations
    const moves = [move, 'e4', 'd4', 'Nf3']; // Example moves
    const scores = [0.9, 0.7, 0.6, 0.5];   // Example scores
    
    ctx.font = '16px Arial';
    ctx.fillStyle = '#2ecc71';
    moves.forEach((m, i) => {
        ctx.fillText(`${m}: ${scores[i].toFixed(2)}`, 10, 20 + i * 30);
        ctx.fillRect(100, 10 + i * 30, scores[i] * 200, 20);
    });
}