import random
import constant


class Agent():
    def __init__(self, player=None):
        self.player = player


class RandomAgent(Agent):
    def play(self, board, dice_roll):
        valid_moves = board.show_valid_moves(self.player, dice_roll)
        if len(valid_moves) > 0:
            choice = random.choice(valid_moves)
            return choice
        else:
            return -1

    def mutate(self, num_children):
        children = []
        for _ in range(num_children):
            children.append(RandomAgent())
        return children

    def dictionary(self):
        dictey = {
            'type': 'RandomAgent'
        }
        return dictey


class OrderedAgent(Agent):
    def __init__(self, order, player=None):
        super(OrderedAgent, self).__init__(player)
        self.order = order

    def play(self, board, dice_roll):
        valid_moves = board.show_valid_moves(self.player, dice_roll)
        end_boxes = []
        if len(valid_moves) > 0:
            for i in valid_moves:
                end_boxes.append(i + dice_roll)
        else:
            return -1
        for target in self.order:
            if target in end_boxes:
                return target - dice_roll

    def mutate(self, num_children):
        children = []
        for _ in range(num_children):
            child_order = self.order.copy()
            for i in range(random.randint(1, 3)):
                x = random.randint(0, len(child_order) - 1)
                y = random.randint(0, len(child_order) - 1)
                child_order[x], child_order[y] = child_order[y], child_order[x]
            children.append(OrderedAgent(child_order))
        return children

    def dictionary(self):
        dictey = {
            'type': 'OrderedAgent',
            'order': self.order
        }
        return dictey

    def __repr__(self):
        return 'OrderedAgent{}'.format(self.order)


class PolicyAgent(Agent):
    def __init__(self, characteristics, player=None):
        super(PolicyAgent, self).__init__(player)
        self.eat_traits = characteristics['eat']
        self.move_traits = characteristics['move']
        self.end_traits = characteristics['end']

    def play(self, board, dice_roll):
        valid_moves = board.show_valid_moves(self.player, dice_roll)
        end_boxes = []
        if len(valid_moves) > 0:
            for i in valid_moves:
                end_boxes.append(i + dice_roll)
        else:
            return -1
        boxes_value = []
        for i in end_boxes:
            description = board.describe_box(self.player, i)
            if description == 'move':
                value = self.move_traits[0] + (len(self.move_traits[1]) - self.move_traits[1].index(i)) * \
                        self.move_traits[2]
                boxes_value.append(value)
            elif description == 'eat':
                value = self.eat_traits[0] + (len(self.eat_traits[1]) - self.eat_traits[1].index(i)) * \
                        self.move_traits[2]
                boxes_value.append(value)
            else:
                value = self.end_traits[0] + (len(self.move_traits[1]) - self.move_traits[1].index(i)) * \
                        self.move_traits[2]
                boxes_value.append(value)
        res = sorted(list(zip(valid_moves, boxes_value)), key=lambda move: move[1], reverse=True)
        return res[0][0]

    def __repr__(self):
        return 'PolicyAgent E{} M{} En{}'.format(self.eat_traits, self.move_traits, self.end_traits)

    def dictionary(self):
        dictey = {
            'type': 'PolicyAgent',
            'eat_traits': self.eat_traits,
            'move_traits': self.eat_traits,
            'end_traits': self.end_traits
        }
        return dictey

    def mutate(self, num_children):
        children = []
        for _ in range(num_children):
            child_traits = [self.eat_traits.copy(), self.move_traits.copy(), self.end_traits.copy()]
            # for j => number of random mutations
            for j in range(random.randint(0, 2)):
                # for k => which trait is mutating
                for k in range(random.randint(0, 3)):
                    # for l => which subtrait is mutating
                    for ll in range(random.randint(0, 3)):
                        plus_or_minus = random.choice([1, -1])
                        if ll == 0:
                            child_traits[k][ll] += plus_or_minus
                        if ll == 1:
                            rand_x = random.randint(0, len(child_traits[k][ll]) - 1)
                            rand_y = random.randint(0, len(child_traits[k][ll]) - 1)
                            child_traits[k][ll][rand_x], child_traits[k][ll][rand_y] = child_traits[k][ll][rand_y], \
                                                                                       child_traits[k][ll][rand_x]
                        else:
                            child_traits[k][ll] += plus_or_minus * 0.1
            # create new child agent
            characteristics = {'eat': child_traits[0], 'move': child_traits[1], 'end': child_traits[2]}
            child = PolicyAgent(characteristics)
            children.append(child)

        return children
