const board = document.getElementById('board');
const status = document.getElementById('status');
const socket = new WebSocket('wss://https://tic-tac-toe-online-ur4u.onrender.com');

let player = null;

for (let i = 0; i < 9; i++) {
  const cell = document.createElement('div');
  cell.classList.add('cell');
  cell.dataset.index = i;
  cell.addEventListener('click', () => {
    socket.send(JSON.stringify({ type: 'move', index: i }));
  });
  board.appendChild(cell);
}

socket.onmessage = (msg) => {
  const data = JSON.parse(msg.data);

  if (data.type === 'init') {
    player = data.player;
    status.textContent = `You are Player ${player}`;
  }

  if (data.type === 'update') {
    board.childNodes.forEach((cell, idx) => {
      cell.textContent = data.board[idx] || '';
      cell.classList.toggle('taken', !!data.board[idx]);
    });
    status.textContent = data.message;
  }
};
