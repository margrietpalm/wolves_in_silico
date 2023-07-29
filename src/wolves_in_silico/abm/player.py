from __future__ import annotations

from enum import Enum
import random

from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from wolves_in_silico.abm.group import Group


class Role(Enum):
    WOLF = 1
    CIV = 2


class Player:

    def __init__(self, role: Role, id: int):
        self.role = role
        self.id = id
        self.is_mayor: bool = False
        self.votes: List[Player] = []

    @property
    def is_wolf(self) -> bool:
        return self.role == Role.WOLF

    def vote(self, group: Group, allow_self: bool = False) -> Player:
        # create a list of options
        idx = list(range(group.size))
        if not allow_self and self in group.population:
            idx.remove(group.population.index(self))
        if len(idx) > 0:
            v = group.population[random.choice(idx)]
            self.votes.append(v)
            return v
        else:
            raise Exception("Cannot vote with an empty group")

    def __repr__(self) -> str:
        bm_suffix = '*' if self.is_mayor else ''
        return f'{self.role.name.lower()}_{self.id:02d}{bm_suffix}'

    def __eq__(self, other) -> bool:
        if not isinstance(other, Player):
            return False
        return (self.role == other.role and self.id == other.id and self.is_mayor == other.is_mayor)
