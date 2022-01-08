from typing import List


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


# p1 = Player("1", 4)
# p2 = Player("2", 8)
p1 = Player("1", 10)
p2 = Player("2", 6)
g1 = Game1([p1, p2])
print(g1.result())
