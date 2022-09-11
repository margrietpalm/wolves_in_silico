from abc import ABC, abstractmethod


class Group(ABC):
    size: int = 0
    has_mayor: bool = False
    mayor_extra_vote: float = .5

    @property
    def vote_size(self) -> float:
        return self.size + self.mayor_extra_vote * self.has_mayor

    @abstractmethod
    def remove(self):
        pass


class Village(Group):
    wolves: Group
    civilians: Group

    def change_mayor_vote(self, mayor_extra_vote):
        self.mayor_extra_vote = mayor_extra_vote
        self.civilians.mayor_extra_vote = mayor_extra_vote
        self.wolves.mayor_extra_vote = mayor_extra_vote

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