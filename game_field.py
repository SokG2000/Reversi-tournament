from tkinter import *

class GameField(Canvas):
    epsilon = 5
    colors = ['white', 'black']

    def __init__(self, root, board_sz, cell_size):
        self.board_sz = board_sz
        self.cell_size = cell_size
        self.left_offset = 3 / 2 * cell_size
        self.right_offset = 1 / 2 * cell_size
        self.up_offset = 1 / 2 * cell_size
        self.button_offset = 1 / 2 * cell_size
        self.root = root
        left_offset = self.left_offset
        right_offset = self.right_offset
        up_offset = self.up_offset
        button_offset = self.button_offset
        width = cell_size * board_sz + left_offset + right_offset
        height = cell_size * board_sz + up_offset + button_offset
        super().__init__(root, width=width, height=height, bg='white')
        for i in range(board_sz + 1):
            self.create_line(i * cell_size + left_offset, up_offset,
                             i * cell_size + left_offset,
                             up_offset + cell_size * board_sz)
        for i in range(board_sz + 1):
            self.create_line(left_offset, i * cell_size + up_offset,
                             left_offset + cell_size * board_sz,
                             i * cell_size + up_offset)
        self.circles = [None] * board_sz
        for i in range(board_sz):
            self.circles[i] = [None] * board_sz

    def make_circle(self, x, y, player):
        if player != 0 and player != 1:
            if self.circles[x][y] is not None:
                self.delete(self.circles[x][y])
                self.circles[x][y] = None
        elif self.circles[x][y] is None:
            l = self.left_offset + x * self.cell_size + self.epsilon
            u = self.up_offset + y * self.cell_size + self.epsilon
            r = self.left_offset + (x + 1) * self.cell_size - self.epsilon
            d = self.up_offset + (y + 1) * self.cell_size - self.epsilon
            self.circles[x][y] = self.create_oval(l, u, r, d,
                                                  fill=self.colors[player])
        else:
            self.itemconfig(self.circles[x][y], fill=self.colors[player])

    def draw_position(self, field):
        for i in range(self.board_sz):
            for j in range(self.board_sz):
                self.make_circle(i, j, field[i][j])

    def find_coor(self, offset, x):
        x = int(x - offset)
        res = x // self.cell_size
        if res < 0 or res >= self.board_sz:
            return -1
        return res

    def find_click_cell(self, event):
        x = self.find_coor(self.left_offset, event.x)
        y = self.find_coor(self.right_offset, event.y)
        if x == -1 or y == -1:
            return (-1, -1)
        return (x, y)
