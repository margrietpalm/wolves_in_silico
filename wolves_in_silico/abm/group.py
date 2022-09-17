import copy
import random
from wolves_in_silico.abm.player import Player
from wolves_in_silico.base.game import Role
import wolves_in_silico.base.group as group_base

class Group(group_base.Group):
    def __init__(self, population: list[Player]):
        self.population: list[Player] = copy.copy(population)

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



class Village(group_base.Village, Group):
    def __init__(self, nciv: int, nwolf: int):
        self.wolves: Wolves = Wolves(nwolf)
        self.civilians: Civilians = Civilians(nciv)
        Group.__init__(self, self.wolves.population + self.civilians.population)

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
