import actor.agents as ag
from controller.controller import Match
import constant
import random
import numpy as np
from time import time
from copy import deepcopy


def match_between_two_random_agents():
    w = 0
    b = 0
    for i in range(1000):
        agent1 = ag.RandomAgent(constant.WHITE)
        agent2 = ag.RandomAgent(constant.BLACK)
        match = Match(agent1, agent2)
        match.play()
        w += 1 if match.moves[len(match.moves) - 1].split("/")[1] == "W" else 0
        b += 1 if match.moves[len(match.moves) - 1].split("/")[1] == "B" else 0
        print(match.moves)
        print(len(match.moves))
        print(w, b)


def tournament_between_ordered_agents():
    rangey = list(range(constant.BOXES))
    list_orders = []
    w = 0
    b = 0
    t = np.zeros(2)
    for i in range(200):
        list_orders.append(random.sample(rangey, len(rangey)))
    for y in range(2):
        print(y)
        t[y] = time()
        if y != 0:
            print(t[y] - t[y - 1])
        point_difference = np.zeros(len(list_orders), dtype=int)
        wins = np.zeros(len(list_orders), dtype=int)

        for i in range(len(list_orders)):
            for j in range(len(list_orders)):
                if i != j:
                    for x in range(2):
                        agent1 = ag.OrderedAgent(constant.WHITE, list_orders[i])
                        agent2 = ag.OrderedAgent(constant.BLACK, list_orders[j])

                        match = Match(agent1, agent2)
                        match.play()
                        w += 1 if match.moves[len(match.moves) - 1].split("/")[1] == "W" else 0
                        b += 1 if match.moves[len(match.moves) - 1].split("/")[1] == "B" else 0
                        if match.moves[len(match.moves) - 1].split("/")[1] == "W":
                            wins[i] += 1
                            diff = match.board.white_score - match.board.black_score
                            point_difference[i] += diff
                            point_difference[j] -= diff
                        else:
                            wins[j] += 1
                            diff = match.board.white_score - match.board.black_score
                            point_difference[i] += diff
                            point_difference[j] -= diff
        max_wins = max(wins)
        min_wins = min(wins)
        winners = []
        diff_winners = []
        diff_losers = []
        losers = []
        for idx, val in enumerate(wins):
            if val == max_wins:
                winners.append(list_orders[idx])
                diff_winners.append(point_difference[idx])
            if val == min_wins:
                losers.append(list_orders[idx])
                diff_losers.append(point_difference[idx])
        print('max wins', max_wins)
        print(tuple(zip(winners, diff_winners)))
        print('least wins', min_wins)
        print(tuple(zip(losers, diff_losers)))
    print("white winners:", w, 'black winners:', b)


def match_between_two_ordered_agents():
    order_a = [8, 13, 4, 11, 15, 14, 10, 12, 0, 2, 1, 6, 9, 7, 5, 3]
    order_b = [8, 11, 2, 9, 13, 12, 6, 10, 15, 0, 14, 4, 7, 5, 3, 1]

    reps = 10000

    agent1 = ag.OrderedAgent(constant.WHITE, order_a)
    agent2 = ag.OrderedAgent(constant.BLACK, order_b)
    agent3 = ag.OrderedAgent(constant.BLACK, order_a)
    agent4 = ag.OrderedAgent(constant.WHITE, order_b)
    wins_1 = 0
    wins_2 = 0
    t0 = time()
    for i in range(reps):
        print(i)
        match = Match(agent1, agent2)
        match.play()
        wins_1 += 1 if match.moves[len(match.moves) - 1].split("/")[1] == "W" else 0
        wins_2 += 1 if match.moves[len(match.moves) - 1].split("/")[1] == "B" else 0

    for i in range(reps):
        print(reps + i)
        match = Match(agent4, agent3)
        match.play()
        wins_2 += 1 if match.moves[len(match.moves) - 1].split("/")[1] == "W" else 0
        wins_1 += 1 if match.moves[len(match.moves) - 1].split("/")[1] == "B" else 0
    t1 = time()
    print('agent1 wins:', wins_1, 'agent2 wins:', wins_2, 'time:', t1 - t0)


def simple_genetic_algorithm_for_ordered_agents():
    starting_order = [8, 4, 13, 2, 10, 14, 0, 15, 11, 12, 1, 7, 9, 3, 6, 5]
    best_order = starting_order
    num_of_children = 100
    generations = 15
    threshold = 0.55
    num_of_matches = 60
    num_of_matches_tournament = 10

    timer = [time()]
    for i in range(generations):
        timer.append(time())
        print(timer[i + 1] - timer[i])
        print('generation', i)
        print('best', best_order)
        pool = [best_order]
        for j in range(num_of_children):
            # mutate the best
            new = deepcopy(best_order)
            for k in range(np.random.randint(1, 3)):
                x = np.random.randint(0, constant.BOXES)
                y = np.random.randint(0, constant.BOXES)
                new[x], new[y] = new[y], new[x]
            pool.append(new)

        better_players = []
        for j in range(num_of_children):
            agent1 = ag.OrderedAgent(constant.WHITE, best_order)
            agent2 = ag.OrderedAgent(constant.BLACK, pool[j + 1])
            agent3 = ag.OrderedAgent(constant.BLACK, best_order)
            agent4 = ag.OrderedAgent(constant.WHITE, pool[j + 1])
            wins_new = 0
            for k in range(num_of_matches):
                match = Match(agent1, agent2)
                match.play()
                wins_new += 1 if match.moves[len(match.moves) - 1].split("/")[1] == "B" else 0

            for k in range(num_of_matches):
                match = Match(agent4, agent3)
                match.play()
                wins_new += 1 if match.moves[len(match.moves) - 1].split("/")[1] == "W" else 0

            if wins_new > threshold * num_of_matches * 2:
                better_players.append(pool[j + 1])

        if len(better_players) == 1:
            best_order = better_players[0]
        elif len(better_players) > 1:
            print('entering knockout phase with {} players'.format(len(better_players)))
            wins = np.zeros(len(better_players))
            point_difference = np.zeros(len(better_players))
            # then play a tournament
            for idx1 in range(len(better_players)):
                for idx2 in range(len(better_players)):
                    if idx1 != idx2:
                        for j in range(num_of_matches_tournament):
                            agent1 = ag.OrderedAgent(constant.WHITE, better_players[idx1])
                            agent2 = ag.OrderedAgent(constant.BLACK, better_players[idx2])
                            match = Match(agent1, agent2)
                            match.play()
                            if match.moves[len(match.moves) - 1].split("/")[1] == "W":
                                wins[idx1] += 1
                                diff = match.board.white_score - match.board.black_score
                                point_difference[idx1] += diff
                                point_difference[idx2] -= diff
                            else:
                                wins[idx2] += 1
                                diff = match.board.white_score - match.board.black_score
                                point_difference[idx2] += diff
                                point_difference[idx1] -= diff
            max_wins = max(wins)
            winners = []
            diff_winners = []
            for idx, val in enumerate(wins):
                if val == max_wins:
                    winners.append(better_players[idx])
                    diff_winners.append(point_difference[idx])
            max_difference = max(diff_winners)
            for idx, val in enumerate(diff_winners):
                if val == max_difference:
                    best_order = winners[idx]

    print('winner', best_order)


if __name__ == "__main__":
    match_between_two_ordered_agents()
