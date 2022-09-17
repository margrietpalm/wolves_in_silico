import random

import wolves_in_silico.base.group as group_base


class Group(group_base.Group):
    def __init__(self, size: int, has_mayor: bool = False):
        self._size = size
        self._has_mayor = has_mayor

    @property
    def has_mayor(self) -> bool:
        return self._has_mayor

    @has_mayor.setter
    def has_mayor(self, has_mayor: bool):
        self._has_mayor = has_mayor

    @property
    def size(self) -> int:
        return self._size

    @size.setter
    def size(self, size: int):
        self._size = size

    def remove(self):
        if self.size <= 0:
            return
        self.size -= 1

    def __repr__(self) -> str:
        return f"population with {self.size} members"


class Village(group_base.Village):
    def __init__(self, nciv: int, nwolf: int):
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
        if pop.has_mayor:
            pop.has_mayor = random.random() < (1 / pop.size)
        pop.remove()

    def __repr__(self) -> str:
        return f'population of {self.size} with {self.nwolves} wolfes and {self.nciv} civilians'


