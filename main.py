import actor.agents as ag
from controller.controller import Match
import constant

if __name__ == "__main__":
    W = 0
    B = 0
    for i in range(1000):
        agent1 = ag.RandomAgent(constant.WHITE)
        agent2 = ag.RandomAgent(constant.BLACK)
        match = Match(agent1, agent2)
        match.play()
        W += 1 if match.moves[len(match.moves) - 1].split("/")[1] == "W" else 0
        B += 1 if match.moves[len(match.moves) - 1].split("/")[1] == "B" else 0
        print(match.moves)
        print(len(match.moves))
        print(W, B)
