import pytest

from wolves_in_silico.core.game import Game, Result, Phase
from wolves_in_silico.core.player import Role


def test_result():
    game = Game(nciv=2, nwolf=2)
    result = game.play()
    assert result.nciv == game.nciv
    assert result.nwolves == game.nwolves
    assert len(result.time) == len(game.nciv)
    assert result.civ_win == (game.winner == Role.CIV)
    assert result.civ_win is not result.wolf_win


class TestGame:
    def test_init(self):
        game = Game(nciv=2, nwolf=2)
        assert not game.finished
        assert game.winner is None
        assert game.village.has_major
        assert game.phase == Phase.NIGHT

    def test_choose_major(self):
        game = Game(nciv=2, nwolf=2)
        for member in game.village.population:
            member.is_major = False
        game.choose_major()
        assert game.village.has_major

    def test_play_night(self):
        game = Game(nciv=2, nwolf=2)
        game.play_night()
        assert game.village.size == 3
        assert game.village.nciv == 1
        assert game.village.nwolves == 2
        assert game.village.has_major
        assert game.phase == Phase.DAY

    def test_play_dau(self):
        game = Game(nciv=2, nwolf=2)
        game.play_day()
        assert game.village.size == 3
        assert game.phase == Phase.NIGHT

    def test_game_wolf_win(self):
        # this game is rigged for wolves to win after one night
        game = Game(nciv=2, nwolf=2)
        game.play()
        assert game.winner == Role.WOLF
        assert game.finished

    def test_game_civ_win(self):
        # This is currently very hard to rig because day kills are random
        game = Game(nciv=2, nwolf=0)
        game.phase = Phase.DAY
        game.play()
        assert game.winner == Role.CIV
        assert game.finished
