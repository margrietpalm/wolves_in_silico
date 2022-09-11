from abc import ABC, abstractmethod


class Group(ABC):
    size: int = 0
    has_major: bool = False

    @property
    def vote_size(self) -> float:
        return self.size + .5 * self.has_major

    @abstractmethod
    def remove(self):
        pass


class Village(Group):
    wolves: Group
    civilians: Group

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
    def has_major(self) -> bool:
        return self.wolves.has_major or self.civilians.has_major