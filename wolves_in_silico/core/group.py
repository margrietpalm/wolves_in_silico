import copy
import random

from .player import Player, Role


class Group:
    def __init__(self, population: list[Player]):
        self.population = copy.copy(population)

    @property
    def size(self) -> int:
        return len(self.population)

    @property
    def vote_size(self) -> float:
        return self.size + .5 * self.has_major

    @property
    def has_major(self) -> bool:
        return any([member.is_major for member in self.population])

    def remove(self, target: Player):
        self.population.remove(target)

    def __repr__(self) -> str:
        return f"population: {', '.join(str(member) for member in self.population)}"



class Village(Group):
    def __init__(self, nciv, nwolf):
        self.wolves = Wolves(nwolf)
        self.civilians = Civilians(nciv)
        Group.__init__(self, self.wolves.population + self.civilians.population)

    @property
    def nwolves(self):
        return self.wolves.size

    @property
    def nciv(self):
        return self.civilians.size

    def remove(self, member):
        if member.is_wolf:
            self.wolves.remove(member)
        else:
            self.civilians.remove(member)
        self.population.remove(member)

    def get_day_kill(self):
        return random.choice(self.population)

    def __repr__(self):
        return f'wolves: {str(self.wolves)}\ncivilians: {str(self.civilians)}'


class Civilians(Group):

    def __init__(self, n):
        Group.__init__(self, [Player(Role.CIV, i + 1) for i in range(n)])


class Wolves(Group):

    def __init__(self, n, p_kill=1):
        Group.__init__(self, [Player(Role.WOLF, i + 1) for i in range(n)])
        self.p_kill = p_kill

    def turn(self) -> bool:
        return random.random() > self.p_kill

    def get_night_kill(self, civilians) -> Player:
        return random.choice(civilians.population)
