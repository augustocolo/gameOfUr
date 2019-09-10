import random


class Agent():
    def __init__(self, player):
        self.player = player


class RandomAgent(Agent):
    def play(self, board, dice_roll):
        valid_moves = board.show_valid_moves(self.player, dice_roll)
        if len(valid_moves) > 0:
            choice = random.choice(valid_moves)
            return choice
        else:
            return -1
