import argparse
import reversi
from tkinter import *
from tkinter.messagebox import showinfo
import numpy as np
from game_field import GameField
board_sz = 8
cell_size = 40

def get_turn(line):
    representation = line[7:9]
    return 8 - int(representation[1]), ord(representation[0]) - ord('a')


def main(log_path):
    with open(log_path, "r") as log_file:
        position = reversi.Position()
        fields = [np.copy(position.field)]
        for line in log_file.readlines():
            if line[:5] != "White" and line[:5] != "Black":
                break
            x, y = get_turn(line)
            position.move(x, y)
            fields.append(np.copy(position.field))
            print(x, y)
    print(fields[-1])
    print(fields[0])
    root = Tk()
    canvas = GameField(root, board_sz, cell_size)
    canvas.pack(expand=YES, fill=BOTH, side=TOP)
    position_id = 0
    def next_position():
        nonlocal position_id
        if position_id == len(fields) - 1:
            return
        position_id += 1
        canvas.draw_position(fields[position_id])
    def prev_position():
        nonlocal position_id
        if position_id == 0:
            return
        position_id -= 1
        canvas.draw_position(fields[position_id])
    next_button = Button(root, height=2, width=20, text='Next',
                          command=next_position)
    next_button.pack(expand=YES, fill=BOTH, side=RIGHT)
    prev_button = Button(root, height=2, width=20, text='Prev',
                          command=prev_position)    
    prev_button.pack(expand=YES, fill=BOTH, side=LEFT)
    arr = fields[0]
    canvas.draw_position(arr)
    root.mainloop()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--log', default="logs.txt",
                        help='path to log file')
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    main(args.log)
