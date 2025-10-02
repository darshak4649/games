import random

def print_board(board):
    return [[cell for cell in row] for row in board]

def find_empty(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return (i, j)
    return None

def valid(board, num, pos):
    for j in range(9):
        if board[pos[0]][j] == num and pos[1] != j:
            return False
    for i in range(9):
        if board[i][pos[1]] == num and pos[0] != i:
            return False
    box_x = pos[1] // 3
    box_y = pos[0] // 3
    for i in range(box_y*3, box_y*3 + 3):
        for j in range(box_x*3, box_x*3 + 3):
            if board[i][j] == num and (i,j) != pos:
                return False
    return True

def solve(board):
    find = find_empty(board)
    if not find:
        return True
    row, col = find
    for i in range(1, 10):
        if valid(board, i, (row, col)):
            board[row][col] = i
            if solve(board):
                return True
            board[row][col] = 0
    return False

def generate_board():
    board = [[0 for _ in range(9)] for _ in range(9)]
    for i in range(0,9,3):
        fill_box(board, i, i)
    # solve(board)
    #
    # remove_numbers(board, 40)
    return board

def fill_box(board, row, col):
    nums = list(range(1,10))
    random.shuffle(nums)
    for i in range(3):
        for j in range(3):
            board[row+i][col+j] = nums.pop()

def remove_numbers(board, count):
    while count > 0:
        i = random.randint(0,8)
        j = random.randint(0,8)
        if board[i][j] != 0:
            board[i][j] = 0
            count -= 1

print(generate_board())