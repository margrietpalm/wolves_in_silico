from typing import Optional
import copy
import numpy as np
from enum import Enum

from wolves_in_silico.abm.group import Village
from wolves_in_silico.abm.player import Role, Player


class Phase(Enum):
    DAY = 1
    NIGHT = 2


class GameRecord:
    def __init__(self, states: list[Village], civ_win: bool):
        self.states = states
        self.nciv = [state.nciv for state in states]
        self.nwolves = [state.nwolves for state in states]
        self.time: np.ndarray = np.arange(0, len(self.states) / 2, .5)
        self.civ_win = civ_win
        self.wolf_win: bool = not self.civ_win

    def __repr__(self):
        return f'''
                number of civilians {" ".join(str(n) for n in self.nciv)}\n
                number of wolves    {" ".join(str(n) for n in self.nciv)}\n
                winner = {"civilians" if self.civ_win else "wolves"}\n'''


class Game():
    village: Village
    finished: bool = False
    winner: Optional[Role] = None

    def __init__(self, nciv: int, nwolf: int):
        self.village: Village = Village(nciv=nciv, nwolf=nwolf)
        self.phase: Phase = Phase.NIGHT
        self.states: list[Village] = [copy.deepcopy(self.village)]
        self.last_kill: Optional[Player] = None
        self.choose_mayor()

    def choose_mayor(self):
        # ensure there is only one mayor
        for member in self.village.population:
            member.is_mayor = False
        # if someone gets killed, that player chooses a mayor
        if self.last_kill is not None:
            mayor = self.last_kill.vote(self.village)
        else:
            mayor = self.village.choose_mayor()
        mayor.is_mayor = True

    def play(self) -> GameRecord:
        states: list[Village] = [copy.deepcopy(self.village)]
        while not self.finished:
            if self.phase == Phase.NIGHT:
                self.play_night()
            else:
                self.play_day()
            states.append(copy.deepcopy(self.village))
        return GameRecord(states=states, civ_win=self.winner == Role.CIV)

    def play_night(self):
        self.last_kill = self.village.wolves.get_night_kill(self.village.civilians)
        self.village.remove(self.last_kill)
        self.finish_phase()

    def play_day(self):
        self.last_kill = self.village.get_day_kill()
        self.village.remove(self.last_kill)
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
