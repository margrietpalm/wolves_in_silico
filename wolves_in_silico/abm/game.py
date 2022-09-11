import random

from .group import Village
from ..base.game import Result, Phase, Role


class Game:

    def __init__(self, nciv, nwolf):
        self.village = Village(nciv=nciv, nwolf=nwolf)
        self.finished = False
        self.winner = None
        # day 0 = elections
        self.choose_major()
        self.phase = Phase.NIGHT
        self.nciv = [nciv]
        self.nwolves = [nwolf]

    def play(self) -> Result:
        while not self.finished:
            if self.phase == Phase.NIGHT:
                self.play_night()
            else:
                self.play_day()
            self.nciv.append(self.village.civilians.size)
            self.nwolves.append(self.village.wolves.size)
        return Result(nciv=self.nciv, nwolves=self.nwolves, civ_win=self.winner == Role.CIV)

    def choose_major(self, p_wolf=.5):
        for member in self.village.population:
            member.is_major = False
        weights = self.village.nwolves * [p_wolf] + self.village.nciv * [1 - p_wolf]
        major = random.choices(self.village.population, weights=weights, k=1)[0]
        major.is_major = True

    def play_night(self):
        target = self.village.wolves.get_night_kill(self.village.civilians.population)
        self.village.remove(target)
        if not self.village.has_major:
            self.choose_major()
        if self.village.wolves.vote_size > self.village.civilians.vote_size:
            self.finished = True
            self.winner = Role.WOLF
        self.phase = Phase.DAY

    def play_day(self):
        target = self.village.get_day_kill()
        self.village.remove(target)
        if not self.village.has_major:
            self.choose_major()
        if self.village.wolves.size == 0:
            self.finished = True
            self.winner = Role.CIV
        if self.village.wolves.vote_size > self.village.civilians.vote_size:
            self.finished = True
            self.winner = Role.WOLF
        self.phase = Phase.NIGHT
