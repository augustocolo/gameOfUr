from model.board import UrBoard
import constant


class Match:
    def __init__(self, agent_white, agent_black):
        self.agent_white = agent_white
        self.agent_black = agent_black
        self.turn = 0
        self.board = UrBoard()
        self.playing = constant.WHITE
        self.moves = []

    def play(self):
        while not self.board.game_ended():
            if self.playing == constant.WHITE:
                dice_roll = self.board.roll_dice()
                move = self.agent_white.play(self.board, dice_roll)
                if move != -1:
                    board_response = self.board.move(constant.WHITE, move, dice_roll)
                    if not board_response['replay']:
                        self.playing = constant.BLACK
                    if board_response['done']:
                        str = '{}/W/{}'.format(move, move + dice_roll)
                        self.moves.append(str)

            elif self.playing == constant.BLACK:
                dice_roll = self.board.roll_dice()
                move = self.agent_black.play(self.board, dice_roll)
                if move != -1:
                    board_response = self.board.move(constant.BLACK, move, dice_roll)
                    if not board_response['replay']:
                        self.playing = constant.WHITE
                    if board_response['done']:
                        str = '{}/B/{}'.format(move, move + dice_roll)
                        self.moves.append(str)
            self.turn += 1
