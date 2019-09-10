from model.board import UrBoard
import constant
from os import system, name
import random


def random_play():
    bb = UrBoard()
    player = 1
    first_roll = True
    turn = 0
    while not bb.game_ended():
        # show game table state
        print("\n")
        print("Turn:", turn)
        print(bb.board)
        print("white" if player == 1 else "black")
        bb.print_state()
        if first_roll:
            dice_roll = bb.roll_dice()
            first_roll = False
        print("Dice Roll:", dice_roll)
        available_moves = bb.show_valid_moves(player, dice_roll)
        if len(available_moves) == 0:
            player = player * -1
            available_moves.append(0)
            first_roll = True
        print("available moves:", available_moves)
        start_box = random.choice(available_moves)
        print("Move:", start_box)
        print(type(start_box))
        if type(start_box) is not int:
            exit()
        if bb.move(player, start_box, dice_roll):
            if start_box + dice_roll not in constant.ROSETTA:
                player = player * -1
            clear_screen()
            turn += 1
            first_roll = True
        else:
            print("MOVE NOT VALID!")
    print('game Ended on turn', turn)
    return turn, 1 if bb.white_score == constant.PIECES else 2


def clear_screen():
    # for windows
    if name == 'nt':
        _ = system('cls')

        # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


def human_play():
    bb = UrBoard()
    player = 1
    first_roll = True
    while not bb.game_ended():
        # show game table state
        bb.print_state()
        if player == constant.WHITE:
            print("WHITE PLAYER HAS TO MOVE")
        else:
            print("BLACK PLAYER HAS TO MOVE")
        if first_roll:
            dice_roll = bb.roll_dice()
            first_roll = False
        print("DICE ROLL: {}".format(dice_roll))
        available_moves = bb.show_valid_moves(player, dice_roll)
        print("VALID MOVES: {}".format(available_moves))
        start_box = input('INPUT MOVE: ')
        start_box = int(start_box)
        if bb.move(player, start_box, dice_roll):
            if start_box + dice_roll not in constant.ROSETTA:
                player = player * -1
            clear_screen()
            first_roll = True
        else:
            print("MOVE NOT VALID!")


if __name__ == "__main__":
    num_iter = 50
    white = 0
    black = 0
    res = []
    sum_turns = 0
    for i in range(num_iter):
        res.append(random_play())
        sum_turns += res[i][0] / num_iter
        if res[i][1] == 1:
            white += 1
        else:
            black += 1
    print("Mean number of turns:", sum_turns)
    print("Win white:", white)
    print("Win black:", black)
