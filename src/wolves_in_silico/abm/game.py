from typing import Optional
import random
import numpy as np
from enum import Enum

from wolves_in_silico.abm.group import Village
from wolves_in_silico.abm.player import Role


class Phase(Enum):
    DAY = 1
    NIGHT = 2


class Result:
    # TODO: remove(?)
    def __init__(self, nciv: list[int], nwolves: list[int], civ_win: bool):
        self.nciv = nciv
        self.nwolves = nwolves
        self.time: np.ndarray = np.arange(0, len(self.nciv) / 2, .5)
        self.civ_win = civ_win
        self.wolf_win: bool = not self.civ_win


class Game():
    village: Village
    finished: bool = False
    winner: Optional[Role] = None

    def __init__(self, nciv: int, nwolf: int):
        self.village: Village = Village(nciv=nciv, nwolf=nwolf)
        self.choose_mayor()
        self.phase: Phase = Phase.NIGHT
        self.nciv: list[int] = [nciv]
        self.nwolves: list[int] = [nwolf]

    def choose_mayor(self, p_wolf: float=.5):
        for member in self.village.population:
            member.is_mayor = False
        weights = self.village.nwolves * [p_wolf] + self.village.nciv * [1 - p_wolf]
        mayor = random.choices(self.village.population, weights=weights, k=1)[0]
        mayor.is_mayor = True

    def play(self) -> Result:
        while not self.finished:
            if self.phase == Phase.NIGHT:
                self.play_night()
            else:
                self.play_day()
            self.nciv.append(self.village.civilians.size)
            self.nwolves.append(self.village.wolves.size)
        return Result(nciv=self.nciv, nwolves=self.nwolves, civ_win=self.winner == Role.CIV)

    def play_night(self):
        target = self.village.wolves.get_night_kill(self.village.civilians)
        self.village.remove(target)
        self.finish_phase()

    def play_day(self):
        target = self.village.get_day_kill()
        self.village.remove(target)
        self.finish_phase()

    def finish_phase(self):
        if not self.village.has_mayor:
            self.choose_mayor()
        if self.village.wolves.size == 0:
            self.finished = True
            self.winner = Role.CIV
        if self.village.wolves.vote_size > self.village.civilians.vote_size:
            self.finished = True
            self.winner = Role.WOLF
        if self.phase == Phase.DAY:
            self.phase = Phase.NIGHT
        else:
            self.phase = Phase.DAY


