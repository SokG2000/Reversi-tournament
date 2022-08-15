import argparse
import reversi
from tkinter import *
from tkinter.messagebox import showinfo
from subprocess import Popen, PIPE, TimeoutExpired
from simulate_game import move_repr
import numpy as np
import time
from game_field import GameField
board_sz = 8
cell_size = 40
log_file = open("log3.txt", "w")
WAIT_TIME = 0.2
TIME_LIMIT = 5


def get_turn(line):
    representation = line[7:9]
    return 8 - int(representation[1]), ord(representation[0]) - ord('a')

def make_turn(players, position):
    sub_proc = Popen(players[position.turn], stdin=PIPE, stdout=PIPE, stderr=PIPE, encoding='utf-8')
    try:
        res = sub_proc.communicate(repr(position).strip() + "\n", timeout=TIME_LIMIT)[0]
        if len(res) != 4 or res[1] != ' ' or res[3] != '\n' or not (ord('0') <= ord(res[0]) <= ord('7')) or not (ord('0') <= ord(res[0]) <= ord('7')):
            position.error_end(1 - position.turn)
            position.turn = -1
        else:
            print(res)
            x, y = map(int, res.split())
            log_file.write(move_repr(x, y, position.turn))
            if position.can_move(x, y, position.turn):
                position.move(x, y)
            else:
                position.error_end(1 - position.turn)
                position.turn = -1
    except TimeoutExpired:
        position.tl_end(1 - position.turn)


def get_command(prog):
    if prog == "I":
        return None
    if len(prog) > 3 and prog[-3:] == ".py":
        return [PYTHON_EXEC, prog]
    return prog

def make_computer_turns(position, canvas, players):
    while position.status == reversi.PLAYING and players[position.turn] is not None:
        make_turn(players, position)
        canvas.draw_position(position.field)




def main(white, black):
    root = Tk()
    canvas = GameField(root, board_sz, cell_size)
    canvas.pack(expand=YES, fill=BOTH, side=TOP)
    players = [None] * 2    
    players[reversi.WHITE] = get_command(white)
    players[reversi.BLACK] = get_command(black)
    position = reversi.Position()
    def make_man_turn(event):
        nonlocal position
        coor = canvas.find_click_cell(event)
        # print(event.x, event.y, position.turn)
        # print(coor)
        if coor != (-1, -1):
            x = coor[0]
            y = coor[1]
            if position.can_move(x, y, position.turn):
                position.move(x, y)
                canvas.draw_position(position.field)
                canvas.update_idletasks()
                time.sleep(WAIT_TIME)
                make_computer_turns(position, canvas, players)
    canvas.bind("<Button-1>", make_man_turn)
    canvas.draw_position(position.field)
    make_computer_turns(position, canvas, players)
    root.mainloop()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--white', default="reversi_stupid.exe",
                        help='white player')
    parser.add_argument('--black', default="I",
                        help='white player')
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    main(args.white, args.black)
