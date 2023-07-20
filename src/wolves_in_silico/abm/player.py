from enum import Enum


class Role(Enum):
    WOLF = 1
    CIV = 2


class Player:

    def __init__(self, role: Role, id: int):
        self.role = role
        self.id = id
        self.is_mayor: bool = False

    @property
    def is_wolf(self) -> bool:
        return self.role == Role.WOLF

    def __repr__(self) -> str:
        bm_suffix = '*' if self.is_mayor else ''
        return f'{self.role.name.lower()}_{self.id:02d}{bm_suffix}'
