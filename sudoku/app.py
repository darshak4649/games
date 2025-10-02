from flask import Flask
from flask_socketio import SocketIO, emit
from sudoku import generate_board, solve, valid, print_board, find_empty

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

# Store boards in memory
boards = {}

@socketio.on('create_board')
def handle_create_board():
    board = generate_board()
    board_id = str(len(boards) + 1)
    boards[board_id] = board
    emit('board_created', {'board_id': board_id, 'board': print_board(board)})

@socketio.on('make_move')
def handle_make_move(data):
    board_id = data.get('board_id')
    row = data.get('row')
    col = data.get('col')
    num = data.get('num')

    board = boards.get(board_id)
    if not board:
        emit('error', {'error': 'Board not found'})
        return

    if board[row][col] != 0:
        emit('error', {'error': 'Cell already filled'})
        return

    if not valid(board, num, (row, col)):
        emit('error', {'error': 'Invalid move'})
        return

    board[row][col] = num
    message = None
    if not find_empty(board):
        message = "Congratulations! Board solved!"

    emit('board_updated', {'board': print_board(board), 'message': message})

@socketio.on('solve_board')
def handle_solve_board(data):
    board_id = data.get('board_id')
    board = boards.get(board_id)
    if not board:
        emit('error', {'error': 'Board not found'})
        return

    solved = solve(board)
    message = "Solved!" if solved else "No solution exists"
    emit('board_updated', {'board': print_board(board), 'message': message})

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5001, debug=True)

