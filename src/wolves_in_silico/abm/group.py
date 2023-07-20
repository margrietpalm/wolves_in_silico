import copy
import random
from wolves_in_silico.abm.player import Player, Role


class Group:
    mayor_extra_vote: float = .5

    def __init__(self, population: list[Player]):
        self.population: list[Player] = copy.copy(population)

    @property
    def vote_size(self) -> float:
        return self.size + self.mayor_extra_vote * self.has_mayor

    @property
    def size(self) -> int:
        return len(self.population)

    @property
    def has_mayor(self) -> bool:
        return any([member.is_mayor for member in self.population])

    def remove(self, target: Player):
        self.population.remove(target)

    def __repr__(self) -> str:
        return f"population: {', '.join(str(member) for member in self.population)}"



class Village(Group):
    wolves: Group
    civilians: Group

    def __init__(self, nciv: int, nwolf: int):
        self.wolves: Wolves = Wolves(nwolf)
        self.civilians: Civilians = Civilians(nciv)
        Group.__init__(self, self.wolves.population + self.civilians.population)

    @property
    def nwolves(self) -> int:
        return self.wolves.size

    @property
    def nciv(self) -> int:
        return self.civilians.size

    @property
    def size(self):
        return self.nwolves + self.nciv

    @property
    def has_mayor(self) -> bool:
        return self.wolves.has_mayor or self.civilians.has_mayor

    def change_mayor_vote(self, mayor_extra_vote: float):
        self.mayor_extra_vote = mayor_extra_vote
        self.civilians.mayor_extra_vote = mayor_extra_vote
        self.wolves.mayor_extra_vote = mayor_extra_vote

    def remove(self, member: Player):
        if member.is_wolf:
            self.wolves.remove(member)
        else:
            self.civilians.remove(member)
        self.population.remove(member)

    def get_day_kill(self) -> Player:
        return random.choice(self.population)

    def __repr__(self) -> str:
        return f'wolves: {str(self.wolves)}\ncivilians: {str(self.civilians)}'


class Civilians(Group):

    def __init__(self, n: int):
        Group.__init__(self, [Player(Role.CIV, i + 1) for i in range(n)])


class Wolves(Group):

    def __init__(self, n: int, p_kill: float = 1.):
        Group.__init__(self, [Player(Role.WOLF, i + 1) for i in range(n)])
        self.p_kill = p_kill

    def turn(self) -> bool:
        return random.random() > self.p_kill

    def get_night_kill(self, civilians: Group) -> Player:
        return random.choice(civilians.population)
