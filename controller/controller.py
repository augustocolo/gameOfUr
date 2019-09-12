from model.board import UrBoard
import numpy as np
import constant


class Match:
    def __init__(self, agent_white, agent_black):
        self.agent_white = agent_white
        self.agent_white.player = 1
        self.agent_black = agent_black
        self.agent_black.player = -1
        self.turn = 0
        self.board = UrBoard()
        self.playing = constant.WHITE
        self.moves = []
        self.winner = None

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
        if self.board.white_score == constant.PIECES:
            self.winner = constant.WHITE
        elif self.board.black_score == constant.PIECES:
            self.winner = constant.BLACK


class Tournament:
    def __init__(self, agent_list, num_repetition):
        self.agents = agent_list
        self.num_reps = num_repetition
        self.total_games = len(agent_list) * (len(agent_list) - 1) * num_repetition
        self.single_games = (len(agent_list) - 1) * 2 * num_repetition
        self.results = [[[None for k in range(self.num_reps)] for j in range(len(self.agents))] for i in
                        range(len(self.agents))]
        self.wins = np.zeros(len(self.agents), dtype=int)
        self.leaderboard = None

    def play(self):
        print('Number of games:', self.total_games)
        print('Games per agent:', self.single_games)
        for i in range(len(self.agents)):
            for j in range(len(self.agents)):
                if i != j:
                    for k in range(self.num_reps):
                        m = Match(self.agents[i], self.agents[j])
                        m.play()
                        if m.winner == constant.WHITE:
                            self.results[i][j][k] = {'winner': 1, 'score': (m.board.white_score, m.board.black_score)}
                            self.wins[i] += 1
                        else:
                            self.results[i][j][k] = {'winner': -1, 'score': (m.board.white_score, m.board.black_score)}
                            self.wins[j] += 1
        res = list(zip(self.agents, self.wins))
        self.leaderboard = sorted(res, key=lambda team: team[1])
        self.leaderboard.reverse()

    def jsonify_leaderboard(self):
        res = []
        for elem in self.leaderboard:
            serial = [elem[0].dictionary(), int(elem[1])]
            res.append(serial)
        return res
