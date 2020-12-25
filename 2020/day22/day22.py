import functools
import copy


def read_input(filename):
    inputs = dict()
    with open(filename) as ifp:
        current_player = None
        for line in [x.strip() for x in ifp.readlines()]:
            if line.find(':') >= 0:
                current_player = line.split(':')[0].strip()
                inputs[current_player] = list()
            elif len(line):
                inputs[current_player].append(int(line))
    return inputs


def score_hand(hand):
    return functools.reduce(lambda x, y: x + y[0]*y[1], zip(range(1, 1+len(hand)), hand), 0)


def to_tuple(i):
    if type(i) in [type([]), type(()), type({})]:
        return tuple([to_tuple(x) for x in i])
    else:
        return i


def play_combat(hands, debug=False, indent=0, recursive=False):
    game_round = 0
    seen_hands = set()
    total_card_count = sum([len(h) for h in hands])
    while True:
        game_round += 1

        if debug:
            print("{}-- {} --".format(indent*'\t', game_round))

        if recursive:
            t_hands = to_tuple(hands)
            if t_hands in seen_hands:
                return 0, hands
            seen_hands.add(t_hands)

        if debug:
            print("{}{}".format(indent*'\t', hands))

        cards = [x.pop() for x in hands]
        if debug:
            print("{}{}".format(indent*'\t', cards))

        hand_winner = None
        if recursive and all([len(x[0]) >= x[1] for x in zip(hands, cards)]):
            new_hands = [x[0][-x[1]:] for x in zip(hands, cards)]
            hand_winner, _ = play_combat(new_hands, debug, indent+1, recursive)
        else:
            hand_winner = cards.index(max(cards))

        if debug:
            print("{}winner: {} ({})".format(indent*'\t', hand_winner, cards[hand_winner]))

        max_card_winner = cards.index(max(cards))
        for c in sorted(cards, reverse=(hand_winner == max_card_winner)):
            hands[hand_winner].insert(0, c)

        if len(hands[hand_winner]) == total_card_count:
            return hand_winner, hands

inputs = read_input("input.txt")

players = inputs.keys()
starting_hands = [list(reversed(inputs[x])) for x in players]


winner_a, hands_a = play_combat(copy.deepcopy(starting_hands))
# print(hands_a)
# print(winner_a)
print("result_a: {}".format(score_hand(hands_a[winner_a])))

winner_b, hands_b = play_combat(copy.deepcopy(starting_hands), indent=0, recursive=True)
# print(hands_b)
# print(winner_b)
print("result_b: {}".format(score_hand(hands_b[winner_b])))

