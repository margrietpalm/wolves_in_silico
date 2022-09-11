from wolves_in_silico.base.game import Role


class Player:

    def __init__(self, role, id):
        self.role = role
        self.id = id
        self.is_mayor = False

    @property
    def is_wolf(self):
        return self.role == Role.WOLF

    def __repr__(self):
        bm_suffix = '*' if self.is_mayor else ''
        return f'{self.role.name.lower()}_{self.id:02d}{bm_suffix}'
