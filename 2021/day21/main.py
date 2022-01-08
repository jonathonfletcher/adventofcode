from typing import List
import functools


class Player:

    def __init__(self, name, startpos):
        self.name = name
        self.startpos = startpos - 1
        self.score = 0

    def __repr__(self):
        return f'{self.name}({self.startpos},{self.score})'

    def move(self, roll):
        self.startpos = (self.startpos + roll) % 10
        self.score += self.startpos + 1


class Game1:

    class Die:

        def __init__(self):
            self.value = 0
            self.count = 0

        def roll(self):
            self.value = (self.value + 1) % 100
            self.count += 1
            return self.value

    def __init__(self, players: List[Player], winscore: int = 1000):
        self.loser = None
        self.winscore = winscore
        self.d = Game1.Die()
        while self.loser is None:
            for i in [0, 1]:
                if self.turn(players[i], self.d):
                    self.loser = players[1-i]
                    return

    def turn(self, p: Player, d: Die) -> bool:
        p.move(d.roll() + d.roll() + d.roll())
        return p.score >= self.winscore

    def result(self) -> int:
        return self.d.count * self.loser.score


class Game2:

    def __init__(self, players: List[Player], winscore: int = 21):
        self.players = players
        self.winscore = winscore

    @staticmethod
    @functools.cache
    def run_game(p0p, p0s, p1p, p1s, winscore):
        w0, w1 = 0, 0
        for roll in [(x, y, z) for x in [1, 2, 3] for y in [1, 2, 3] for z in [1, 2, 3]]:
            tp0p = (p0p + sum(roll)) % 10
            tp0s = (p0s+tp0p+1)
            if tp0s < 21:
                nw1, nw0 = Game2.run_game(p1p, p1s, tp0p, tp0s, winscore)
                w0, w1 = w0+nw0, w1+nw1
            else:
                w0 += 1
        return w0, w1

    def result(self):
        return max(Game2.run_game(self.players[0].startpos, 0, self.players[1].startpos, 0, self.winscore))


# players = [Player("1", 4), Player("2", 8)]
players = [Player("1", 10), Player("2", 6)]
g1 = Game1(players)
print(g1.result())

players = [Player("1", 10), Player("2", 6)]
g2 = Game2(players)
print(g2.result())
