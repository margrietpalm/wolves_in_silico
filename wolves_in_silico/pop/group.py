import random

import wolves_in_silico.base.group as group_base


class Group(group_base.Group):
    def __init__(self, size: int, has_major: bool = False):
        self.size = size
        self.has_major = has_major

    def remove(self):
        if self.size <= 0:
            return
        self.size -= 1

    def __repr__(self) -> str:
        return f"population with {self.size} members"


class Village(group_base.Village):
    def __init__(self, nciv, nwolf):
        self.wolves = Group(size=nwolf)
        self.civilians = Group(size=nciv)

    @property
    def nwolves(self):
        return self.wolves.size

    @property
    def nciv(self):
        return self.civilians.size

    def remove(self, wolf=False):
        pop = self.wolves if wolf else self.civilians
        if pop.has_major:
            pop.has_major = random.random() < (1 / pop.size)
        pop.remove()

    def __repr__(self):
        return f'wolves: {self.nwolves}\ncivilians: {self.nciv}'


