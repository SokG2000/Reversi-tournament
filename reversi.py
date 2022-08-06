import numpy as np
WHITE = 0
BLACK = 1
EMPTY = -1

PLAYING = "playing"
NORMAL_END = "norm"
ERROR_END = "error"
TL_END = "tl"

class Position:
    def __init__(self):
        self.field = np.ones((8, 8), dtype=int) * EMPTY
        self.field[3][4] = BLACK
        self.field[4][3] = BLACK
        self.field[3][3] = WHITE
        self.field[4][4] = WHITE
        self.turn = BLACK
        self.dx = [-1, 0, 1, 1, 1, 0, -1, -1]
        self.dy = [1, 1, 1, 0, -1, -1, -1, 0]
        self.num_dirs = 8
        self.status = PLAYING
        self.results = None
        self.winner = None
    
    def __repr__(self):
        res = str(self.turn) + "\n" + "\n".join((" ".join(map(str, line)) for line in self.field)) + "\n"
        return res
    
    def __str__(self):
        return "\n".join((" ".join(map(str, line)) for line in self.field)) + "\n"
    
    def count_reverses(self, x, y, player):
        res = 0
        for dx, dy in zip(self.dx, self.dy):
            next_x = x + dx
            next_y = y + dy
            dir_reversed = 0
            while 0 <= next_x <= 7 and 0 <= next_y <= 7 and self.field[next_x][next_y] == 1 - player:
                dir_reversed += 1
                next_x += dx
                next_y += dy
            if 0 <= next_x <= 7 and 0 <= next_y <= 7 and self.field[next_x][next_y] == player:
                res += dir_reversed
        return res
    
    def can_move(self, x, y, player):
        if x < 0 or x > 7 or y < 0 or y > 7:
            return False
        if self.field[x][y] != EMPTY:
            return False
        return self.count_reverses(x, y, player) > 0
    
    def move(self, x, y):
        self.field[x][y] = self.turn
        for dx, dy in zip(self.dx, self.dy):
            next_x = x + dx
            next_y = y + dy
            dir_reversed = 0
            while 0 <= next_x <= 7 and 0 <= next_y <= 7 and self.field[next_x][next_y] == 1 - self.turn:
                dir_reversed += 1
                next_x += dx
                next_y += dy
            if 0 <= next_x <= 7 and 0 <= next_y <= 7 and self.field[next_x][next_y] == self.turn:
                for i in range(1, dir_reversed + 1):
                    self.field[x + i * dx][y + i * dy] = self.turn
        self.turn = self.next_player(self.turn)
    
    def next_player(self, player):
        opponent = 1 - player
        for x in range(8):
            for y in range(8):
                if self.can_move(x, y, opponent):
                    return opponent
        for x in range(8):
            for y in range(8):
                if self.can_move(x, y, player):
                    return player
        self.status = NORMAL_END
        self.results = self.get_score()
        if self.results[WHITE] > self.results[BLACK]:
            self.winner = WHITE
        elif self.results[WHITE] < self.results[BLACK]:
            self.winner = BLACK
        else:
            self.winner = -1
        if self.winner != -1 and self.results[1 - self.winner] == 0:
            self.results[self.winner] = 64
        return -1
    
    def tl_end(self, winner):
        self.status = TL_END
        self.winner = winner
        self.results = [0, 0]
        self.results[winner] = 64
    
    def error_end(self, winner):
        self.status = ERROR_END
        self.winner = winner
        self.results = [0, 0]
        self.results[winner] = 64
    
    def get_score(self):
        res = [0, 0]
        for x in range(8):
            for y in range(8):
                if self.field[x][y] == WHITE:
                    res[WHITE] += 1
                if self.field[x][y] == BLACK:
                    res[BLACK] += 1
        return res
        


if __name__ == "__main__":
    pos = Position()
    print(pos.field)
    print(pos)
    