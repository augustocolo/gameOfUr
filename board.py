import numpy as np
import constant
import random


class UrBoard:
    def __init__(self):

        self.white_score = 0
        self.black_score = 0

        self.white_start = constant.PIECES - 1
        self.black_start = constant.PIECES - 1

        self.board = np.array([[1, -1],
                               [0, 0], [0, 0], [0, 0], [0, 0],
                               0, 0, 0, 0, 0, 0, 0, 0,
                               [0, 0], [0, 0],
                               (0, 0)])

    def check_valid_move(self, player, start_box, end_box):
        # check if indices are ok
        if start_box not in range(constant.BOXES - 1):
            return False
        if end_box not in range(1, constant.BOXES):
            return False

        list_order = 0 if player == constant.WHITE else 1
        # START BOX CHECKS
        # case: start box is list
        if type(self.board[start_box]) is list:
            # check if piece is in start box
            if self.board[start_box][list_order] == 0:
                return False

        # case: start box is int
        elif type(self.board[start_box]) is int:
            if self.board[start_box] != player:
                return False

        # start box can only be int or list
        else:
            return False

        # END BOX CHECKS
        # case: end box is list (first four and last two boxes)
        if type(self.board[end_box]) is list:
            # check if end box is empty
            if self.board[end_box][list_order] is not player:
                # everything ok: return true
                return True
            else:
                # there's already another piece in arrival box
                return False

        # case: end box is tuple (end of race)
        elif type(self.board[end_box]) is tuple:
            # everything ok: return true
            return True
        # case: end box is int
        elif type(self.board[end_box]) is int:
            if self.board[end_box] != player:
                # if it's free -> ok! Return true
                if self.board[end_box] == 0:
                    return True
                # if not check if it's a rosetta
                else:
                    if end_box in constant.ROSETTA:
                        return False
                    else:
                        return True
            else:
                return False

    def move(self, player, start_box, dice_roll):
        # if dice_roll is zero return true
        if dice_roll == 0:
            return True
        end_box = start_box + dice_roll

        if self.check_valid_move(player, start_box, end_box):
            # Case: end box is tuple (piece gets to the end)
            if type(self.board[end_box]) is tuple:
                # remove this piece from board
                self.remove_piece(player, start_box)
                # add score
                self.add_score(player)

            # Case: end box is int
            elif type(self.board[end_box]) is int:
                if self.board[end_box] != 0:
                    # add piece to start (eat opponent's piece)
                    self.eat_piece(player)
                self.remove_piece(player, start_box)
                self.add_piece(player, end_box)

            # Case: end box is list
            elif type(self.board[end_box]) is list:
                self.remove_piece(player, start_box)
                self.add_piece(player, end_box)

            # Restore first box if it was used
            if start_box == 0:
                self.restore_first_box(player)

            return True

        else:
            return False

    def remove_piece(self, player, start_box):
        list_order = 0 if player == constant.WHITE else 1
        if type(self.board[start_box]) is list:
            self.board[start_box][list_order] = 0
        else:
            self.board[start_box] = 0

    def add_piece(self, player, end_box):
        list_order = 0 if player == constant.WHITE else 1
        if type(self.board[end_box]) is list:
            self.board[end_box][list_order] = player
        else:
            self.board[end_box] = player

    def eat_piece(self, player):
        if player == constant.WHITE:
            self.black_start += 1
        else:
            self.white_start += 1

    def add_score(self, player):
        if player == constant.WHITE:
            self.white_score += 1
        else:
            self.black_score += 1

    def restore_first_box(self, player):
        self.add_piece(player, 0)
        if player == constant.WHITE:
            self.white_start -= 1
        else:
            self.black_start -= 1

    def show_valid_moves(self, player, dice_roll):
        valid_moves = []
        for start_box in range(constant.BOXES - 1):
            if self.check_valid_move(player, start_box, start_box + dice_roll):
                valid_moves.append(start_box)
        return valid_moves

    def game_ended(self):
        if self.white_score == constant.PIECES or self.black_score == constant.PIECES:
            return True
        else:
            return False

    def state(self):
        small_list = []
        result = [[self.white_score, self.black_score], [self.white_start + 1, self.black_start + 1]]

        # add to the result the two START sections
        for list_order in range(2):
            small_list = []
            for i in range(1, 1 + constant.START_BOXES):
                if self.board[i][list_order] == 0:
                    small_list.append('X')
                else:
                    if list_order == 0:
                        small_list.append('W')
                    else:
                        small_list.append('B')
            result.append(small_list)

        # add to the result the MIDDLE section
        small_list = []
        for i in range(1 + constant.START_BOXES, 1 + constant.START_BOXES + constant.MIDDLE_BOXES):
            if self.board[i] == constant.WHITE:
                small_list.append('W')
            elif self.board[i] == constant.BLACK:
                small_list.append('B')
            else:
                small_list.append('X')
        result.append(small_list)

        # add to the result the END section
        for list_order in range(2):
            small_list = []
            for i in range(1 + constant.START_BOXES + constant.MIDDLE_BOXES, constant.BOXES - 1):
                if self.board[i][list_order] == 0:
                    small_list.append('X')
                else:
                    if list_order == 0:
                        small_list.append('W')
                    else:
                        small_list.append('B')
            result.append(small_list)

        # result = [[score White, scoreBlack], [remainingWHITE, remainingBlack], [whiteSTARTsection], [blackSTARTsection], [MIDDLEsection], [whiteENDsection], [blackENDsection]]
        return result

    def print_state(self):
        state = self.state()
        print('Score')
        print('WHITE {} - {} BLACK'.format(state[0][0], state[0][1]))
        print('Table')
        print('{} remaining: {} \t {}'.format(state[2], state[1][0], state[5]))
        print(state[4])
        print('{} remaining: {} \t {}'.format(state[3], state[1][1], state[6]))

    def roll_dice(self):
        result = 0
        for dice in range(constant.NUM_DICES):
            result += random.choice(constant.DICE)
        return result
