BOARD_SZ = 8
WHITE = 0
BLACK = 1
EMPTY = -1

dxs = [-1, 0, 1, 1, 1, 0, -1, -1]
dys = [1, 1, 1, 0, -1, -1, -1, 0]


def count_reverses(board, x, y, player):
    res = 0
    for dx, dy in zip(dxs, dys):
        next_x = x + dx
        next_y = y + dy
        dir_reversed = 0
        while 0 <= next_x <= 7 and 0 <= next_y <= 7 and board[next_x][next_y] == 1 - player:
            dir_reversed += 1
            next_x += dx
            next_y += dy
        if 0 <= next_x <= 7 and 0 <= next_y <= 7 and board[next_x][next_y] == player:
            res += dir_reversed
    return res

def can_move(board, x, y, player):
    if x < 0 or x >= BOARD_SZ or y < 0 or y >= BOARD_SZ:
        return False
    if board[x][y] != EMPTY:
        return False
    return count_reverses(board, x, y, player) > 0

def stupid_choise(board, player):
    return (0, 0)

def main():
    player = int(input())
    board = [None] * BOARD_SZ
    for i in range(BOARD_SZ):
        board[i] = list(map(int, input().split()))


main()