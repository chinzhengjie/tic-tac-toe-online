from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

clients = []
board = [None] * 9
turn = "X"

def check_winner():
    wins = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
    for a, b, c in wins:
        if board[a] and board[a] == board[b] == board[c]:
            return board[a]
    if all(board):
        return "Draw"
    return None

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    player = "X" if len(clients) == 0 else "O"
    clients.append(ws)
    await ws.send_json({"type": "init", "player": player})

    try:
        while True:
            data = await ws.receive_json()
            if data["type"] == "move":
                idx = data["index"]
                global turn
                if board[idx] is None and player == turn:
                    board[idx] = player
                    turn = "O" if turn == "X" else "X"
                    winner = check_winner()
                    message = f"{winner} wins!" if winner and winner != "Draw" else "It's a draw!" if winner == "Draw" else f"{turn}'s turn"
                    for client in clients:
                        await client.send_json({
                            "type": "update",
                            "board": board,
                            "message": message
                        })
    except WebSocketDisconnect:
        clients.remove(ws)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
