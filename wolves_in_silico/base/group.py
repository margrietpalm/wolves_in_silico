class Group:
    mayor_extra_vote: float = .5

    @property
    def size(self):
        return 0

    @property
    def has_mayor(self) -> bool:
        return False

    @property
    def vote_size(self) -> float:
        return self.size + self.mayor_extra_vote * self.has_mayor


class Village(Group):
    wolves: Group
    civilians: Group

    def change_mayor_vote(self, mayor_extra_vote: float):
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