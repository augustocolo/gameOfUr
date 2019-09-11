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


class OrderedAgent(Agent):
    def __init__(self, player, order):
        super(OrderedAgent, self).__init__(player)
        self.order = order

    def play(self, board, dice_roll):
        valid_moves = board.show_valid_moves(self.player, dice_roll)
        end_boxes = []
        if len(valid_moves) > 0:
            for i in valid_moves:
                end_boxes.append(i + dice_roll)
        for target in self.order:
            if target in end_boxes:
                return target - dice_roll
        else:
            return -1
