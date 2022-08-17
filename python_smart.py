from copy import deepcopy
n = 8
MAX_DEEP = 3

costs = [[1] * 8 for i in range(8)]
#costs[0][0] = 20
#costs[0][7] = 20
#costs[7][0] = 20
#costs[7][7] = 20
#for i in range(2, 6):
#    costs[0][i] = 3
#    costs[i][0] = 3
#    costs[7][i] = 3
#    costs[i][7] = 3


def can_move(field, x, y, color):
    if field[x][y] != -1:
        return False
    dxs = [-1, -1, -1, 0, 1, 1, 1, 0]
    dys = [-1, 0, 1, 1, 1, 0, -1, -1]
    for dx, dy in zip(dxs, dys):
        new_x = x + dx
        new_y = y + dy
        if not (0 <= new_x <= 7 and 0 <= new_y <= 7 and field[new_x][new_y] == 1 - color):
            continue
        while 0 <= new_x <= 7 and 0 <= new_y <= 7 and field[new_x][new_y] == 1 - color:
            new_x += dx
            new_y += dy
        if 0 <= new_x <= 7 and 0 <= new_y <= 7 and field[new_x][new_y] == color:
            return True
    return False


def move(field, x, y, color):
    new_field = deepcopy(field)
    dxs = [-1, -1, -1, 0, 1, 1, 1, 0]
    dys = [-1, 0, 1, 1, 1, 0, -1, -1]
    for dx, dy in zip(dxs, dys):
        new_x = x + dx
        new_y = y + dy
        while 0 <= new_x <= 7 and 0 <= new_y <= 7 and field[new_x][new_y] == 1 - color:
            new_x += dx
            new_y += dy
        if 0 <= new_x <= 7 and 0 <= new_y <= 7 and field[new_x][new_y] == color:
            new_x -= dx
            new_y -= dy
            while x != new_x or y != new_y:
                new_field[new_x][new_y] = color
                new_x -= dx
                new_y -= dy
    new_field[x][y] = color
    return new_field


def estimate(field, color, deep):
    if deep == 0:
        diff = 0
        for i in range(n):
            for j in range(n):
                if field[i][j] == color:
                    diff += costs[i][j]
                elif field[i][j] == color:
                    diff -= costs[i][j]
        return diff
    else:
        best = None
        for i in range(n):
            for j in range(n):
                if can_move(field, i, j, 1 - color):
                    new_field = move(field, i, j, 1 - color)
                    score = estimate(new_field, 1 - color, deep - 1)
                    if best is None or best < score:
                        best = score
        if best is None:
            return -estimate(field, 1 - color, deep - 1)
        return -best


color = int(input())
cells = [None] * n
for i in range(n):
    cells[i] = list(map(int, input().split()))
best_score = None
best_x = -1
best_y = -1
for x in range(n):
    for y in range(n):
        if can_move(cells, x, y, color):
            new_cells = move(cells, x, y, color)
            score = estimate(new_cells, color, MAX_DEEP)
            if best_score is None or best_score < score:
                best_score = score
                best_x = x
                best_y = y
print(best_x, best_y)
