from enum import Enum
from typing import Optional
from abc import ABC, abstractmethod

import numpy as np

from wolves_in_silico.base.group import Village


class Phase(Enum):
    DAY = 1
    NIGHT = 2


class Role(Enum):
    WOLF = 1
    CIV = 2


class Result:
    def __init__(self, nciv: list[int], nwolves: list[int], civ_win: bool):
        self.nciv = nciv
        self.nwolves = nwolves
        self.time = np.arange(0, len(self.nciv) / 2, .5)
        self.civ_win = civ_win
        self.wolf_win = not self.civ_win


class Game(ABC):
    village: Village
    finished: bool = False
    winner: Optional[Role] = None

    def __init__(self, nciv, nwolf):
        self.choose_major()
        self.phase = Phase.NIGHT
        self.nciv = [nciv]
        self.nwolves = [nwolf]

    @abstractmethod
    def choose_major(self):
        pass

    def play(self) -> Result:
        while not self.finished:
            if self.phase == Phase.NIGHT:
                self.play_night()
            else:
                self.play_day()
            self.nciv.append(self.village.civilians.size)
            self.nwolves.append(self.village.wolves.size)
        return Result(nciv=self.nciv, nwolves=self.nwolves, civ_win=self.winner == Role.CIV)

    def finish_phase(self):
        if not self.village.has_major:
            self.choose_major()
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

    @abstractmethod
    def play_night(self):
        pass

    @abstractmethod
    def play_day(self):
        pass
