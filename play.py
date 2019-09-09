from board import UrBoard
import constant
from os import system, name


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
    human_play()
