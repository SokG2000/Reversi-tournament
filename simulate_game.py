from subprocess import Popen, PIPE, TimeoutExpired
from time import time
import argparse
import reversi
from sys import platform

side_names = [None] * 2
side_names[reversi.WHITE] = "White"
side_names[reversi.BLACK] = "Black"
TIME_LIMIT = 5
if "win" in platform.lower():
    PYTHON_EXEC = "python"
else:
    PYTHON_EXEC = "python3"

def move_repr(x, y, player):
    return f"{side_names[player]}: {chr(ord('a') + y)}{8-x}\n"
    

def make_turn(players, position, log_file):
    sub_proc = Popen(players[position.turn], stdin=PIPE, stdout=PIPE, stderr=PIPE, encoding='utf-8')
    try:
        res = sub_proc.communicate(repr(position).strip() + "\n", timeout=TIME_LIMIT)[0]
        if len(res) != 4 or res[1] != ' ' or res[3] != '\n' or not (ord('0') <= ord(res[0]) <= ord('7')) or not (ord('0') <= ord(res[0]) <= ord('7')):
            position.error_end(1 - position.turn)
            position.turn = -1
        else:
            #print(res)
            x, y = map(int, res.split())
            log_file.write(move_repr(x, y, position.turn))
            if position.can_move(x, y, position.turn):
                position.move(x, y)
            else:
                position.error_end(1 - position.turn)
                position.turn = -1
    except TimeoutExpired:
        position.tl_end(1 - position.turn)

def write_result(position, log_file):
    if position.status == reversi.PLAYING:
        print("Still running")
    elif position.status == reversi.NORMAL_END:
        log_file.write(f"{side_names[position.winner]} won.\n")
        log_file.write(f"Score {position.results[reversi.WHITE]}: {position.results[reversi.BLACK]}")
    elif position.status == reversi.TL_END:
        log_file.write(f"{side_names[position.winner]} won due to opponents time limit.\n")
        log_file.write(f"Score {position.results[reversi.WHITE]}: {position.results[reversi.BLACK]}")
    elif position.status == reversi.ERROR_END:
        log_file.write(f"{side_names[position.winner]} won due to opponents invalid move.\n")
        log_file.write(f"Score {position.results[reversi.WHITE]}: {position.results[reversi.BLACK]}")


def get_command(prog):
    if len(prog) > 3 and prog[-3:] == ".py":
        return [PYTHON_EXEC, prog]
    return prog

def play(black, white, log_path):
    players = [None] * 2
    players[reversi.WHITE] = get_command(white)
    players[reversi.BLACK] = get_command(black)
    with open(log_path, "w") as log_file:
        position = reversi.Position()
        while position.status == reversi.PLAYING:
            make_turn(players, position, log_file)
        log_file.write("Final situation:\n" + str(position))
        write_result(position, log_file)
    return (position.results[reversi.WHITE], position.results[reversi.BLACK])


def parse_args():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--white', default="reversi_easy.exe",
                        help='path to white player programm')
    parser.add_argument('--black', default="python_solution.py",
                        help='path to black player programm')
    parser.add_argument('--log', default="logs2.txt",
                        help='path to log file')
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    play(args.black, args.white, args.log)
