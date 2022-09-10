from enum import Enum


class Role(Enum):
    WOLF = 1
    CIV = 2


class Player:

    def __init__(self, role, id):
        self.role = role
        self.id = id
        self.is_major = False

    @property
    def is_wolf(self):
        return self.role == Role.WOLF

    def __repr__(self):
        bm_suffix = '*' if self.is_major else ''
        return f'{self.role.name.lower()}_{self.id:02d}{bm_suffix}'
