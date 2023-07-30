import copy
import random

from collections import Counter
from typing import Optional, List

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
        return any(member.is_mayor for member in self.population)

    @property
    def mayor(self) -> Optional[Player]:
        if not self.has_mayor:
            return None
        mayors = [p for p in self.population if p.is_mayor]
        if len(mayors) == 1:
            return mayors[0]
        else:
            raise Exception(f"{len(mayors)} in the group")

    def remove(self, target: Player):
        self.population.remove(target)

    def __contains__(self, item: Player) -> bool:
        return item in self.population

    def __repr__(self) -> str:
        return f"population: {', '.join(str(member) for member in self.population)}"

    def __eq__(self, other):
        if not isinstance(other, Group):
            return False
        return (self.population == other.population and
                self.mayor_extra_vote == other.mayor_extra_vote)


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

    def choose_mayor(self) -> Player:
        while True:
            votes = [p.vote(self, allow_self=True) for p in self.population]
            max_votes = self._count_votes(votes)
            if len(max_votes) == 1:
                return max_votes[0]

    def get_day_kill(self) -> Player:
        # collect votes and count
        max_votes = self._count_votes([p.vote(self) for p in self.population])
        # if there is a majority, that choice counts
        if len(max_votes) == 1:
            return max_votes[0]
        # if there is no majority, mayor chooses
        # for now, this is the mayor's original choice
        else:
            return self.mayor.votes[-1]

    def _count_votes(self, votes: List[Player]) -> List[Player]:
        counts = Counter(votes)
        if self.has_mayor:
            counts[self.mayor.votes[-1]] += self.mayor_extra_vote
        return [p for p, c in counts.items() if c == max(counts.values())]

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
