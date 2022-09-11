import random

from wolves_in_silico.pop.group import Village
from wolves_in_silico.base.game import Phase, Result, Role
from wolves_in_silico.base.game import Game as GameBase


class Game(GameBase):
    name = 'pop'
    
    def __init__(self, nciv, nwolf):
        self.village = Village(nciv=nciv, nwolf=nwolf)
        GameBase.__init__(self, nciv=nciv, nwolf=nwolf)

    def choose_mayor(self):
        self.village.wolves.has_mayor = False
        self.village.civilians.has_mayor = False
        if random.random() < (self.village.nwolves / self.village.size):
            self.village.wolves.has_mayor = True
        else:
            self.village.civilians.has_mayor = True

    def play_night(self):
        self.village.remove(wolf=False)
        self.finish_phase()

    def play_day(self):
        wolf_kill = random.random() < (self.village.nwolves / self.village.size)
        self.village.remove(wolf=wolf_kill)
        self.finish_phase()
