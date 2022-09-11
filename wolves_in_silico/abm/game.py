import random

from .group import Village
from wolves_in_silico.base.game import Result, Phase, Role
from wolves_in_silico.base.game import Game as GameBase


class Game(GameBase):
    name = 'abm'

    def __init__(self, nciv, nwolf):
        self.village = Village(nciv=nciv, nwolf=nwolf)
        GameBase.__init__(self, nciv=nciv, nwolf=nwolf)

    def choose_mayor(self, p_wolf=.5):
        for member in self.village.population:
            member.is_mayor = False
        weights = self.village.nwolves * [p_wolf] + self.village.nciv * [1 - p_wolf]
        mayor = random.choices(self.village.population, weights=weights, k=1)[0]
        mayor.is_mayor = True

    def play_night(self):
        target = self.village.wolves.get_night_kill(self.village.civilians.population)
        self.village.remove(target)
        self.finish_phase()


    def play_day(self):
        target = self.village.get_day_kill()
        self.village.remove(target)
        self.finish_phase()

